import logging
from logging import Formatter, Handler, Logger

logger: Logger = logging.getLogger(__name__)

handler: Handler = logging.StreamHandler()
handler.setLevel(logging.WARNING)

format: Formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
handler.setFormatter(format)

logger.addHandler(handler)

# logger.warning('This is a warning')
# logger.error('This is an error')
