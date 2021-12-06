.PHONY: cp_env_test init init_debug init_local init_tests down test run

cp_env_test:
	cp .env.template .env

init:
	docker compose --env-file=.env up -d --build

init_debug:
	docker compose --env-file=.env up --build

init_local:
	docker compose --env-file=.env up elastic_test -d --build
	docker compose --env-file=.env up redis_test -d --build
	docker compose --env-file=.env up fastapi_test -d --build
	echo "\x1b[32;1m Эластик просит подождать секунд 10-20, пока он поднимется, спасибо!\x1b[0m"

init_tests:
	docker compose --env-file=.env up tests --build

down:
	docker compose down

test:
	pytest src

run: cp_env_test init_local init_tests down
