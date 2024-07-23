APP_NAME := openmetadata-retention
APP_NAME_CAMMEL := openMetadataRetention

.PHONY: clean
clean:
	rm -rf target build docker-volume
	rm -rf src/metadata/community/applications/$(APP_NAME)/generated

.PHONY: all
all: target/$(APP_NAME).jar src/metadata/community/applications/$(APP_NAME)/generated/config.py down docker-compose

target/$(APP_NAME).jar:
	mkdir -p target
	jar cvf target/$(APP_NAME).jar -C src/ json/data/appMarketPlaceDefinition/ -C src/ assets/

src/metadata/community/applications/$(APP_NAME)/generated/config.py:
	python scripts/generate_config_model.py $(APP_NAME_CAMMEL)

docker-compose:
	docker compose up --build -d

down:
	docker compose down
