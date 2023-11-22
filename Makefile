.PHONY: clean install update-deps test build full-build pylint run
.DEFAULT_GOAL: build

clean:
	@rm -rf .pytest_cache dist __pycache__ */__pycache__

install: clean
	@poetry install

update-deps:
	@poetry update

test: install
	@poetry run pytest

build: test
	@poetry build

full-build: clean
	@docker image build -t image-refresher .

pylint:
	@poetry run pylint image_refresher

run: install
	@REFRESHER_IMAGE_1=alpine:latest poetry run python3 -m image_refresher.main
