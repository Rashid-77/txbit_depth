import logging
from datetime import datetime
from functools import lru_cache
from pathlib import Path



@lru_cache
def get_logger(module_name, folder, fname):
    logger = logging.getLogger(module_name)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    Path(f'logs/{folder}').mkdir(parents=True, exist_ok=True)
    fh = logging.FileHandler(f'logs/{folder}/{datetime.now():%Y-%m-%d}-{fname}.log')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.setLevel(logging.DEBUG)
    return logger



