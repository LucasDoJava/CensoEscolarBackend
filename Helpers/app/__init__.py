from flask import Flask
from flask_restful import Api

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:%21%40LuizInacio008@localhost:5432/apicensoescolar"

api = Api(app)