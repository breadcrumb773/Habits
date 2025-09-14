import logging
from pathlib import Path
from datetime import datetime
import random

prj_dir = Path(__file__).resolve().parents[1]

def conf_logger():
    logfile = f"{prj_dir}/logs/fastapi_{random.randint(10000,99999)}_{datetime.now()}.log"
    logging.basicConfig(format="{asctime}:{levelname}:{name}:{module}:{filename}:{funcName}:{message}",
                        style="{",
                        level=logging.DEBUG,
                        filename=str(logfile),
                        force=True,
                        datefmt="%Y:%m %d.%H.%M",
                        encoding="UTF-8",
                        filemode="a",)
conf_logger()
logging.getLogger(__name__)

def logger_dev(func):
    def wrapper(*args,**kwargs):
        logging.info(f"Start {func.__name__} with {args} and {kwargs}")
        res = func()
        logging.info(f"{func.__name__} return {res}")
        return res
    return wrapper