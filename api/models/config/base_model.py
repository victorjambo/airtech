"""Module for Base Model"""
from .database import db
from .model_operations import ModelOperations


class BaseModel(db.Model, ModelOperations):
    __abstract__ = True

    id = db.Column(db.String(), primary_key=True)
