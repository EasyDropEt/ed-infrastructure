.phony: export_deps docker.build docker.run docker.build.quite run build upload

export_deps:
	@echo "Make: Exporting dependencies..."
	@poetry export --without-hashes --format=requirements.txt > requirements.txt

test:
	@echo "Make: Running tests..."
	@python -m pytest .

test.coverage:
	@echo "Make: Running tests with coverage..."
	@python -m pytest --cov=src --cov-report=term-missing .

docker.build:
	@echo "Make: Building a docker image... (Might be minutes)"
	@docker build -t domain_model:dev .

docker.build.quite:
	@echo "Make: Building a docker image... (Might be minutes)"
	@docker build -q -t domain_model:dev .

docker.run: docker.build.quite
	@echo "Make: Running docker container..."
	@docker run -p 8000:8000 -v $(PWD):/app domain_model:dev run

build:
	@echo "Make: Building package..."
	@python3 -m pip install build
	@python3 -m build --wheel

upload: build
	@echo "Make: Uploading package..."
	@twine upload dist/*
	@rm -rf dist
	@rm -rf build
	@rm -rf src/*.egg-info
	@rm -rf .pytest_cache
	@rm -rf .coverage
	@rm -rf .eggs
	@rm -rf .tox
