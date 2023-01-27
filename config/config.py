from flask_cors import CORS
import connexion

cfg = {
    "app": {
        "host": "localhost",
        "port": 5000,
        "input_file_name": "config/test.xlsx",
        "output_file_name": "extractedData",
        "number_of_products": 10,
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
    }
}

app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")

CORS(app.app, origins="*", allow_headers="*")
