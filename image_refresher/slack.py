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
        response = webhook.send(text=message)
        if response.status_code != 200 or response.body != "ok":
            logging.error('Slack webhook unsuccesful, result: %s', response.body)
