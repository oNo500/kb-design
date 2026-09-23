"""Application locations do not redefine resource types or content status."""

PARA_ROOTS = ("projects", "areas", "resources", "archives")
VOCABULARY = "vocabulary"
KIND_DIRECTORIES = {
    "concepts": "concepts", "entities": "entities", "types": "document-types",
    "genres": "genres", "forms": "forms", "references": "references",
}
VAULT_DIRECTORIES = ("inbox", *PARA_ROOTS, VOCABULARY, "views", "templates", "attachments")
MANIFEST_VERSION = 2
