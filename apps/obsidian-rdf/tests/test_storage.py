from pathlib import Path

import pytest

from kb_obsidian_rdf import storage
from kb_obsidian_rdf.common import ContractError, Delivery, digest, json_bytes


@pytest.fixture(autouse=True)
def external_state(tmp_path, monkeypatch):
    monkeypatch.setenv("KB_OBSIDIAN_STATE_ROOT", str(tmp_path / "state"))


def delivery(text="before", *, extra=None):
    files = {"05-vocabulary/concepts/one.md": text.encode()}
    state = {
        "records.json": json_bytes({"format_version": 1, "records": []}),
        "projection.json": json_bytes({"format_version": 1, "entries": []}),
    }
    for path, data in (extra or {}).items():
        (files if path.startswith("05-vocabulary/") else state)[path] = data
    entries = lambda items: [{"path": path, "role": "reference", "size": len(data),
                              "sha256": digest(data)} for path, data in sorted(items.items())]
    manifest = {"format_version": 3, "mode": "preview",
                "files": entries(files), "state_files": entries(state)}
    if text != "before" or extra:
        manifest["previous_delivery"] = {"sha256": digest(delivery().state_files["manifest.json"])}
    state["manifest.json"] = json_bytes(manifest)
    files["06-views/topics.base"] = b"user view"
    files["home.md"] = b"first entry"
    return Delivery(files, state)


def admin(vault, relative):
    return storage.state_directory(vault) / relative


def test_initialization_never_overwrites_nonempty_target(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    content = vault / "private.md"
    content.write_text("personal content")
    with pytest.raises(ContractError, match="非空"):
        storage.initialize(vault, delivery())
    assert content.read_text() == "personal content"
    assert set(vault.iterdir()) == {content}


@pytest.mark.parametrize("conflict", ["edit", "unknown", "symlink"])
def test_refresh_refuses_managed_conflicts_without_touching_user_content(tmp_path, conflict):
    vault = tmp_path / "vault"
    storage.initialize(vault, delivery())
    (vault / "03-resources").mkdir(exist_ok=True)
    note = vault / "03-resources/mine.md"
    note.write_text("[[05-vocabulary/concepts/one]]")
    if conflict == "edit":
        (vault / "05-vocabulary/concepts/one.md").write_text("manual edit")
    elif conflict == "unknown":
        (vault / "05-vocabulary/private.md").write_text("private")
    else:
        outside = tmp_path / "outside.md"
        outside.write_text("must stay")
        (vault / "05-vocabulary/concepts/one.md").unlink()
        (vault / "05-vocabulary/concepts/one.md").symlink_to(outside)
    with pytest.raises(ContractError):
        storage.refresh(vault, delivery("after"), apply=True, offline=True)
    assert note.read_text() == "[[05-vocabulary/concepts/one]]"
    if conflict == "edit":
        assert (vault / "05-vocabulary/concepts/one.md").read_text() == "manual edit"
    elif conflict == "unknown":
        assert (vault / "05-vocabulary/private.md").read_text() == "private"
    else:
        assert outside.read_text() == "must stay"


def test_refresh_requires_explicit_apply_and_offline_and_preserves_user_files(tmp_path):
    vault = tmp_path / "vault"
    storage.initialize(vault, delivery())
    view = vault / "06-views/topics.base"
    view.write_text("my view")
    result = storage.refresh(vault, delivery("after"))
    assert result["status"] == "preview"
    assert (vault / "05-vocabulary/concepts/one.md").read_text() == "before"
    proposed = result["user_file_changes"]
    assert proposed[0]["path"] == "06-views/topics.base"
    assert (Path(proposed[0]["candidate"])).read_bytes() == b"user view"
    assert "my view" in proposed[0]["diff"]
    with pytest.raises(ContractError, match="关闭"):
        storage.refresh(vault, delivery("after"), apply=True)
    result = storage.refresh(vault, delivery("after"), apply=True, offline=True)
    assert result["status"] == "installed"
    assert (vault / "05-vocabulary/concepts/one.md").read_text() == "after"
    assert view.read_text() == "my view"
    assert storage.inspect(vault)["manifest_sha256"] == digest(delivery("after").state_files["manifest.json"])


@pytest.mark.parametrize("fail_on", [1, 2, 3, 4])
def test_directory_swap_failure_has_prewrite_journal_and_recovers(tmp_path, monkeypatch, fail_on):
    vault = tmp_path / "vault"
    storage.initialize(vault, delivery())
    rename = storage._move_directory
    calls = 0

    def fail(source, target):
        nonlocal calls
        calls += 1
        assert (admin(vault, "recovery.json")).exists()
        if calls == fail_on:
            raise OSError("injected directory interruption")
        rename(source, target)

    with monkeypatch.context() as patch:
        patch.setattr(storage, "_move_directory", fail)
        with pytest.raises(ContractError, match="恢复"):
            storage.refresh(vault, delivery("after"), apply=True, offline=True)
    with pytest.raises(ContractError, match="恢复"):
        storage.inspect(vault)
    result = storage.recover(vault, offline=True)
    assert result["status"] == "recovered"
    assert (vault / "05-vocabulary/concepts/one.md").read_text() == ("after" if fail_on == 4 else "before")
    assert storage.inspect(vault)["pending"] is None


def test_recovery_refuses_rollback_that_would_break_new_article_reference(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    storage.initialize(vault, delivery())
    rename = storage._move_directory

    def fail(source, target):
        if Path(target) == vault / "05-vocabulary":
            raise OSError("interrupted before candidate install")
        rename(source, target)

    with monkeypatch.context() as patch:
        patch.setattr(storage, "_move_directory", fail)
        with pytest.raises(ContractError):
            storage.refresh(vault, delivery("after", extra={"05-vocabulary/concepts/new.md": b"new"}), apply=True, offline=True)
    (vault / "03-resources").mkdir(exist_ok=True)
    note = vault / "03-resources/new.md"
    note.write_text('---\nsubject:\n  - "[[05-vocabulary/concepts/new]]"\n---\n')
    with pytest.raises(ContractError, match="引用"):
        storage.recover(vault, offline=True)
    assert "05-vocabulary/concepts/new" in note.read_text()
    assert (admin(vault, "recovery.json")).exists()


def test_symlinked_target_and_parent_never_modify_destination(tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    alias = tmp_path / "alias"
    alias.symlink_to(outside, target_is_directory=True)
    for vault in (alias, alias / "child"):
        with pytest.raises(ContractError, match="符号链接"):
            storage.initialize(vault, delivery())
    assert list(outside.iterdir()) == []


def test_all_tool_mutations_share_the_same_nonblocking_lock(tmp_path):
    vault = tmp_path / "vault"
    storage.initialize(vault, delivery())
    with storage.vault_lock(vault):
        with pytest.raises(ContractError, match="占用"):
            storage.refresh(vault, delivery("after"), apply=True, offline=True)
    assert (vault / "05-vocabulary/concepts/one.md").read_text() == "before"


def test_missing_receipt_digest_cannot_disable_baseline_verification(tmp_path):
    import json

    vault = tmp_path / "vault"
    storage.initialize(vault, delivery())
    path = admin(vault, "current.json")
    receipt = json.loads(path.read_bytes())
    del receipt["manifest_sha256"]
    path.write_bytes(json_bytes(receipt))
    with pytest.raises(ContractError, match="凭据"):
        storage.inspect(vault)


def test_recovery_completes_fully_installed_new_directory_after_receipt_failure(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    storage.initialize(vault, delivery())

    def fail(*args, **kwargs):
        raise OSError("cannot finish receipt")

    with monkeypatch.context() as patch:
        patch.setattr(storage, "_receipt", fail)
        with pytest.raises(ContractError, match="恢复"):
            storage.refresh(vault, delivery("after"), apply=True, offline=True)
    assert (vault / "05-vocabulary/concepts/one.md").read_text() == "after"
    result = storage.recover(vault, offline=True)
    assert result["resolution"] == "new_installed"
    assert (vault / "05-vocabulary/concepts/one.md").read_text() == "after"
    assert storage.inspect(vault)["pending"] is None


def test_recovery_refuses_raw_iri_dependency_introduced_after_interruption(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    storage.initialize(vault, delivery())
    new_records = json_bytes({"format_version": 1, "records": [{"identity": {"iri": "urn:test:new"}}]})
    candidate = delivery(extra={"records.json": new_records})
    rename = storage._move_directory

    def fail(source, target):
        if Path(target) == vault / "05-vocabulary":
            raise OSError("interrupt")
        rename(source, target)

    with monkeypatch.context() as patch:
        patch.setattr(storage, "_move_directory", fail)
        with pytest.raises(ContractError):
            storage.refresh(vault, candidate, apply=True, offline=True)
    (vault / "03-resources/new.md").write_text('---\nsubject: ["urn:test:new"]\n---\n')
    with pytest.raises(ContractError, match="原身份引用"):
        storage.recover(vault, offline=True)
    assert (admin(vault, "recovery.json")).exists()


def test_initial_directory_install_failure_never_leaves_a_completed_vault(tmp_path, monkeypatch):
    vault = tmp_path / "vault"

    def fail(*args):
        raise OSError("initial rename interruption")

    monkeypatch.setattr(storage, "_move_directory", fail)
    with pytest.raises(ContractError, match="初始化未完成"):
        storage.initialize(vault, delivery())
    assert not vault.exists()


def test_managed_file_modified_after_move_is_preserved_and_cannot_be_recovered_over(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    storage.initialize(vault, delivery())
    rename = storage._move_directory
    edited = None

    def concurrent_edit(source, target):
        nonlocal edited
        rename(source, target)
        if Path(source) == vault / "05-vocabulary":
            edited = Path(target) / "concepts/one.md"
            edited.write_text("late external edit")

    monkeypatch.setattr(storage, "_move_directory", concurrent_edit)
    with pytest.raises(ContractError, match="发生变化"):
        storage.refresh(vault, delivery("after"), apply=True, offline=True)
    with pytest.raises(ContractError, match="发生变化"):
        storage.recover(vault, offline=True)
    assert edited.read_text() == "late external edit"


def test_case_aliases_on_insensitive_volumes_do_not_bypass_tool_lock(tmp_path):
    vault = tmp_path / "Vault"
    storage.initialize(vault, delivery())
    alias = tmp_path / "vault"
    if not alias.exists() or not alias.samefile(vault):
        pytest.skip("requires a case-insensitive filesystem")
    with storage.vault_lock(vault):
        with pytest.raises(ContractError, match="占用"):
            storage.refresh(alias, delivery("after"), apply=True, offline=True)


def test_missing_candidate_cannot_silently_discard_unchecked_new_dependencies(tmp_path, monkeypatch):
    import json
    import shutil

    vault = tmp_path / "vault"
    storage.initialize(vault, delivery())

    def fail(*args):
        raise OSError("interrupt before first rename")

    with monkeypatch.context() as patch:
        patch.setattr(storage, "_move_directory", fail)
        with pytest.raises(ContractError):
            storage.refresh(vault, delivery("after"), apply=True, offline=True)
    journal = json.loads((admin(vault, "recovery.json")).read_bytes())
    shutil.rmtree(admin(vault, journal["candidate"]))
    with pytest.raises(ContractError, match="候选"):
        storage.recover(vault, offline=True)
    assert (vault / "05-vocabulary/concepts/one.md").read_text() == "before"
    assert (admin(vault, "recovery.json")).exists()


def interrupted_refresh(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    storage.initialize(vault, delivery())
    rename = storage._move_directory

    def fail(source, target):
        if Path(target) == vault / "05-vocabulary":
            raise OSError("interrupted before candidate install")
        rename(source, target)

    with monkeypatch.context() as patch:
        patch.setattr(storage, "_move_directory", fail)
        with pytest.raises(ContractError):
            storage.refresh(vault, delivery("after", extra={"05-vocabulary/concepts/new.md": b"new"}),
                            apply=True, offline=True)
    (vault / "03-resources/sub").mkdir()
    return vault


@pytest.mark.parametrize("body", [
    "[new](../../05-vocabulary/concepts/new.md)",
    "[new](./../../05-vocabulary/concepts/new.md)",
    "[new](../../05-vocabulary/concepts/%6Eew.md#section)",
    "[new](../../05-vocabulary/concepts/new.md 'title')",
    "[new][target]\n\n[target]: ../../05-vocabulary/concepts/new.md",
    "![new](../../05-vocabulary/concepts/new.md)",
    "[[05-vocabulary/concepts/new|*新概念*]]",
])
def test_recovery_resolves_real_article_links_before_any_rollback(tmp_path, monkeypatch, body):
    vault = interrupted_refresh(tmp_path, monkeypatch)
    note = vault / "03-resources/sub/a.md"
    note.write_text(body)
    with pytest.raises(ContractError, match="引用"):
        storage.recover(vault, offline=True)
    assert note.read_text() == body
    assert (admin(vault, "recovery.json")).exists()
    assert not (vault / "05-vocabulary").exists()


@pytest.mark.parametrize("body", [
    "`[new](../../05-vocabulary/concepts/new.md)`",
    "`[[05-vocabulary/concepts/new]]`",
    "```markdown\n[new](../../05-vocabulary/concepts/new.md)\n[[05-vocabulary/concepts/new]]\n```",
    r"\[[05-vocabulary/concepts/new]]",
    r"\[new](../../05-vocabulary/concepts/new.md)",
    "普通文字。\n\n[unused]: ../../05-vocabulary/concepts/new.md",
])
def test_recovery_does_not_treat_code_or_escaped_examples_as_dependencies(tmp_path, monkeypatch, body):
    vault = interrupted_refresh(tmp_path, monkeypatch)
    note = vault / "03-resources/sub/a.md"
    note.write_text(body)
    result = storage.recover(vault, offline=True)
    assert result["resolution"] == "old_restored"
    assert note.read_text() == body
    assert (vault / "05-vocabulary/concepts/one.md").read_text() == "before"


@pytest.mark.parametrize("href", ["../../../outside.md", "%2E%2E/%2E%2E/%2E%2E/outside.md"])
def test_recovery_rejects_local_link_traversal_outside_vault(tmp_path, monkeypatch, href):
    vault = interrupted_refresh(tmp_path, monkeypatch)
    (vault / "03-resources/sub/a.md").write_text(f"[outside]({href})")
    with pytest.raises(ContractError, match="不安全|越界"):
        storage.recover(vault, offline=True)
    assert (admin(vault, "recovery.json")).exists()


def test_engineering_data_never_enters_vault_and_fast_read_verifies_identity_data(tmp_path):
    vault = tmp_path / "vault"
    storage.initialize(vault, delivery())
    assert set(path.name for path in vault.iterdir()) == {
        "home.md", "00-inbox", "01-projects", "02-areas", "03-resources", "04-archives",
        "05-vocabulary", "06-views", "07-templates", "08-attachments",
    }
    state = storage.read_state(vault)
    assert state["state_dir"] == str(storage.state_directory(vault))
    assert "records.json" in state["state_files"]
    assert state["records"] == {"format_version": 1, "records": []}
    (vault / "05-vocabulary/concepts/one.md").write_text("late page edit")
    assert storage.read_state(vault)["manifest_sha256"] == state["manifest_sha256"]
    with pytest.raises(ContractError, match="发生变化"):
        storage.inspect(vault)
    admin(vault, "current/records.json").write_text('{}')
    with pytest.raises(ContractError, match="发生变化"):
        storage.read_state(vault)


@pytest.mark.parametrize("location", ["inside", "ancestor", "same"])
def test_state_overlap_is_rejected_before_any_write(tmp_path, location):
    vault = tmp_path / "vault"
    root = {"inside": vault / "admin", "ancestor": tmp_path, "same": vault}[location]
    with pytest.raises(ContractError, match="库外|重叠"):
        storage.initialize(vault, delivery(), state_root=root)
    assert not vault.exists()


def test_separate_state_root_cannot_claim_an_existing_vault(tmp_path):
    vault = tmp_path / "vault"
    storage.initialize(vault, delivery())
    with pytest.raises(ContractError, match="非空"):
        storage.initialize(vault, delivery(), state_root=tmp_path / "other-state")
    with pytest.raises(ContractError, match="缺失|绑定"):
        storage.inspect(vault, state_root=tmp_path / "other-state")


def test_refresh_rejects_stale_previous_delivery(tmp_path):
    vault = tmp_path / "vault"
    storage.initialize(vault, delivery())
    storage.refresh(vault, delivery("after"), apply=True, offline=True)
    with pytest.raises(ContractError, match="基准|上一"):
        storage.refresh(vault, delivery("outdated"), apply=True, offline=True)
    assert (vault / "05-vocabulary/concepts/one.md").read_text() == "after"


@pytest.mark.parametrize("folder", ["01-projects", "02-areas", "03-resources", "04-archives"])
def test_all_para_areas_protect_references_during_recovery(tmp_path, monkeypatch, folder):
    vault = interrupted_refresh(tmp_path, monkeypatch)
    note = vault / folder / "new.md"
    note.write_text("[[05-vocabulary/concepts/new]]")
    with pytest.raises(ContractError, match="引用"):
        storage.recover(vault, offline=True)
    assert note.read_text() == "[[05-vocabulary/concepts/new]]"


def test_inbox_is_not_interpreted_as_model_content_during_recovery(tmp_path, monkeypatch):
    vault = interrupted_refresh(tmp_path, monkeypatch)
    (vault / "00-inbox/free-note.md").write_text('---\nunclosed yaml [\n[[05-vocabulary/concepts/new]]')
    assert storage.recover(vault, offline=True)["resolution"] == "old_restored"


@pytest.mark.parametrize("fail_on", [1, 2])
def test_initial_partial_install_has_external_recovery_and_can_finish(tmp_path, monkeypatch, fail_on):
    vault = tmp_path / "vault"
    move = storage._move_directory
    calls = 0
    def fail(source, target):
        nonlocal calls
        calls += 1
        assert admin(vault, "recovery.json").is_file()
        if calls == fail_on:
            raise OSError("initial split install interruption")
        move(source, target)
    with monkeypatch.context() as patch:
        patch.setattr(storage, "_move_directory", fail)
        with pytest.raises(ContractError, match="初始化未完成"):
            storage.initialize(vault, delivery())
    assert admin(vault, "recovery.json").is_file()
    with pytest.raises(ContractError, match="恢复"):
        storage.read_state(vault)
    assert storage.recover(vault, offline=True)["status"] == "recovered"
    assert storage.inspect(vault)["pending"] is None
    assert (vault / "home.md").read_text() == "first entry"


def test_state_on_other_filesystem_is_rejected_before_writes(tmp_path, monkeypatch):
    vault, state_root = tmp_path / "vault", tmp_path / "state"
    monkeypatch.setattr(storage, "_device", lambda path: 1 if path == vault else 2)
    with pytest.raises(ContractError, match="同一文件系统"):
        storage.initialize(vault, delivery(), state_root=state_root)
    assert not vault.exists()
    assert not state_root.exists()


def test_state_only_refresh_recovers_new_version_after_receipt_failure(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    storage.initialize(vault, delivery())
    candidate = delivery(extra={"projection.json": json_bytes({"format_version": 1, "entries": ["changed"]})})
    with monkeypatch.context() as patch:
        patch.setattr(storage, "_receipt", lambda *args, **kwargs: (_ for _ in ()).throw(OSError("receipt failure")))
        with pytest.raises(ContractError, match="恢复"):
            storage.refresh(vault, candidate, apply=True, offline=True)
    assert storage.recover(vault, offline=True)["resolution"] == "new_installed"
    assert storage.inspect(vault)["manifest_sha256"] == digest(candidate.state_files["manifest.json"])


def test_interrupted_initial_preparation_can_be_aborted_and_retried_without_losing_evidence(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    write = storage._write
    def fail(path, *args, **kwargs):
        if path.name == "projection.json":
            raise OSError("state preparation failed")
        return write(path, *args, **kwargs)
    with monkeypatch.context() as patch:
        patch.setattr(storage, "_write", fail)
        with pytest.raises(ContractError, match="初始化未完成"):
            storage.initialize(vault, delivery())
    result = storage.recover(vault, offline=True)
    assert result["resolution"] == "initialization_aborted"
    assert Path(result["preserved_state"]).is_dir()
    assert not vault.exists()
    storage.initialize(vault, delivery())
    assert storage.inspect(vault)["pending"] is None


@pytest.mark.parametrize("path", ["03-resources/source.ttl", "06-views/report.json", "07-templates/manifest.json"])
def test_delivery_cannot_leak_engineering_files_into_public_directories(tmp_path, path):
    vault = tmp_path / "vault"
    candidate = delivery()
    candidate.vault_files[path] = b"engineering data"
    with pytest.raises(ContractError, match="初建文件"):
        storage.initialize(vault, candidate)
    assert not vault.exists()
    assert not storage.state_directory(vault).exists()
