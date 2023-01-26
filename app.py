# Standard module imports
import getopt, sys

# Project imports
from config import config
from src.utils import createOutputFile

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

    createOutputFile(config.inputFileName, config.outputFileName, headless=headless_mode)

if __name__ == '__main__':
    main(argumentList=sys.argv[1:])

