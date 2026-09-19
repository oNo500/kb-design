"""Load packaged SHACL text without depending on a validator or old tools.

The caller chooses the data graph and validation engine. This module neither
reads vocabulary data nor runs inference, validation, translation or writes.
"""
from importlib.resources import files

_STANDARD = ("skos.ttl", "skos-xl.ttl", "skos-thes.ttl")
_PROFILES = {
    "standard": _STANDARD,
    "target": (*_STANDARD, "metadata.ttl", "profile.ttl"),
}


def read_shapes(profile: str = "target") -> str:
    """Return Turtle for the explicitly selected, bundled rule set.

    ``standard`` contains the supported SKOS/XL and adopted SKOS-Thes checks,
    not a claim of exhaustive standard conformance. ``target`` adds the
    adopted project constraints. Context-specific shapes in the latter need
    explicit targets supplied by the caller; see the package coverage guide.
    """
    if profile == "structure":
        from .structure import load_structure
        return load_structure()[0].serialize(format="turtle")
    if profile not in _PROFILES:
        raise ValueError("profile must be 'standard', 'target' or 'structure'")
    directory = files(__package__).joinpath("shapes")
    return "\n".join(
        directory.joinpath(name).read_text(encoding="utf-8")
        for name in _PROFILES[profile]
    )
