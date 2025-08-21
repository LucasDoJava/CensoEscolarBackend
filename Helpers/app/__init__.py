from flask import Flask
from flask_restful import Api

app = Flask(__name__)

# note o "+psycopg2"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:2005@localhost:5432/apicensoescolar"

api = Api(app)
