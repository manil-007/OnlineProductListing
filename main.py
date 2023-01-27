import getopt, sys
from waitress import serve

from config.config import app, cfg

def usage(prog_name):
    print("Usage: \npython3 " + prog_name + " -u: prints this usage message" + "\nor")
    print("python3 " + prog_name + " -h: run the tool in headless mode, this should help running on server")

def process_args(args):
    options = "uh"
    long_options = ["Usage", "Headless"]
    headless_mode = False

    try:
        # Parse the arguments
        arguments, values = getopt.getopt(args[1:], options, long_options)

        for currentArgument, currentValue in arguments:
            if currentArgument in ("-u", "--Usage"):
                usage(args[0])
                exit(-2)
            elif currentArgument in ("-h", "--Headless"):
                headless_mode = True
    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))
        
    cfg["app"]["headless"] = headless_mode

if __name__=='__main__':
    process_args(args=sys.argv)

    serve(app=app, host=cfg["app"]["host"], port=cfg["app"]["port"])