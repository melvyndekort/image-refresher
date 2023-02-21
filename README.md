## Image refresher

This project updates specified docker images on the host system.
A notification is sent to a Slack channel when an image is successfully refreshed.

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

You have to configure the Slack Webhook URL:
```
-e REFRESHER_SLACK_WEBHOOK_URL=[URL]
```

### example
```
docker run \
  -e REFRESHER_INTERVAL=7200 \
  -e REFRESHER_SLACK_WEBHOOK_URL=https://hooks.slack.com/services/ABC123/ABC123/ABC123 \
  -e REFRESHER_IMAGE1=alpine:latest \
  -e REFRESHER_IMAGE2=busybox:latest \
  -e REFRESHER_IMAGE3=python:3.10-slim \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  melvyndekort/image-refresher
```
