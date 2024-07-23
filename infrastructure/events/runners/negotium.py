from negotium import Negotium
from negotium.brokers import Redis

from config import logger, settings
from domain.events.runners.detached import DetachedRunner
from utils.importers import dynamic_import

negotium = Negotium(
    "deepchecks",
    Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        user=settings.redis_user,
        password=settings.redis_password,
    ),
)
negotium.start()


@negotium.task
def _runner(fname: str, *args, **kwargs):
    logger.info(f"Running {fname} with args {args} and kwargs {kwargs}")
    fn = dynamic_import(fname)
    return fn(*args, **kwargs)


class NegotiumDetachedRunner(DetachedRunner):
    def run(self, fname: str, *args, **kwargs):
        return _runner.delay(fname, *args, **kwargs)
