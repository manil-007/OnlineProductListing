from flask_cors import CORS
import connexion

cfg = {
    "app": {
        "host": "127.0.0.1",
        "port": 5432,
        "input_file_name": "config/test.xlsx",
        "output_file_name": "extractedData",
        "number_of_products": 10,
        "title_keywords_required": True,
        "description_keywords_required": True,
        "credentials": {
            "username": "admin",
            "password": "admin"
        }
    },
    "db": {
        "host": "localhost",
        "port": 27017,
        "database": "test",
        "credentials": {
            "username": "admin",
            "password": "admin"
        }
    },
    "openapi": {
        "secret": "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"
    }
}

app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")
CORS(app.app)
