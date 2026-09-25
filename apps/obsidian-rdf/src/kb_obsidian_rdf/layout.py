"""Application locations do not redefine resource types or content status."""

INDEXES = "00-indexes"
INBOX = "01-inbox"
PROJECTS = "10-projects"
AREAS = "20-areas"
RESOURCES = "30-resources"
ARCHIVES = "40-archives"
VOCABULARY = "90-vocabulary"
VIEWS = "91-views"
TEMPLATES = "92-templates"
ATTACHMENTS = "93-attachments"
PARA_ROOTS = (PROJECTS, AREAS, RESOURCES, ARCHIVES)
CONTENT_ROOTS = (INDEXES, *PARA_ROOTS)
KIND_DIRECTORIES = {
    "concepts": "concepts", "entities": "entities", "types": "document-types",
    "genres": "genres", "forms": "forms", "references": "references",
}
VAULT_DIRECTORIES = (INDEXES, INBOX, *PARA_ROOTS, VOCABULARY, VIEWS, TEMPLATES, ATTACHMENTS)
MANIFEST_VERSION = 4
