#!/usr/bin/env python

import docker
import os
import re

client = docker.from_env()

for key, value in os.environ.items():
  if key.startswith('IMAGE'):
    oldimage = client.images.get(value)
    newimage = client.images.pull(value)
    if newimage.id != oldimage.id:
      client.images.remove(oldimage.id)
      print('Image {} refreshed'.format(value))
