## TODO
- [] shipping app icon
- [] UI configuration needs to be retrieved from API
- [] need to populate apps_marketplace from URL?
- [] permission model?
 

## Steps
- copy OpenMetadataRetention.json to OpenMetadata/openmetadata-ui/src/main/resources/ui/src/utils/ApplicationSchemas/
- run OpenMetadata/docker/run_local_docker.sh
- tag images
- docker compose up -d --build