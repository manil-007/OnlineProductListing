import os
from pathlib import Path
from datetime import datetime as dt

from flask import jsonify, request
from tenacity import retry, stop_after_attempt, wait_random_exponential
import tiktoken
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
    prompt = Path("config/prompt_for_extracting_keywords.txt").read_text() + text

    response = completion_with_backoff(model="text-davinci-003", 
                                        prompt="\"\"\"\n"+prompt+"\n\"\"\"", 
                                        temperature=0.7, 
                                        max_tokens=1024,
                                        top_p=1.0,
                                        frequency_penalty=0.0,
                                        presence_penalty=0.0,
                                        stop=["\"\"\""]
                                    )
    
    return jsonify(response)

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff(**kwargs):
    return openai.Completion.create(**kwargs)

def keywords_to_text():
    keywords = request.get_json()
    prompt = Path("config/prompt_for_building_text.txt").read_text() + ",".join(keywords)

    response = completion_with_backoff(model="text-davinci-003", 
                                        prompt="\"\"\"\n"+prompt+"\n\"\"\"", 
                                        temperature=0.7, 
                                        max_tokens=1024,
                                        top_p=1.0,
                                        frequency_penalty=0.0,
                                        presence_penalty=0.0,
                                        stop=["\"\"\""]
                                    )
    
    return jsonify(response)