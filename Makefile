backend-run:
	cd backend && uvicorn app.main:app --reload

backend-local-environment:
	cd backend && make local-environment

backend-integration-tests:
	cd backend && make integration-tests

backend-run-docker:
	cd backend && make run-docker