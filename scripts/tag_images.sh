#!/usr/bin/env bash
# strict mode
set -euo pipefail

VERSION=1.5.0-SNAPSHOT
DB_IMAGE=docker.getcollate.io/openmetadata/db:$VERSION
SERVER_IMAGE=docker.getcollate.io/openmetadata/server:$VERSION
INGESTION_IMAGE=docker.getcollate.io/openmetadata/ingestion:$VERSION

DB_CONTAINER=openmetadata_mysql
SERVER_CONTAINER=openmetadata_server
INGESTION_CONTAINER=openmetadata_ingestion

declare -A containers=(
    ["$DB_CONTAINER"]="$DB_IMAGE"
    ["$SERVER_CONTAINER"]="$SERVER_IMAGE"
    ["$INGESTION_CONTAINER"]="$INGESTION_IMAGE"
)

# Loop through the container-image pairs and run docker commit for each
for container in "${!containers[@]}"; do
    image=${containers[$container]}
    echo "Committing $container to $image..."
    docker commit "$container" "$image"
done

echo "Done committing images."