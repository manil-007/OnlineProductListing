from config import config
from src.utils import createOutputFile


if __name__ == '__main__':
    createOutputFile(config.inputFileName, config.outputFileName)
