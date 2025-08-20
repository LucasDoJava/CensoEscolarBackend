from helpers.app import app

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from flask_migrate import Migrate

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:12345@localhost:5432/apicensoescolar"
db.init_app(app)

migrate = Migrate(app, db)

#flask db init
#flask db migrate -m "mensagem"
#flask db upgrade