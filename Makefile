clean:
	rm -rf build
	rm -rf dist
	rm -rf src/sayvai_tools/__pycache__
	rm -rf __pycache__
	rm -rf src/sayvai_tools.egg-info

build:
	apt-get update && apt-get install -y python3 python3-pip
	pip install --upgrade pip
	pip install poetry
	poetry build
	poetry install

install:
	pip install .

format:
	black src/

test:
	pytest tests/

