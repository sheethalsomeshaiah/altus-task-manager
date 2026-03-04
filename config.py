import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    PORT = 5001
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"

class StagingConfig(Config):
    DEBUG = False
    PORT = 5002
    SQLALCHEMY_DATABASE_URI = "sqlite:///staging.db"

class UATConfig(Config):
    DEBUG = False
    PORT = 5003
    SQLALCHEMY_DATABASE_URI = "sqlite:///uat.db"

class ProductionConfig(Config):
    DEBUG = False
    PORT = 5004
    SQLALCHEMY_DATABASE_URI = "sqlite:///prod.db"