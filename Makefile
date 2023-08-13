venv:
	python3 -m venv venv
	./venv/bin/python3 -m pip install --upgrade pip


.PHONY: setup
setup: venv
	./venv/bin/pip3 install -r requirements.txt


.PHONY: format
format:
	./venv/bin/black gps2gtfs


.PHONY: lint
lint:
	./venv/bin/flake8 gps2gtfs
