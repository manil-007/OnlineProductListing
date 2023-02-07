import os
from pathlib import Path

from flask import jsonify, request
from datetime import datetime as dt
import openai

from config.config import cfg
from src.utils import create_output_file
from src.ProvisionOpenAI import ProvisionOpenAI

ProvisionOpenAI.set_api_key(cfg["openapi"]["secret"])

openai.api_key = ProvisionOpenAI.get_api_key()

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

def extract_keywords():
    text = request.get_json()["keywords_text"]
    prompt = Path("config/prompt.txt").read_text() + text

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )

    return jsonify(response)
