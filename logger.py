import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('pimicroclimate.log')
formatter = logging.Formatter('%(levelname)s %(asctime)s: %(message)s', "%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
