#!/usr/bin/env python3

import getopt, logging, sys
import logging.config

from waitress import serve
from datetime import datetime
from config.config import app, cfg


LOG_CONFIG_DIR = "./config/logging"
LOG_DIR = "./logs"


def setup_logging(verbose):
    env = "prod"
    if verbose:
        env = "dev"
    log_configs = {"dev": "dev.ini", "prod": "prod.ini"}
    config = log_configs.get(env, "logging.prod.ini")
    config_path = "/".join([LOG_CONFIG_DIR, config])

    timestamp = datetime.now().strftime("%Y%m%d-%H_%M_%S")

    logging.config.fileConfig(config_path,
                              disable_existing_loggers=False,
                              defaults={"logfilename": f"{LOG_DIR}/{timestamp}.log"}
                            )


def usage(prog_name):
    print("Usage: \npython3 " + prog_name + " -u: prints this usage message" + "\nor")
    print("python3 " + prog_name + " -h: run the tool in headless mode, this should help running on server")


def process_args(args):
    options = "uhvw"
    long_options = ["Usage", "Headless", "Verbose", "WithoutGPT"]
    headless_mode = False
    verbose_mode = False
    keywordsWithoutGPT = False

    try:
        # Parse the arguments
        arguments, values = getopt.getopt(args[1:], options, long_options)

        for currentArgument, currentValue in arguments:
            if currentArgument in ("-u", "--Usage"):
                usage(args[0])
                exit(-2)
            elif currentArgument in ("-h", "--Headless"):
                headless_mode = True
            elif currentArgument in ("-v", "--Verbose"):
                verbose_mode = True
            elif currentArgument in ("-w", "--WithoutGPT"):
                keywordsWithoutGPT = True
    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))
        
    cfg["app"]["headless"] = headless_mode
    cfg["verbose"] = verbose_mode
    cfg["keywordsWithoutGPT"] = keywordsWithoutGPT


if __name__=='__main__':
    process_args(args=sys.argv)
    setup_logging(cfg["verbose"])
    logger = logging.getLogger(__name__)

    logger.info("Program started")

    serve(app=app, host=cfg["app"]["host"], port=cfg["app"]["port"])
    logger.info("Program Finished")
