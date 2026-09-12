"""Identify document roles independently of their topic directory.

Legacy decision directories remain readable for historical snapshots and test
repositories. Current documents use role prefixes under docs topic directories.
Neither a filename nor a directory grants approval; decision schemas and their
existing acceptance rules still determine authority.
"""

from fnmatch import fnmatchcase
from pathlib import Path, PurePosixPath


# Preserve the existing source/term selection of each relocated decision.
# This table changes locations, never decision IDs, patches or approval status.
# Unknown new names remain visible as decisions, but cannot acquire a source or
# term selection merely by containing schema-looking metadata.
_DECISION_NAMES = {
    "决定-终端访问.md": "obsidian-agent-entry.md",
    "决定-视图排序.md": "obsidian-base-sort-preferences.md",
    "决定-词表参考刷新.md": "obsidian-reference-refresh.md",
    "决定-Obsidian 工具归属.md": "obsidian-tool-location.md",
    "决定-应用约束与表示分层.md": "application-profile-boundary.md",
    "决定-设计与应用分离.md": "form-independence.md",
    "决定-预览归属.md": "vocab-preview-location.md",
    "决定-仓库布局.md": "monorepo-layout.md",
    "决定-当前阶段.md": "current-stage-scope.md",
    "决定-决策权的首批边界.md": "decision-rights-defaults.md",
    "决定-文档主题组织.md": "docs-topic-organization.md",
    "决定-文档文件命名.md": "document-filenames.md",
    "决定-项目约定入口.md": "project-instructions-entry.md",
    "决定-验证投入.md": "verification-effort.md",
    "决定-内容单元标识符.md": "content-unit-identifiers.md",
    "决定-公众人物边界.md": "person-admission-clarification.md",
    "决定-证据阶段.md": "evidence-stage-boundary.md",
    "决定-参考文献分离.md": "source-bibliography-separation.md",
    "决定-来源收尾.md": "source-completion.md",
    "决定-来源批次采纳.md": "source-data-batch.md",
    "决定-来源核对取舍.md": "source-evidence-priority.md",
    "决定-来源执行.md": "source-execution-boundary.md",
    "决定-来源字段采纳.md": "source-field-adoptions.md",
    "决定-来源字段值.md": "source-field-values.md",
    "决定-来源模式.md": "source-governance-schema.md",
    "决定-来源迁移.md": "source-migration-policy.md",
    "决定-来源探测.md": "source-probe-policy.md",
    "决定-来源字段合同.md": "source-v2-field-contract.md",
    "决定-来源校验.md": "source-validation-policy.md",
    "决定-译名依据扩展.md": "industry-translation-basis.md",
    "决定-模型知识译名.md": "model-knowledge-translation.md",
    "决定-模型译名标记.md": "model-translation-marker.md",
    "决定-术语来源采纳.md": "source-term-complete-citations.md",
    "决定-语言依据结构.md": "structured-label-basis.md",
    "决定-术语发布条件.md": "term-complete-publication.md",
    "决定-术语结构采纳.md": "term-complete-structure.md",
    "决定-术语具体值.md": "term-data-values.md",
    "决定-术语依据范围.md": "term-evidence-scope.md",
    "决定-术语实施范围.md": "term-infrastructure-scope.md",
    "决定-限定定义许可.md": "term-limited-definition-source-use.md",
    "决定-译名检索来源.md": "translation-reference-resources.md",
    "决定-原样复制与本地分析分层.md": "borrow-and-analyze.md",
    "决定-树按学科而非分面.md": "tree-by-discipline.md"
}


def decision_selection_name(path):
    path = PurePosixPath(path)
    if path.name.startswith("决定-"):
        return _DECISION_NAMES.get(path.name, path.name)
    if path.name.startswith("decision-"):
        return path.name[len("decision-"):]
    if path.parent == PurePosixPath("docs/decisions"):
        return path.name
    return None


def is_decision_path(path, patterns=("*.md",)):
    path = PurePosixPath(path)
    if not path.parts or path.parts[0] != "docs":
        return False
    name = decision_selection_name(path)
    return name is not None and any(fnmatchcase(name, pattern) for pattern in patterns)


def decision_paths(directory: Path, patterns=("*.md",)):
    """Find only decision documents; do not scan copied proposal metadata."""
    directory = Path(directory)
    if directory.name == "decisions":
        # Explicit legacy snapshot/fixture directory, not all its siblings.
        return sorted(path for path in directory.glob("*.md")
                      if is_decision_path(PurePosixPath("docs/decisions") / path.name, patterns))
    return sorted(path for path in directory.rglob("*.md")
                  if is_decision_path(PurePosixPath("docs") / path.relative_to(directory), patterns))


def document_role(path):
    path = PurePosixPath(path)
    if not path.parts or path.parts[0] != "docs":
        return None
    if path.name.startswith(("proposal-", "提案-")) or path.as_posix().startswith("docs/drafts/"):
        return "draft"
    if is_decision_path(path):
        return "history"
    if path.name.startswith(("reading-", "阅读-")) or path.as_posix().startswith("docs/references/"):
        return "source"
    return "formal"
