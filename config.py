class DevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Mutie12791@127.0.0.1:5432/taskmanager'
    SECRET_KEY = 'some_random_string'
    JWT_SECRET_KEY = 'somerandomnstring'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP = 'task_manager.py'
    FLASK_ENV = 'development'


class ProductionConfig:
    DEBUG = False
