#!/usr/bin/env python

import docker
import logging
import os
import re
import schedule
import sys
import time

from slack_sdk.webhook import WebhookClient

formatter = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=formatter)

# Function setup
def refresh(images):
  client = docker.from_env()
  webhook = WebhookClient(os.environ['SLACK_WEBHOOK_URL'])

  for imagename in images:
    logging.info('Checking image for refresh: {}'.format(imagename))
    oldimage = client.images.get(imagename)
    newimage = client.images.pull(imagename)
    if newimage.id != oldimage.id:
      client.images.remove(oldimage.id)

      logging.info('Image refreshed: {}'.format(imagename))
      response = webhook.send(text='Image refreshed: {}'.format(imagename))
      if response.status_code == 200 and response.body == "ok":
        logging.info('Slack webhook successful')
      else:
        logging.error('Slack webhook unsuccesful, result: {}'.format(response.body))
    else:
      print("No refresh needed for image: {}".format(imagename))
  
  client.close()

images = []
for key, imagename in os.environ.items():
  if key.startswith('IMAGE'):
    images.append(imagename)

logging.info('Monitoring images: {}'.format(', '.join(images)))

# Task scheduling
# 15 minutes after every 2 hours refresh() is called.
schedule.every(2).hours.at(':15').do(refresh, images=images)
logging.info('Scheduling 15 minutes after every 2 hours')

# Loop so that the scheduling task keeps on running all time.
while True:
	schedule.run_pending()
	time.sleep(1)
