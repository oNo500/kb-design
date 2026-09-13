#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p output/runtime
jar=output/runtime/jena-fuseki-server-6.2.0.jar
checksum=2c92c598e65ab69d99820052e05f4277ed1d77980a8845f87545ad35b71a76ee
if ! printf '%s  %s\n' "$checksum" "$jar" | shasum -a 256 -c - >/dev/null 2>&1; then
  curl --fail --location --retry 3 \
    https://repo.maven.apache.org/maven2/org/apache/jena/jena-fuseki-server/6.2.0/jena-fuseki-server-6.2.0.jar \
    -o "$jar.part"
  printf '%s  %s\n' "$checksum" "$jar.part" | shasum -a 256 -c -
  mv "$jar.part" "$jar"
fi
printf 'Fuseki 6.2.0 verified\n'
