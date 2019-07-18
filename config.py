from os import getenv


class Config(object):
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URI',
                                     default='postgresql://localhost/airtech')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = getenv('EMAIL_HOST_USER')
    MAIL_PASSWORD = getenv('EMAIL_HOST_PASSWORD')
    MAIL_SUPPRESS_SEND = True


class ProductionConfig(Config):
    DATABASE_URI = getenv('DATABASE_URI')
    MAIL_SUPPRESS_SEND = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = getenv('TEST_DATABASE_URI',
                                     default='postgresql://localhost/airtech_test')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
