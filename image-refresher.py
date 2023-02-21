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

webhook_url = os.environ['SLACK_WEBHOOK_URL']

# Function setup
def refresh(images):
  client = docker.from_env()
  webhook = WebhookClient(webhook_url)

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
      logging.info("No refresh needed for image: {}".format(imagename))
  
  client.close()

images = []
for key, imagename in os.environ.items():
  if key.startswith('IMAGE'):
    images.append(imagename)

logging.info('Monitoring images: {}'.format(', '.join(images)))

# Task scheduling
# Get interval how often refresh() is called from environment variables.
interval = int(os.environ['REFRESHER_INTERVAL'])
schedule.every(interval).seconds.do(refresh, images=images)
logging.info('Scheduling interval every {} seconds'.format(interval))

# Loop so that the scheduling task keeps on running all time.
while True:
	schedule.run_pending()
	time.sleep(1)
