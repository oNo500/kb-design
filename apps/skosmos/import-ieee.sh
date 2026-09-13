#!/bin/sh
set -eu
cd "$(dirname "$0")"
source=../../packages/kb-vocab/output/ieee-2025-resolved/vocabulary.ttl
# PUT replaces only this preview graph. The source file is read-only input.
curl --fail --show-error --silent -X PUT \
  -H 'Content-Type: text/turtle' --data-binary "@$source" \
  'http://127.0.0.1:9030/skosmos/data?graph=urn%3Akb-design%3Apreview%3Aieee-2025'
printf '\n'
