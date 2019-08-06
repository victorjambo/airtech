import redis
from os import getenv


class Config(object):
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL',
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

    # Celery configuration
    CELERY_BROKER_URL = getenv(
        'CELERY_BROKER_URL', default='redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = getenv(
        'CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')

    CACHE_TYPE = 'simple'
    CACHE_KEY_PREFIX = 'fcache'
    CACHE_REDIS_HOST = getenv('CACHE_REDIS_HOST', default='localhost')
    CACHE_REDIS_PORT = getenv('CACHE_REDIS_PORT', default='6379')
    CACHE_REDIS_URL = getenv('CACHE_REDIS_URL', default='redis://localhost:6379')

    JOBS = [{
        'id': 'periodic_email',
        'func': 'scheduler:scheduler',
        'trigger': 'interval',
        'hours': 24
    }]

    SCHEDULER_API_ENABLED = True


class ProductionConfig(Config):
    DATABASE_URL = getenv('DATABASE_URL')
    MAIL_SUPPRESS_SEND = False


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SUPPRESS_SEND = False


class TestingConfig(Config):
    CACHE_TYPE = 'simple'
    TESTING = True
    SQLALCHEMY_DATABASE_URL = getenv('TEST_DATABASE_URL',
                                     default='postgresql://localhost/airtech_test')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
