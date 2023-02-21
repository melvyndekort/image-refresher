## Image refresher

This project updates specified docker images on the local system.

The use case is to update images that have **NO** running containers.
If you want to update the image of running containers, use [Watchtower](https://hub.docker.com/r/containrrr/watchtower) instead.

## How to use

Specify environment variables for each image you'd like to have refreshed with
```
-e IMAGE[number]=repository:tag
```

### example
```
docker run \
  -v /var/run/docker.sock:/var/run/docker.sock:ro
  -e IMAGE1=alpine:latest
  -e IMAGE2=busybox:latest
  -e IMAGE3=python:3.10-slim
  melvyndekort/image-refresher
```
