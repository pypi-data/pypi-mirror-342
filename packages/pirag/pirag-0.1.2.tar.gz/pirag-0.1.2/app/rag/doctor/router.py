from argparse import Namespace
from loguru import logger

def route(args: Namespace):
    logger.info("Doctor route")
    print(args)

