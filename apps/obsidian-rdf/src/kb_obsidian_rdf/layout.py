"""Application locations do not redefine resource types or content status."""

INBOX = "00-inbox"
PROJECTS = "01-projects"
AREAS = "02-areas"
RESOURCES = "03-resources"
ARCHIVES = "04-archives"
VOCABULARY = "05-vocabulary"
VIEWS = "06-views"
TEMPLATES = "07-templates"
ATTACHMENTS = "08-attachments"
PARA_ROOTS = (PROJECTS, AREAS, RESOURCES, ARCHIVES)
KIND_DIRECTORIES = {
    "concepts": "concepts", "entities": "entities", "types": "document-types",
    "genres": "genres", "forms": "forms", "references": "references",
}
VAULT_DIRECTORIES = (INBOX, *PARA_ROOTS, VOCABULARY, VIEWS, TEMPLATES, ATTACHMENTS)
MANIFEST_VERSION = 3
