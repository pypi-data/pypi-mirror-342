import logging
import sys

knit_logger = logging.getLogger(__name__)
knit_logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("Knit : %(asctime)s: %(message)s")
stream_handler.setFormatter(log_formatter)
knit_logger.addHandler(stream_handler)
