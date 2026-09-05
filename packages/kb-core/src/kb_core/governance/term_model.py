from kb_core.repository import project_root
from collections import Counter
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Literal, Optional, Sequence

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

from kb_core.source_model import (
    ReferenceUse,
    SCHEMA_IDS,
    build_schema_documents,
    validate_references,
)


Workflow = Literal["candidate", "active", "deprecated"]
AdministrativeStatus = Literal[
    "preferredTerm-admn-sts",
    "admittedTerm-admn-sts",
    "deprecatedTerm-admn-sts",
    "supersededTerm-admn-sts",
]
LanguageTag = Literal["en", "zh-Hans", "zh-Hant"]

ADMINISTRATIVE_STATUSES = (
    "preferredTerm-admn-sts",
    "admittedTerm-admn-sts",
    "deprecatedTerm-admn-sts",
    "supersededTerm-admn-sts",
)
WORKFLOWS = ("candidate", "active", "deprecated")
LANGUAGE_TAGS = ("en", "zh-Hans", "zh-Hant")

ROOT = project_root(__file__)
TERMS_SCHEMA = ROOT / "schemas" / "terms-v1.schema.json"


@dataclass(frozen=True)
class TermIssue:
    code: str
    origin: Literal["term", "source"]
    path: str
    message: str


@dataclass(frozen=True)
class HistoryEvent:
    date: str
    event: str
    decision: str
    reason: str
    from_value: Optional[str]
    to_value: Optional[str]
    linked_terms: Sequence[str]


@dataclass(frozen=True)
class TermRecord:
    id: str
    text: str
    administrative_status: AdministrativeStatus
    basis: Sequence[object]
    replaced_by: Optional[str]
    history: Sequence[HistoryEvent]


@dataclass(frozen=True)
class LanguageRecord:
    language: LanguageTag
    terms: Sequence[TermRecord]


@dataclass(frozen=True)
class DefinitionRecord:
    language: LanguageTag
    text: str
    basis: Sequence[object]


@dataclass(frozen=True)
class SubjectFieldRecord:
    topic_id: str
    basis: Sequence[object]


@dataclass(frozen=True)
class ConceptRecord:
    id: str
    subject_fields: Sequence[SubjectFieldRecord]
    definitions: Sequence[DefinitionRecord]
    languages: Sequence[LanguageRecord]
    basis: Sequence[object]
    source: Optional[object]
    match: Sequence[object]
    workflow: Workflow
    history: Sequence[HistoryEvent]


@dataclass(frozen=True)
class TermsDocument:
    schema: str
    version: int
    concepts: Sequence[ConceptRecord]


class TermsSchemaError(ValueError):
    def __init__(self, issues: Sequence[TermIssue]):
        self.issues = tuple(issues)
        super().__init__("; ".join(
            f"{issue.code} {issue.path}: {issue.message}" for issue in self.issues
        ))


def exported_reference_uris():
    return {
        "basis": SCHEMA_IDS["source-entities.schema.json"] + "#/$defs/basisItem",
        "source": SCHEMA_IDS["source-migration.schema.json"] + "#/$defs/source",
        "match": SCHEMA_IDS["source-migration.schema.json"] + "#/$defs/match",
    }


def object_schema(required, properties, all_of=None):
    value = {
        "type": "object",
        "required": list(required),
        "additionalProperties": False,
        "properties": properties,
    }
    if all_of is not None:
        value["allOf"] = all_of
    return value


def local_term_definitions(refs):
    concept_pattern = (
        r"^tc-[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-"
        r"[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
    )
    term_pattern = concept_pattern.replace("^tc-", "^tm-")
    language = {"enum": list(LANGUAGE_TAGS)}
    basis = {
        "type": "array",
        "minItems": 1,
        "items": {"$ref": refs["basis"]},
    }
    history = object_schema(
        ("date", "event", "decision", "reason", "from_value", "to_value", "linked_terms"),
        {
            "date": {"type": "string", "format": "date"},
            "event": {"type": "string", "minLength": 1},
            "decision": {"type": "string", "minLength": 1},
            "reason": {"type": "string", "minLength": 1},
            "from_value": {"type": ["string", "null"]},
            "to_value": {"type": ["string", "null"]},
            "linked_terms": {
                "type": "array",
                "uniqueItems": True,
                "items": {"type": "string", "pattern": term_pattern},
            },
        },
    )
    term = object_schema(
        ("id", "text", "administrative_status", "basis", "history"),
        {
            "id": {"type": "string", "pattern": term_pattern},
            "text": {"type": "string", "minLength": 1},
            "administrative_status": {"enum": list(ADMINISTRATIVE_STATUSES)},
            "basis": {"$ref": "#/$defs/basis"},
            "replaced_by": {"type": "string", "pattern": term_pattern},
            "history": {
                "type": "array",
                "minItems": 1,
                "items": {"$ref": "#/$defs/history"},
            },
        },
        [{
            "if": {
                "properties": {
                    "administrative_status": {"const": "supersededTerm-admn-sts"},
                },
                "required": ["administrative_status"],
            },
            "then": {"required": ["replaced_by"]},
            "else": {"not": {"required": ["replaced_by"]}},
        }],
    )
    language_record = object_schema(
        ("language", "terms"),
        {
            "language": {"$ref": "#/$defs/language"},
            "terms": {
                "type": "array",
                "minItems": 1,
                "uniqueItems": True,
                "items": {"$ref": "#/$defs/term"},
            },
        },
    )
    subject_field = object_schema(
        ("topic_id", "basis"),
        {
            "topic_id": {"type": "string", "minLength": 1},
            "basis": {"$ref": "#/$defs/basis"},
        },
    )
    definition = object_schema(
        ("language", "text", "basis"),
        {
            "language": {"$ref": "#/$defs/language"},
            "text": {"type": "string", "minLength": 1},
            "basis": {"$ref": "#/$defs/basis"},
        },
    )
    concept = object_schema(
        ("id", "subject_fields", "definitions", "languages", "basis", "workflow", "history"),
        {
            "id": {"type": "string", "pattern": concept_pattern},
            "subject_fields": {
                "type": "array",
                "minItems": 1,
                "uniqueItems": True,
                "items": {"$ref": "#/$defs/subject_field"},
            },
            "definitions": {
                "type": "array",
                "minItems": 1,
                "uniqueItems": True,
                "items": {"$ref": "#/$defs/definition"},
            },
            "languages": {
                "type": "array",
                "minItems": 1,
                "uniqueItems": True,
                "items": {"$ref": "#/$defs/language_record"},
            },
            "basis": {"$ref": "#/$defs/basis"},
            "source": {"$ref": "#/$defs/source_reference"},
            "match": {
                "type": "array",
                "uniqueItems": True,
                "items": {"$ref": "#/$defs/match_reference"},
            },
            "workflow": {"enum": list(WORKFLOWS)},
            "history": {
                "type": "array",
                "minItems": 1,
                "items": {"$ref": "#/$defs/history"},
            },
        },
    )
    return {
        "language": language,
        "basis": basis,
        "source_reference": {"$ref": refs["source"]},
        "match_reference": {"$ref": refs["match"]},
        "history": history,
        "term": term,
        "language_record": language_record,
        "subject_field": subject_field,
        "definition": definition,
        "concept": concept,
    }


def build_terms_schema():
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "urn:kb-design:schema:terms:1",
        "type": "object",
        "required": ["schema", "version", "concepts"],
        "additionalProperties": False,
        "properties": {
            "schema": {"const": "urn:kb-design:schema:terms:1"},
            "version": {"const": 1},
            "concepts": {
                "type": "array",
                "items": {"$ref": "#/$defs/concept"},
            },
        },
        "$defs": local_term_definitions(exported_reference_uris()),
    }


def _format_path(parts):
    value = ""
    for part in parts:
        value += f"[{part}]" if isinstance(part, int) else (("." if value else "") + part)
    return value or "$"


def schema_issues(value, schema=None, source_schemas=None):
    if schema is None:
        schema = json.loads(TERMS_SCHEMA.read_text(encoding="utf-8"))
    if source_schemas is None:
        source_schemas = build_schema_documents().values()
    registry = Registry().with_resources(
        (item["$id"], Resource.from_contents(item)) for item in source_schemas
    )
    validator = Draft202012Validator(
        schema, registry=registry, format_checker=FormatChecker(),
    )
    return tuple(sorted((
        TermIssue(
            "TERM_SCHEMA_INVALID",
            "term",
            _format_path(error.absolute_path),
            error.message,
        )
        for error in validator.iter_errors(value)
    ), key=lambda issue: (issue.path, issue.message)))


def _parse_history(value):
    return HistoryEvent(
        value["date"],
        value["event"],
        value["decision"],
        value["reason"],
        value["from_value"],
        value["to_value"],
        tuple(value["linked_terms"]),
    )


def parse_terms(value):
    concepts = []
    for concept in value["concepts"]:
        subject_fields = tuple(
            SubjectFieldRecord(row["topic_id"], tuple(row["basis"]))
            for row in concept["subject_fields"]
        )
        definitions = tuple(
            DefinitionRecord(row["language"], row["text"], tuple(row["basis"]))
            for row in concept["definitions"]
        )
        languages = []
        for language in concept["languages"]:
            terms = tuple(
                TermRecord(
                    row["id"],
                    row["text"],
                    row["administrative_status"],
                    tuple(row["basis"]),
                    row.get("replaced_by"),
                    tuple(_parse_history(event) for event in row["history"]),
                )
                for row in language["terms"]
            )
            languages.append(LanguageRecord(language["language"], terms))
        concepts.append(ConceptRecord(
            concept["id"],
            subject_fields,
            definitions,
            tuple(languages),
            tuple(concept["basis"]),
            concept.get("source"),
            tuple(concept.get("match", ())),
            concept["workflow"],
            tuple(_parse_history(event) for event in concept["history"]),
        ))
    return TermsDocument(value["schema"], value["version"], tuple(concepts))


def load_terms(path: Path):
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    issues = schema_issues(value)
    if issues:
        raise TermsSchemaError(issues)
    return parse_terms(value)


def collect_reference_uses(document, file="terms"):
    uses = []
    for concept_index, concept in enumerate(document.concepts):
        record = concept.id
        for basis_index, basis in enumerate(concept.basis):
            uses.append(ReferenceUse(
                "basis", file, record,
                f"concepts[{concept_index}].basis[{basis_index}]", basis,
            ))
        for index, field in enumerate(concept.subject_fields):
            for basis_index, basis in enumerate(field.basis):
                uses.append(ReferenceUse(
                    "basis", file, record,
                    f"concepts[{concept_index}].subject_fields[{index}].basis[{basis_index}]",
                    basis,
                ))
        for index, definition in enumerate(concept.definitions):
            for basis_index, basis in enumerate(definition.basis):
                uses.append(ReferenceUse(
                    "basis", file, record,
                    f"concepts[{concept_index}].definitions[{index}].basis[{basis_index}]",
                    basis,
                ))
        for language_index, language in enumerate(concept.languages):
            for term_index, term in enumerate(language.terms):
                for basis_index, basis in enumerate(term.basis):
                    uses.append(ReferenceUse(
                        "basis", file, record,
                        f"concepts[{concept_index}].languages[{language_index}].terms[{term_index}].basis[{basis_index}]",
                        basis,
                    ))
        if concept.source is not None:
            uses.append(ReferenceUse(
                "source", file, record, f"concepts[{concept_index}].source", concept.source,
            ))
        for index, match in enumerate(concept.match):
            uses.append(ReferenceUse(
                "match", file, record, f"concepts[{concept_index}].match[{index}]", match,
            ))
    return tuple(uses)


def _duplicate_issues(values, code, path):
    return [
        TermIssue(code, "term", path, f"duplicate stable id {value}")
        for value, count in Counter(values).items() if count > 1
    ]


def validate_terms(document, source_root: Path, topic_ids):
    issues = []
    issues.extend(_duplicate_issues(
        (concept.id for concept in document.concepts),
        "TERM_CONCEPT_ID_DUPLICATE", "concepts",
    ))
    all_term_ids = [
        term.id
        for concept in document.concepts
        for language in concept.languages
        for term in language.terms
    ]
    issues.extend(_duplicate_issues(all_term_ids, "TERM_ID_DUPLICATE", "concepts"))

    for concept_index, concept in enumerate(document.concepts):
        language_counts = Counter(row.language for row in concept.languages)
        for language, count in language_counts.items():
            if count > 1:
                issues.append(TermIssue(
                    "TERM_LANGUAGE_DUPLICATE", "term",
                    f"concepts[{concept_index}].languages", f"duplicate language {language}",
                ))
        for language_index, language in enumerate(concept.languages):
            text_counts = Counter(term.text for term in language.terms)
            for text, count in text_counts.items():
                if count > 1:
                    issues.append(TermIssue(
                        "TERM_TEXT_DUPLICATE", "term",
                        f"concepts[{concept_index}].languages[{language_index}].terms",
                        f"duplicate term text {text}",
                    ))
        if concept.workflow == "active":
            definition_counts = Counter(row.language for row in concept.definitions)
            for language, count in definition_counts.items():
                if count > 1:
                    issues.append(TermIssue(
                        "TERM_ACTIVE_DEFINITION_CONFLICT", "term",
                        f"concepts[{concept_index}].definitions",
                        f"active concept has {count} definitions for {language}",
                    ))
        for field_index, field in enumerate(concept.subject_fields):
            if field.topic_id not in topic_ids:
                issues.append(TermIssue(
                    "TERM_SUBJECT_FIELD_UNKNOWN", "term",
                    f"concepts[{concept_index}].subject_fields[{field_index}].topic_id",
                    f"unknown topic id {field.topic_id}",
                ))

    for issue in validate_references(source_root, collect_reference_uses(document)):
        issues.append(TermIssue(
            "TERM_SOURCE_CONTRACT_" + issue.code,
            "source",
            issue.field_path,
            f"{issue.file}:{issue.record}:{issue.field_path}: {issue.message}",
        ))
    return tuple(sorted(issues, key=lambda issue: (
        issue.path, issue.code, issue.message,
    )))
