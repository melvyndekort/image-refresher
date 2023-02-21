#!/usr/bin/env python

import docker
import os
import re
import schedule
import time

from slack_sdk.webhook import WebhookClient

# Function setup
def refresh():
  client = docker.from_env()
  webhook = WebhookClient(os.environ['SLACK_WEBHOOK_URL'])

  for key, value in os.environ.items():
    if key.startswith('IMAGE'):
      oldimage = client.images.get(value)
      newimage = client.images.pull(value)
      if newimage.id != oldimage.id:
        client.images.remove(oldimage.id)
        
        response = webhook.send(text='Image {} refreshed'.format(value))
        assert response.status_code == 200
        assert response.body == "ok"
  
  client.close()

# Task scheduling
# 15 minutes after every 2 hours refresh() is called.
schedule.every(2).hours.at(':15').do(refresh)

# Loop so that the scheduling task keeps on running all time.
while True:
	schedule.run_pending()
	time.sleep(1)
