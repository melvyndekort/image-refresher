import os
import logging
import docker
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

FORMAT = '%(asctime)s %(levelname)s %(name)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)

from image_refresher import ntfy

scheduler = BlockingScheduler()
client = docker.from_env()


def get_image_id(image):
    try:
        return client.images.get(image).id
    except docker.errors.APIError:
        return None


def refresh(image):
    logging.info('Checking %s for refresh', image)
    old = get_image_id(image)

    if not old:
        client.images.pull(image)
        logging.info('New image pulled: %s', image)
    elif client.images.pull(image).id != old:
        client.images.remove(old)
        logging.info('Existing image refreshed: %s', image)
        ntfy.notify(f'Existing image refreshed: {image}')
    else:
        logging.info("No refresh needed for %s", image)


def main():
    if 'REFRESHER_INTERVAL' in os.environ:
        INTERVAL = int(os.environ['REFRESHER_INTERVAL'])
    else:
        INTERVAL = 7200
    logging.info('Interval was set to %d', INTERVAL)

    for k, v in os.environ.items():
        if k.startswith('REFRESHER_IMAGE'):
            refresh(v)
            scheduler.add_job(
                refresh,
                IntervalTrigger(seconds=INTERVAL),
                name=v,
                args=[v]
            )

    scheduler.start()


if __name__ == "__main__":
    main()
