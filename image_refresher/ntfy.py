"""Notification service via Apprise API."""
import os
import logging
import requests

logger = logging.getLogger(__name__)

if 'APPRISE_URL' in os.environ:
    APPRISE_URL = os.environ['APPRISE_URL']
    APPRISE_TAG = os.environ.get('APPRISE_TAG', 'homelab')
    APPRISE_KEY = os.environ.get('APPRISE_KEY', 'apprise')
else:
    APPRISE_URL = None
    APPRISE_TAG = None
    APPRISE_KEY = None
    logger.warning('Apprise URL not set')


def notify(message):
    """Send notification via Apprise API."""
    if APPRISE_URL:
        url = APPRISE_URL.rstrip('/')
        payload = {
            'body': message,
            'tag': APPRISE_TAG
        }
        try:
            response = requests.post(f'{url}/notify/{APPRISE_KEY}', json=payload, timeout=10)
            if response.status_code not in (200, 204):
                logger.error('Apprise notification failed, status: %s', response.status_code)
        except requests.RequestException as e:
            logger.error('Apprise notification failed: %s', e)
