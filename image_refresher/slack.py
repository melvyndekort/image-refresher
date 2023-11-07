import os
import logging
from slack_sdk.webhook import WebhookClient

logger = logging.getLogger(__name__)

if 'REFRESHER_SLACK_WEBHOOK_URL' in os.environ:
    WEBHOOK_URL = os.environ['REFRESHER_SLACK_WEBHOOK_URL']
    webhook = WebhookClient(WEBHOOK_URL)
else:
    webhook = None
    logger.warning('Slack webhook URL not set')


def notify(message):
    if webhook:
        response = webhook.send(text='Image refreshed: {}'.format(imagename))
        if response.status_code == 200 and response.body == "ok":
            logging.info('Slack webhook successful')
        else:
            logging.error('Slack webhook unsuccesful, result: {}'.format(response.body))
