import os

app_dir = os.path.abspath(os.path.dirname(__file__))
base_path = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a#966really@!defew`232e9875654jklkjj#%key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # flask-security #
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha256'
    STORAGE = '/home/tornado/PycharmProjects/pythonProject/myBlog/app/static/images'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


class DevelopementConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or \
                              'mysql+mysqlconnector://bloger:a_L908zx_q@localhost/myblog'


class TestingConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or \
                              'mysql+mysqlconnector://bloger:a_L908zx_q@localhost/myblog'


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or \
                              'mysql+mysqlconnector://bloger:a_L908zx_q@localhost/myblog'