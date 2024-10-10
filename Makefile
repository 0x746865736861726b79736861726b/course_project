DOCKER_COMPOSE = docker-compose
PROJECT_NAME = BLOCKCHAIN

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

build:
	$(DOCKER_COMPOSE) build --no-cache

restart:
	$(DOCKER_COMPOSE) down
	$(DOCKER_COMPOSE) up -d

logs:
	$(DOCKER_COMPOSE) logs -f

migrate:
	$(DOCKER_COMPOSE) run --rm web python src/manage.py migrate

makemigrations:
	$(DOCKER_COMPOSE) run --rm web python src/manage.py makemigrations

createsuperuser:
	$(DOCKER_COMPOSE) run --rm web python src/manage.py createsuperuser

shell:
	$(DOCKER_COMPOSE) run --rm web python src/manage.py shell

collectstatic:
	$(DOCKER_COMPOSE) run --rm web python src/manage.py collectstatic --noinput

clean:
	$(DOCKER_COMPOSE) down -v --remove-orphans

prune:
	docker system prune -af --volumes