from flask import jsonify
from datetime import datetime as dt

from config.config import cfg
from src.utils import create_output_file

def ping(username: str, suffix: str=None):
    resp = {"who": username, "at": dt.now().strftime("%Y-%m-%d, %H:%M:%S"), "suffix": suffix}

    pong = jsonify(resp)
    pong.status_code = 200

    return pong

def run(username: str):
    create_output_file(cfg["app"]["input_file_name"], cfg["app"]["output_file_name"], cfg["app"]["headless"])
