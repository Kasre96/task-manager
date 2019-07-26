from flask import Flask, jsonify
import connexion
from config import *
import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
import warnings
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

warnings.filterwarnings('ignore')

# connexion app
app = connexion.App(__name__, specification_dir='./api/')
flask_app = app.app

# config
app.app.config.from_object(DevelopmentConfig)

# Ensure instance path exists
try:
    os.makedirs(app.app.instance_path)
except OSError:
    pass

# Database
db = SQLAlchemy(flask_app)
mash = Marshmallow(flask_app)

from app import models

migrate = Migrate(flask_app, db)

# jwt
JWTManager(flask_app)

# Index page
@app.route('/')
def home():
    return 'Hello, World!'





