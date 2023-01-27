Mentioning the points as discussed:
1. For the data extraction, the user will input the data in two parts
   a. List of search products separated by semicolon
   b. Top 'n' products to be searched
2. After getting the user inputs, the api call will be made which will generate the data in the form of dict like
   {"searchedProductName": "Hair Oil", "GeneratedProductTitle": "To be generated", "GeneratedProductDescription": "To be generated", "keywords": "[list of    keywords]"}
3. At last the user will check and proceed with updating the listed product data or export the table data into excel sheel.

In the above second step, it will consist of mutiple steps:
1. The excel will be generated with the extracted product data.
2. The data will be grouped according to the searched product name.
3. The product title and description data will be combined to single data. 
4. The brand name will be extracted from the data and which will be removed from above combined data.
5. The noise and stop words will be removed from above data.
6. Using BERT algorithm, the keywords will be generated in the form of lists.
7. Now this list of keywords will be used to generate title and description using chatpGPT.

# Online Product Listing
This repo will be used for extracting the information from the similar products and will generate the best listing of the products.

## How to run
### Setup a virtual environment
`python3 -m venv venv` 
`pip install -r requierments.txt`

### Run as standalone module
`python app.py -h` # run in headless mode

OR

`python app.py -u` # prints usage

### Run as centralised API
`python main.py -h` # Run in headless mode - preferred

OR

`python main.py` # Run with browser - use for debugging

### Swagger UI
Swagger UI is available only in test / debug mode. Access URL - localhost:5000/api/v1/ui/ to test the API.

## References
- [Python REST APIs With Flask, Connexion, and SQLAlchemy](https://dassum.medium.com/python-rest-apis-with-flask-connexion-and-sqlalchemy-3c8c3292d9ce)
- [How to write README.md](https://medium.com/@saumya.ranjan/how-to-write-a-readme-md-file-markdown-file-20cb7cbcd6f)
- [Swagger YAML Editor](https://editor.swagger.io/)

