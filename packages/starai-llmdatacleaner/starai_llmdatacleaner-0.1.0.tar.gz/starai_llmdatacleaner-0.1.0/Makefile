test:
	uv run pytest -c pytest.ini -s

build:
	uv build

lint:
	uv run ruff check  --fix
	
format:
	uv run ruff format

install:
	pip install uv
	uv sync