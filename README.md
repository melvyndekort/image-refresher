# IMAGE-REFRESHER

## Badges

### Quality

[![Maintainability](https://api.codeclimate.com/v1/badges/71ecf3dfaf6ecf361640/maintainability)](https://codeclimate.com/github/melvyndekort/image-refresher/maintainability) [![codecov](https://codecov.io/gh/melvyndekort/image-refresher/graph/badge.svg?token=J3tLYcZWAT)](https://codecov.io/gh/melvyndekort/image-refresher)

### Workflows

![pipeline](https://github.com/melvyndekort/image-refresher/actions/workflows/pipeline.yml/badge.svg)

## Purpose

This project updates specified docker images on the host system.
A notification is sent to an ntfy server when an image is successfully refreshed.

The use case is to update images that have **NO** running containers.
If you want to update the image of running containers, use [Watchtower](https://hub.docker.com/r/containrrr/watchtower) instead.

## How to use

Specify environment variables for each image you'd like to have refreshed with

```
-e REFRESHER_IMAGE[number]=[repository:tag]
```

You have to configure the interval at which the scanner is scheduled:

```
-e REFRESHER_INTERVAL=[seconds]
```

You have to configure the ntfy server URL and token:

```
-e NTFY_URL=[URL]
-e NTFY_TOKEN=[TOKEN]
```

### Example

```
docker run \
  -e REFRESHER_INTERVAL=7200 \
  -e NTFY_URL=https://ntfy.example.com/topic \
  -e NTFY_TOKEN=tk_abc123 \
  -e REFRESHER_IMAGE1=alpine:latest \
  -e REFRESHER_IMAGE2=busybox:latest \
  -e REFRESHER_IMAGE3=python:3.10-slim \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  melvyndekort/image-refresher
```
