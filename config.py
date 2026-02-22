import os

class Config:
    SECRET_KEY = "supersecretkey"
    SQLALCHEMY_DATABASE_URI = "sqlite:///lms.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False