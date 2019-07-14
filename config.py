from os import getenv


class Config(object):
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URI',
                                     default='postgresql://localhost/airtech')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    DATABASE_URI = getenv('DATABASE_URI')


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
