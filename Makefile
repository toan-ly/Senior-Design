### Pre-commit
precommit:
	pre-commit run --all-files

run-qdrant:
	docker run -p 6333:6333 qdrant/qdrant

docker-build-data:
	docker compose run --rm backend python -m scripts.build_data

### Backend Requirements
backend-req-export:
	uv pip compile pyproject.toml --output-file backend/requirements.txt --no-deps

### Development
backend:		
	uvicorn backend.app.main:app --reload --port 8000

frontend:
	streamlit run frontend/🏠_Home_page.py

run:
	uvicorn backend.app.main:app --reload --port 8000 & \
	streamlit run frontend/app.py

docker-up:
	docker compose up --build

docker-down:
	docker compose down
