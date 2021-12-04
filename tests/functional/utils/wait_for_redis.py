import asyncio
import logging
import os
import sys
import time

import aioredis

sys.path.insert(1, os.path.realpath(os.path.pardir))
from functional.settings import REDIS_HOST, REDIS_PORT

logger = logging.getLogger(__name__)
log_format = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format)

bold_green = "\x1b[32;1m"
reset = "\x1b[0m"


async def main():
    redis_online = False
    while not redis_online:
        try:
            redis = await aioredis.create_redis((REDIS_HOST, REDIS_PORT))
            redis_answer = await redis.ping()
            if redis_answer == b'PONG':
                redis_online = True
                logger.debug('Redis reporting!'.join([bold_green, reset]))
        except:
            logger.exception('Waiting for redis...', exc_info=False)
            time.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
