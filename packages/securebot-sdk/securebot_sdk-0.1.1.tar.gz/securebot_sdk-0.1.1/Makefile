.PHONY: setup lint test build clean

setup:
	uv venv
	uv pip install -e ".[dev]"

pre-commit:
	uv pip install -e ".[dev]"
	pre-commit install
	pre-commit run --all-files

test:
	pytest

build:
	python -m build

clean:
	rm -rf dist/ build/ *.egg-info
