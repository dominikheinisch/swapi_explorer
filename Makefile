.PHONY: test

COMPOSE_PROJECT=backend

DEV?=false
ifeq ($(DEV),true)
	COMPOSE_FILE=compose-dev.yml
else
	COMPOSE_FILE=compose-prod.yml
endif

COMPOSE=docker-compose -p $(COMPOSE_PROJECT) -f $(COMPOSE_FILE)



build:
	$(COMPOSE) build

upd:
	$(COMPOSE) up -d

up:
	$(COMPOSE) up

down:
	$(COMPOSE) down

clean:
	$(COMPOSE) kill
	$(COMPOSE) rm --force

shell:
	docker exec -it $(COMPOSE_PROJECT)_$(COMPOSE_PROJECT)_1 /bin/sh

init: build up

logs:
	docker logs -f $(COMPOSE_PROJECT)_$(COMPOSE_PROJECT)_1

pytest:
	$(COMPOSE) run $(COMPOSE_PROJECT) /bin/bash -c " \
		./docker-entrypoint.sh && \
		pytest -v -s \
	"

bp: build pytest
