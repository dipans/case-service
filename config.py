import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@postgres:5432/case_service"


#SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"