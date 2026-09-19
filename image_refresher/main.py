"""Watches configured Docker images for updates and pulls/notifies on change."""

import logging
import os

import docker
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

from image_refresher import ntfy

FORMAT = '%(asctime)s %(levelname)s %(name)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)

scheduler = BlockingScheduler()
client = docker.from_env()


def get_image_id(image):
    """Return the local image ID for image, or None if it isn't present locally."""
    try:
        return client.images.get(image).id
    except docker.errors.APIError:
        return None


def refresh(image):
    """Pull image if new or changed, notifying on either case."""
    logging.info('Checking %s for refresh', image)
    old = get_image_id(image)

    if not old:
        client.images.pull(image)
        logging.info('New image pulled: %s', image)
        ntfy.notify(f'New image pulled: {image}')
    elif client.images.pull(image).id != old:
        client.images.remove(old)
        logging.info('Existing image refreshed: %s', image)
        ntfy.notify(f'Existing image refreshed: {image}')
    else:
        logging.info("No refresh needed for %s", image)


def main():
    """Schedule a periodic refresh job for each REFRESHER_IMAGE* env var."""
    if 'REFRESHER_INTERVAL' in os.environ:
        interval = int(os.environ['REFRESHER_INTERVAL'])
    else:
        interval = 7200
    logging.info('Interval was set to %d', interval)

    for k, v in os.environ.items():
        if k.startswith('REFRESHER_IMAGE'):
            refresh(v)
            scheduler.add_job(
                refresh,
                IntervalTrigger(seconds=interval),
                name=v,
                args=[v]
            )

    scheduler.start()


if __name__ == "__main__":
    main()
