# Standard module imports
import getopt, sys

# Project module imports
from config.config import cfg
from utils.utils import create_output_file

def usage(file=sys.stdout):
    print("python app.py [-h | -u]", file=file)
    print("-h: run the tool in headless mode, this should help running on server")
    print("-u: prints this usage message")
    exit(-1)

def main(argumentList):
    options = "uh"
    long_options = ["Usage", "Headless"]
    headless_mode = False

    try:
        # Parse the arguments
        arguments, values = getopt.getopt(argumentList, options, long_options)

        for currentArgument, currentValue in arguments:
            if currentArgument in ("-u", "--Usage"):
                usage()
            elif currentArgument in ("-h", "--Headless"):
                headless_mode = True
    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))

    create_output_file(headless_mode
                       , cfg.get("app").get("input_file_name")
                       , None
                       , cfg.get("app").get("number_of_products"))


if __name__ == '__main__':
    main(argumentList=sys.argv[1:])

