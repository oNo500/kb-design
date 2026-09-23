"""Each behavior test owns its external application state."""
import pytest


@pytest.fixture(autouse=True)
def isolated_state_root(tmp_path, monkeypatch):
    monkeypatch.setenv("KB_OBSIDIAN_STATE_ROOT", str(tmp_path.resolve() / "state"))
