.PHONY: clean install test build full-build pylint run
.DEFAULT_GOAL: build

clean:
	@rm -rf .pytest_cache dist __pycache__ */__pycache__

install:
	@poetry install

test: install
	@poetry run pytest

build: test
	@poetry build

full-build:
	@docker image build -t image-refresher .

pylint:
	@poetry run pylint image_refresher

run:
	@REFRESHER_IMAGE_1=alpine:latest poetry run python3 -m image_refresher.main