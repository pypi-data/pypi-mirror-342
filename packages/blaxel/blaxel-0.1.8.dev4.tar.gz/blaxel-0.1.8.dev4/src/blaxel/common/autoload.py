
import logging

from ..client import client
from ..instrumentation.manager import telemetry_manager
from .settings import settings

logger = logging.getLogger("blaxel")

def autoload() -> None:
    client.with_base_url(settings.base_url)
    client.with_auth(settings.auth)
    logger.setLevel(settings.log_level)
    telemetry_manager.initialize(settings)