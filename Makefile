.PHONY: clean install update-deps test build full-build pylint run
.DEFAULT_GOAL: build

clean:
	@rm -rf .pytest_cache dist __pycache__ */__pycache__

install: clean
	@uv sync --all-extras

update-deps:
	@uv sync --upgrade --all-extras

test: install
	@uv run pytest

build: test
	@uv build

full-build: clean
	@docker image build -t image-refresher .

pylint:
	@uv run pylint image_refresher

run: install
	@REFRESHER_IMAGE_1=alpine:latest uv run python3 -m image_refresher.main
