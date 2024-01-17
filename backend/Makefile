
run:
	cd backend && uvicorn app.main:app --reload

run-docker:
	docker build -t workspace-api-local -f Dockerfile .
	docker run -e PORT=8000 --env-file .env	-p 8000:8000 --rm -it  workspace-api-local 

local-environment:
	docker compose -f docker-compose-run-local.yaml down
	docker compose -f docker-compose-run-local.yaml stop
	docker compose -f docker-compose-run-local.yaml build --force-rm
	docker compose -f docker-compose-run-local.yaml up

integration-tests:
	docker compose -f docker-compose-tests.yaml down --remove-orphans
	docker compose -f docker-compose-tests.yaml stop
	docker compose -f docker-compose-tests.yaml build --force-rm
	docker compose -f docker-compose-tests.yaml up --exit-code-from app-test