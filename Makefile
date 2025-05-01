STORAGE_YML=compose_files/postgres.yaml
APP_YML=compose_files/prod_app.yaml
ENV_FILE=.env
ENV_DEV=.env-dev
PYTHONPATH=src

export PYTHONPATH:=$(PYTHONPATH)


.PHONY: all
all: storages app

.PHONY: storages
storages: storage_up migrate

.PHONY: storage_up
storage_up:
	docker compose -f $(STORAGE_YML) --env-file=$(ENV_DEV) up -d

.PHONY: migrate
migrate:
	sleep 7
	alembic upgrade head


.PHONY: storages-down
storages-down:
	docker compose -f $(STORAGE_YML) --env-file=$(ENV_DEV) down
	
.PHONY: app-prod
app-prod:
	docker compose -f $(APP_YML) --env-file=$(ENV_FILE) up -d

.PHONY: app-prod-down
app-prod-down:
	docker compose -f $(APP_YML) --env-file=$(ENV_FILE) down

.PHONY: app-dev
app-dev:
	uvicorn --factory application.api.v1.app:get_app --reload

