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