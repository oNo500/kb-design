"""Presence counts from SHACL field declarations, without running pySHACL."""
from collections import defaultdict

from rdflib import Graph, Literal, RDF, RDFS
from rdflib.namespace import SH

from .structure import TARGETS, conditions_for, fields_for, load_structure


def inventory(data: Graph, *, structure=None, roots=None, resource_type=None) -> dict:
    if structure is None:
        structure, roots = load_structure()
    if roots is None:
        raise ValueError("Resource shape roots are required")
    by_predicate, types, parents = defaultdict(set), defaultdict(set), defaultdict(set)
    values, empty = defaultdict(int), defaultdict(int)
    subjects = set()
    for subject, predicate, value in data:
        subjects.add(subject)
        by_predicate[predicate].add(subject)
        values[subject, predicate] += 1
        if isinstance(value, Literal) and str(value) == "":
            empty[subject, predicate] += 1
        if predicate == RDF.type:
            types[value].add(subject)
        elif predicate == RDFS.subClassOf:
            parents[subject].add(value)

    def instances(target):
        selected = set(types[target])
        for candidate, nodes in types.items():
            pending, seen = [candidate], set()
            while pending:
                current = pending.pop()
                if current in seen:
                    continue
                seen.add(current)
                if current == target:
                    selected.update(nodes)
                    break
                pending.extend(parents[current])
        return selected

    def select_targets(shape):
        if next(structure.objects(shape, SH.target), None) is not None:
            raise ValueError(f"Custom SHACL targets are not supported by inventory: {shape}")
        has_scope = any(next(structure.objects(shape, p), None) is not None for p in TARGETS[:-1])
        selected = set(structure.objects(shape, SH.targetNode))
        for cls in structure.objects(shape, SH.targetClass):
            selected.update(instances(cls))
        for predicate in structure.objects(shape, SH.targetSubjectsOf):
            selected.update(by_predicate[predicate])
        for predicate in structure.objects(shape, SH.targetObjectsOf):
            selected.update(data.objects(None, predicate))
        return has_scope, selected

    result, classified, all_fields = [], set(), set()
    condition_resources = defaultdict(set)
    for root in roots:
        name = str(root).rsplit(":", 1)[-1]
        fields = fields_for(structure, root)
        has_scope, selected = select_targets(root)
        classified.update(selected)
        if resource_type and resource_type != name:
            continue
        all_fields.update(fields)
        for condition in conditions_for(structure, root):
            condition_resources[condition].add(name)
        rows = []
        for predicate, shapes in sorted(fields.items(), key=lambda pair: str(pair[0])):
            present = selected & by_predicate[predicate]
            descriptions = sorted({str(d) for s in shapes for d in structure.objects(s, SH.description)})
            rows.append({
                "field": str(predicate), "name": structure.namespace_manager.normalizeUri(predicate),
                "shapes": sorted(map(str, shapes)), "description": descriptions,
                "present": len(present) if selected else None,
                "absent": len(selected - present) if selected else None,
                "empty_values": sum(empty.get((s, predicate), 0) for s in selected) if selected else None,
                "statements": sum(values.get((s, predicate), 0) for s in selected) if selected else None,
            })
        result.append({
            "type": name, "shape": str(root), "label": str(structure.value(root, SH.name) or name),
            "status": "scope_required" if not has_scope else "no_objects" if not selected else "counted",
            "objects": len(selected) if has_scope else None, "fields": rows,
        })
    if resource_type and not result:
        raise ValueError(f"Unknown resource type: {resource_type}")
    conditions = []
    for shape, resource_types in sorted(condition_resources.items(), key=lambda pair: str(pair[0])):
        has_scope, selected = select_targets(shape)
        deactivated = structure.value(shape, SH.deactivated) == Literal(True)
        conditions.append({
            "shape": str(shape), "name": str(structure.value(shape, SH.name) or shape),
            "resource_types": sorted(resource_types),
            "scope_status": "deactivated" if deactivated else "specified" if has_scope else "unspecified",
            "selected_objects": len(selected) if has_scope else None,
            "validation_executed": False,
        })
    # This overview also finds field use on auxiliary/untyped resources.
    overview = [{"field": str(p), "name": structure.namespace_manager.normalizeUri(p),
                 "present_subjects": len(by_predicate[p]),
                 "statements": sum(values[s, p] for s in by_predicate[p])}
                for p in sorted(all_fields, key=str)]
    return {"triples": len(data), "subjects": len(subjects), "resources": result,
            "fields": overview, "conditions": conditions,
            "unclassified_subjects": sorted(map(str, subjects - classified)),
            "untyped_subjects": sorted(map(str, subjects - by_predicate[RDF.type]))}
