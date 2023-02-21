## Image refresher

This project updates specified docker images on the host system.
A notification is sent to a Slack channel when an image is successfully refreshed.

The use case is to update images that have **NO** running containers.
If you want to update the image of running containers, use [Watchtower](https://hub.docker.com/r/containrrr/watchtower) instead.

## How to use

Specify environment variables for each image you'd like to have refreshed with
```
-e IMAGE[number]=[repository:tag]
```

You have to configure the interval at which the scanner is scheduled:
```
-e REFRESHER_INTERVAL=[seconds]
```

You have to configure the Slack Webhook URL:
```
-e SLACK_WEBHOOK_URL=[URL]
```

### example
```
docker run \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -e REFRESHER_INTERVAL=7200 \
  -e SLACK_WEBHOOK_URL=https://hooks.slack.com/services/ABC123/ABC123/ABC123 \
  -e IMAGE1=alpine:latest \
  -e IMAGE2=busybox:latest \
  -e IMAGE3=python:3.10-slim \
  melvyndekort/image-refresher
```
