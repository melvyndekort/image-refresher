import os
import logging
import requests

logger = logging.getLogger(__name__)

if 'NTFY_URL' in os.environ and 'NTFY_TOKEN' in os.environ:
    NTFY_URL = os.environ['NTFY_URL']
    NTFY_TOKEN = os.environ['NTFY_TOKEN']
else:
    NTFY_URL = None
    NTFY_TOKEN = None
    logger.warning('ntfy URL or token not set')


def notify(message):
    if NTFY_URL and NTFY_TOKEN:
        headers = {'Authorization': f'Bearer {NTFY_TOKEN}'}
        response = requests.post(NTFY_URL, data=message, headers=headers)
        if response.status_code != 200:
            logging.error('ntfy notification failed, status: %s', response.status_code)
