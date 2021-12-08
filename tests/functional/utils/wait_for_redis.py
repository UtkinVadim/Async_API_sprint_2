import asyncio
import logging
import sys

import aioredis
import backoff
from functional.settings import REDIS_HOST, REDIS_PORT

logger = logging.getLogger(__name__)
log_format = "%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s"
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=log_format)

bold_green = "\x1b[32;1m"
reset = "\x1b[0m"


def backoff_handler(_details):
    logger.exception("Waiting for redis...", exc_info=False)


@backoff.on_exception(backoff.expo, ConnectionRefusedError, max_time=300, max_tries=15, on_backoff=backoff_handler)
async def main():
    redis = await aioredis.create_redis((REDIS_HOST, REDIS_PORT))
    redis_answer = await redis.ping()
    if redis_answer == b"PONG":
        logger.info("Redis reporting!".join([bold_green, reset]))
        redis.close()
        await redis.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
