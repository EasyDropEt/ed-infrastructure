.phony: docker.build docker.run docker.build.quite run build upload

run:
	@echo "Make: Running the package..."
	@python src/server.py

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
