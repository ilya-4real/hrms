STORAGE_YML=compose_files/postgres.yaml
ENV_FILE=.env
PYTHONPATH=src

export PYTHONPATH:=$(PYTHONPATH)


.PHONY: all
all: storages app

.PHONY: storages
storages: storage_up migrate

.PHONY: storage_up
storage_up:
	docker compose -f $(STORAGE_YML) --env-file=$(ENV_FILE) up -d

.PHONY: migrate
migrate:
	sleep 7
	alembic upgrade head

.PHONY: storages-down
storages-down:
	docker compose -f $(STORAGE_YML) --env-file=$(ENV_FILE) down
	

.PHONY: app
app:
	uvicorn --factory application.api.v1.app:get_app --reload

