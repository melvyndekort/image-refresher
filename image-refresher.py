#!/usr/bin/env python

import docker
import os
import re
import schedule

from slack_sdk.webhook import WebhookClient

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

schedule.every(2).hours.at(':15').do(refresh)
