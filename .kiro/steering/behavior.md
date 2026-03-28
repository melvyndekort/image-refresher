# image-refresher

> For global standards, way-of-workings, and pre-commit checklist, see `~/.kiro/steering/behavior.md`

## Role

Python developer and DevOps engineer.

## What This Does

Periodically checks for updated Docker images and pulls them on the host. Uses Docker SDK and APScheduler. Configured via environment variables (`REFRESHER_IMAGE_1`, `REFRESHER_IMAGE_2`, etc.).

## Repository Structure

- `image_refresher/` — Application source
- `tests/` — Test suite
- `Dockerfile` — Multi-stage Alpine build
- `Makefile` — `install`, `test`, `lint`, `format` (pylint), `build`, `full-build`, `run`

## Deployment

- Container image: `ghcr.io/melvyndekort/image-refresher:latest`
- Runs on homelab Docker via Portainer

## Related Repositories

- `~/src/melvyndekort/homelab` — Docker Compose stack that runs this container
