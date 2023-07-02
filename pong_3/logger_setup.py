import logging

FILENAME = "pong.log"
LOGFORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
DEFAULT_LEVEL = "logging.info"


logging.basicConfig(
    filename=FILENAME, level=logging.INFO, format=LOGFORMAT, datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("main")
