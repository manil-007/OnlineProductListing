from flask import jsonify, request
from datetime import datetime as dt

from config.config import cfg
from src.utils import create_output_file

def ping(username: str, suffix: str=None):
    resp = {"who": username, "at": dt.now().strftime("%Y-%m-%d, %H:%M:%S"), "suffix": suffix}

    pong = jsonify(resp)
    pong.status_code = 200

    return pong

# Write Python function to tokenize a semicolon separated string

def run(username: str):
    create_output_file(cfg["app"]["input_file_name"], cfg["app"]["output_file_name"], cfg["app"]["headless"])

def run_post(username: str="vatsaaa"):
    search_strings = request.get_json()["search_string"].split(";")
    stripped_search_strings = [s.strip() for s in search_strings]
    num_of_products = request.get_json()["num_of_products"]

    create_output_file(cfg["app"]["input_file_name"], cfg["app"]["output_file_name"], cfg["app"]["headless"], stripped_search_strings, num_of_products)
