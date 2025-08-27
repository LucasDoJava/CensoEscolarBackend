from flask import Flask
from flask_restful import Api
from flask_caching import Cache

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:%21%40LuizInacio008@localhost:5432/apicensoescolar"

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "pool_size": 10,
    "max_overflow": 20,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_REDIS_HOST"] = "localhost"
app.config["CACHE_REDIS_PORT"] = 6379
app.config["CACHE_REDIS_DB"] = 0
app.config["CACHE_REDIS_PASSWORD"] = None
app.config["CACHE_DEFAULT_TIMEOUT"] = 3600

cache = Cache(app)  

api = Api(app)
