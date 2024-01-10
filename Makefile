clean:
	rm -rf build
	rm -rf dist
	rm -rf src/sayvai_tools/__pycache__
	rm -rf __pycache__
	rm -rf src/sayvai_tools.egg-info

build:
	apt-get update && apt-get install libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev -y

install:
	pip install .

format:
	black src/