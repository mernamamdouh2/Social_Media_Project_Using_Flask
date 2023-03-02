from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from flask_login import LoginManager

app = Flask (__name__)

app.config['SECRET_KEY'] = '92bb1cc78650ae59ae9b8266bac43d93'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
# from .models import *
migrate = Migrate(app, db, render_as_batch=True)
login_manager = LoginManager(app)

from socialMedia import routes
from socialMedia.routes import users
app.register_blueprint(users)