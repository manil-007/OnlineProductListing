import openai
import logging

from pathlib import Path
from datetime import datetime as dt
from flask import jsonify, request, wrappers
from flask_cors import cross_origin
from tenacity import RetryError
from config.config import cfg, app
from utils.utils import create_output_file, completion_with_backoff
from gensim.summarization import keywords

logger = logging.getLogger(__name__)


@app.app.route("/ping", methods=["GET"])
def ping(username: str, suffix: str = None):
    resp = {"who": username, "at": dt.now().strftime("%Y-%m-%d, %H:%M:%S"), "suffix": suffix}

    pong = jsonify(resp)
    pong.status_code = 200

    return pong


def get_products(search_strings: str):
    stripped_search_strings = [s.strip() for s in search_strings]
    num_of_products = request.get_json()["num_of_products"]

    output = create_output_file(cfg["app"]["headless"],
                                None,
                                stripped_search_strings,
                                num_of_products
                                )
    return output


@app.app.route("/getproducts", methods=["POST"])
@cross_origin()
def get_products_for_search_phrases(username: str = "vatsaaa"):
    search_strings = request.get_json()["search_string"].split(";")
    output = get_products(search_strings)
    logger.info("get_products_for_search_phrases output : {a}".format(a=output))
    # Prepare response before returning
    response = jsonify(output)
    response.status_code = 200

    return response


def get_keywords(text: str):
    prompt = Path("config/prompt/prompt_for_extracting_keywords.txt").read_text() + text.lower()
    extractedKeywords = None
    logging.info("Generating keywords")
    if cfg["keywordsWithoutGPT"]:
        try:
            extractedKeywords = keywords(text, words=20, split=True, lemmatize=True)
        except:
            logging.error("Error Occured while extracting keywords using Gensim")
    else:
        try:
            response = completion_with_backoff(model="text-davinci-003",
                                               prompt="\"\"\"\n" + prompt + "\n\"\"\"",
                                               temperature=0.4,
                                               max_tokens=1024,
                                               top_p=1.0,
                                               frequency_penalty=0.0,
                                               presence_penalty=0.0,
                                               stop=["\"\"\""]
                                               )
            extractedKeywords = response["choices"][0]["text"].replace("\n", "").split(", ")
        except openai.OpenAIError as eoai:
            logger.error("OpenAIError : {a}".format(a=eoai.user_message))
        except RetryError as ere:
            logger.error("RetryError: A possible error OpenAI API error occurred!!")

    return extractedKeywords


@app.app.route("/getkeywords", methods=["POST"])
@cross_origin()
def get_keywords_for_text():
    text = request.get_json()["keywords_text"]
    keywords = get_keywords(text)
    return jsonify(keywords)


def build_text(keywords, flag):
    text = None
    if flag == "title":
        prompt = Path("config/prompt/prompt_for_building_description_text.txt").read_text() + ",".join(keywords)
        logger.info("Building Title using OpenAI")
    if flag == "description":
        prompt = Path("config/prompt/prompt_for_building_title_text.txt").read_text() + ",".join(keywords)
        logger.info("Building Description using OpenAI")
    try:
        response = completion_with_backoff(model="text-davinci-003",
                                           prompt="\"\"\"\n" + prompt + "\n\"\"\"",
                                           temperature=0.4,
                                           max_tokens=1024,
                                           top_p=1.0,
                                           frequency_penalty=0.0,
                                           presence_penalty=0.0,
                                           stop=["\"\"\""]
                                           )
        text = response["choices"][0]["text"].replace("\n", "")
    except openai.OpenAIError as eoai:
        logger.error("OpenAIError : {a}".format(a=eoai.user_message))
    except RetryError as ere:
        logger.error("RetryError: A possible error OpenAI API error occurred!!")
    else:
        response.status_code = 200
    return text


@app.app.route("/buildtext", methods=["POST"])
@cross_origin()
def build_text_from_keywords():
    keywords = request.get_json()
    text = build_text(keywords)
    return jsonify(text)


@app.app.route("/getlistings", methods=["POST"])
@cross_origin()
def get_listings():
    new_op = {}

    ## 1. Use search phrases for finding relevant products and their attributes 
    search_strings = request.get_json()["search_string"].split(";")
    products = get_products(search_strings)
    stripped_search_strings = [s.strip() for s in search_strings]

    ## 2. For each search phrase, we want the keywords from title and keywords from description
    ## TODO: Read title_keywords_required and description_keywords_required from commandline
    for sp in stripped_search_strings:
        new_op[sp] = {}
        new_op[sp]["title_keywords"] = []
        new_op[sp]["description_keywords"] = []

        for item in products[sp]:
            if item and item["title"] and cfg["app"]["title_keywords_required"]:
                new_op[sp]["title_keywords"] += get_keywords(item["title"])
                if item and item["brand"] and item["brand"] in new_op[sp]["title_keywords"]:
                    new_op[sp]["title_keywords"].remove(item["brand"])

            if item and item["description"] and cfg["app"]["description_keywords_required"]:
                new_op[sp]["description_keywords"] += get_keywords(item["description"])
                if item and item["brand"] and item["brand"] in new_op[sp]["description_keywords"]:
                    new_op[sp]["description_keywords"].remove(item["brand"])

        new_op[sp]["title_keywords"] = list(set(new_op[sp]["title_keywords"]))
        new_op[sp]["description_keywords"] = list(set(new_op[sp]["description_keywords"]))

        if len(new_op[sp]["title_keywords"]) > 0:
            new_op[sp]["title"] = build_text(new_op[sp]["title_keywords"], "title")

        if len(new_op[sp]["description_keywords"]) > 0:
            new_op[sp]["details"] = build_text(new_op[sp]["description_keywords"], "description")

        new_op[sp]["keywords"] = list(set(new_op[sp]["title_keywords"] + new_op[sp]["description_keywords"]))

    logger.debug("The generated listing data : {a}".format(a=new_op))
    return new_op
