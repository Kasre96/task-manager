from flask import Flask, jsonify
import connexion
from config import *
import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

# connexion app
app = connexion.App(__name__, specification_dir='./api/')
flask_app = app.app

# config
app.app.config.from_object(DevelopmentConfig)

# Swagger Documentation
# app.add_api('swagger.yaml')

# Ensure instance path exists
try:
    os.makedirs(app.app.instance_path)
except OSError:
    pass

# Database
db = SQLAlchemy(flask_app)
mash = Marshmallow(flask_app)
migrate = Migrate(flask_app, db)

# Index page
@app.route('/')
def home():
    return 'Hello, World!'


from app import models


