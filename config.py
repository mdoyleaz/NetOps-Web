# config.py
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    Common Configurations
    """
    # Flask-Security Encription Options
    SECURITY_PASSWORD_SALT = "sha512_crypt"
    # Flask-Security Email Options
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False
    # Flask-Security Enable Options
    SECURITY_CHANGEABLE = True
    # Flask-Security Templates
    SECURITY_LOGIN_USER_TEMPLATE = "login.html"

    SECURITY_TRACKABLE = True


class DevelopmentConfig(Config):
    """
    Development Configurations
    """
    DEBUG = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'netops_web_devel.db')


class ProductionConfig(Config):
    """
    Production Configurations
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqllite:///netops_web.db'


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
