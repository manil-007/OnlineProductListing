from pathlib import Path
from datetime import datetime as dt

from flask import jsonify, request, wrappers
from flask_cors import cross_origin

import openai
from tenacity import RetryError

from config.config import cfg, app
from utils.utils import create_output_file, completion_with_backoff, trimList, trimText

@app.app.route("/ping", methods=["GET"])
def ping(username: str, suffix: str = None):
    resp = {"who": username, "at": dt.now().strftime("%Y-%m-%d, %H:%M:%S"), "suffix": suffix}

    pong = jsonify(resp)
    pong.status_code = 200

    return pong

@app.app.route("/getproducts", methods=["POST"])
@cross_origin()
def get_products_for_search_phrases(username: str = "vatsaaa"):
    search_strings = request.get_json()["search_string"].split(";")
    stripped_search_strings = [s.strip() for s in search_strings]
    num_of_products = request.get_json()["num_of_products"]

    output = create_output_file(cfg["app"]["headless"],
                                None,
                                stripped_search_strings,
                                num_of_products
                                )

    # Prepare response before returning
    response = jsonify(output)
    response.status_code = 200

    return response

@app.app.route("/getkeywords", methods=["POST"])
@cross_origin()
def get_keywords_for_text():
    text = request.get_json()["keywords_text"]
    prompt = Path("config/prompt_for_extracting_keywords.txt").read_text() + text

    response = None
    
    try:
        response = completion_with_backoff(model="text-davinci-003",
                                       prompt="\"\"\"\n" + prompt + "\n\"\"\"",
                                       temperature=0.7,
                                       max_tokens=1024,
                                       top_p=1.0,
                                       frequency_penalty=0.0,
                                       presence_penalty=0.0,
                                       stop=["\"\"\""]
                                       )
    except openai.OpenAIError as eoai: 
        print("OpenAIError: " + eoai.user_message)
    except RetryError as ere:
        print("RetryError: A possible error OpenAI API error occurred!!")

    return jsonify(response)

@app.app.route("/buildtext", methods=["POST"])
@cross_origin()
def build_text_from_keywords():
    keywords = request.get_json()
    prompt = Path("config/prompt_for_building_description_text.txt").read_text() + ",".join(keywords)

    response = None

    try:
        response = completion_with_backoff(model="text-davinci-003",
                                       prompt="\"\"\"\n" + prompt + "\n\"\"\"",
                                       temperature=0.7,
                                       max_tokens=1024,
                                       top_p=1.0,
                                       frequency_penalty=0.0,
                                       presence_penalty=0.0,
                                       stop=["\"\"\""]
                                       )
    except openai.OpenAIError as eoai: 
        print("OpenAIError: " + eoai.user_message)
    except RetryError as ere:
        print("RetryError: A possible error OpenAI API error occurred!!")
    else:
        response.status_code = 200
    
    return jsonify(response)

@app.app.route("/getlistings", methods=["POST"])
@cross_origin()
def get_listings():
    new_op = {}

    ## 1. Use search phrases for finding relevant products and their attributes 
    search_strings = request.get_json()["search_string"].split(";")
    stripped_search_strings = [s.strip() for s in search_strings]
    num_of_products = request.get_json()["num_of_products"]

    output = create_output_file(cfg["app"]["headless"],
                                None,
                                stripped_search_strings,
                                num_of_products
                                )

    ## 2. For each search phrase, we want the keywords from title and keywords from description
    ## TODO: Make Title and Description keyword extraction based on a configuration flag passed
    ## If the title_keywords_required is TRUE then extract keywords from title
    ## Similarly, when desc_keywords_required flag is TRUE extract keywords from description
    for sp in stripped_search_strings:
        new_op[sp] = {}
        title_keywords = []
        description_keywords = []
        for item in output[sp]:
            # Being defensive, for instances where 'title' was not found
            if item and item["title"]:
                title_prompt = Path("config/prompt_for_extracting_keywords.txt").read_text() + item["title"].replace(item["brand"], "")

                try:
                    title_response = completion_with_backoff(model="text-davinci-003",
                                       prompt="\"\"\"\n" + title_prompt + "\n\"\"\"",
                                       temperature=0.4,
                                       max_tokens=1024,
                                       top_p=1.0,
                                       frequency_penalty=0.0,
                                       presence_penalty=0.0,
                                       stop=["\"\"\""]
                                       )
                    title_keywords += (title_response["choices"][0]["text"].replace(item["brand"], "")).split(",")
                except openai.OpenAIError as eoai: 
                    print("OpenAIError: " + eoai.user_message)
                except RetryError as ere:
                    print("RetryError: A possible error OpenAI API error occurred!!")

            # Being defensive, for instances where 'description' was not found
            if item and item["description"]:
                description_prompt = Path("config/prompt_for_extracting_keywords.txt").read_text() + item["description"].replace(item["brand"], "")

                try:
                    description_response = completion_with_backoff(model="text-davinci-003",
                                       prompt="\"\"\"\n" + description_prompt + "\n\"\"\"",
                                       temperature=0.4,
                                       max_tokens=1024,
                                       top_p=1.0,
                                       frequency_penalty=0.0,
                                       presence_penalty=0.0,
                                       stop=["\"\"\""]
                                       )
                    description_keywords += (description_response["choices"][0]["text"].replace(item["brand"], "")).split(",")
                except openai.OpenAIError as eoai: 
                    print("OpenAIError: " + eoai.user_message)
                except RetryError as ere:
                    print("RetryError: A possible error OpenAI API error occurred!!")

        new_op[sp]["title_keywords"] = trimList(list(set(title_keywords)))
        new_op[sp]["description_keywords"] = trimList(list(set(description_keywords)))

        if len(new_op[sp]["title_keywords"]) > 0:
            try:
                suggested_title_prompt = Path("config/prompt_for_building_title_text.txt").read_text() + str(
                    new_op[sp]["title_keywords"])
                suggested_title_response = completion_with_backoff(model="text-davinci-003",
                                                        prompt="\"\"\"\n" + suggested_title_prompt + "\n\"\"\"",
                                                        temperature=0.4,
                                                        max_tokens=1024,
                                                        top_p=1.0,
                                                        frequency_penalty=0.0,
                                                        presence_penalty=0.0,
                                                        stop=["\"\"\""]
                                                        )
                new_op[sp]["title"] = trimText(suggested_title_response.choices[0].text).replace(item["brand"], "")
            except openai.OpenAIError as eoai:
                print("OpenAIError: " + eoai.user_message)
            except RetryError as ere:
                print("RetryError: A possible error OpenAI API error occurred!!")
        else:
            new_op[sp]["title"] = ""

        if len(new_op[sp]["description_keywords"]) > 0:
            try:
                suggested_description_prompt = Path(
                    "config/prompt_for_building_description_text.txt").read_text() + str(
                    new_op[sp]["description_keywords"])
                suggested_description_response = completion_with_backoff(model="text-davinci-003",
                                                                prompt="\"\"\"\n" + suggested_description_prompt + "\n\"\"\"",
                                                                temperature=0.4,
                                                                max_tokens=1024,
                                                                top_p=1.0,
                                                                frequency_penalty=0.0,
                                                                presence_penalty=0.0,
                                                                stop=["\"\"\""]
                                                                )
                new_op[sp]["details"] = trimText(suggested_description_response.choices[0].text).replace(item["brand"], "")
            except openai.OpenAIError as eoai:
                print("OpenAIError: " + eoai.user_message)
            except RetryError as ere:
                print("RetryError: A possible error OpenAI API error occurred!!")
        else:
            new_op[sp]["details"] = ""

        new_op[sp]["keywords"] = list(set(trimList(new_op[sp]["title_keywords"] + new_op[sp]["description_keywords"])))
        print("Title Keywords:", new_op[sp]["keywords"])

    ## 4. We need to ensure that the dictionary is mapping correctly as that on UI
    
    ## 5. Call tested functions built and tested instead of the spread out code
    
    return new_op
