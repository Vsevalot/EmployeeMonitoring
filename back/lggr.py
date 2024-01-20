import logging
import sys

logger = logging.getLogger(name="employee-directory-worker")
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
logger.setLevel("DEBUG")
