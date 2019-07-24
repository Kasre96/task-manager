class DevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Mutie12791@127.0.0.1:5432/task_manager'
    SECRET_KEY = 'some_random_string'
    JWT_SECRET_KEY = 'somerandomnstring'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig:
    DEBUG = False
