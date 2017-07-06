""" Loads environment configuration """
import os
import dotenv

APP_ROOT = os.path.join(os.path.dirname(__file__), '')
dotenv_path = os.path.join(APP_ROOT, '.env')
dotenv.load(dotenv_path)


class Config(object):
    """ Defines config variables """

    DB_ENGINE = os.environ.get("DB_ENGINE")
    USERNAME = os.environ.get("USERNAME")
    PASSWORD = os.environ.get("PASSWORD")
    UNIQUE_TOKEN = os.environ.get("UNIQUE_TOKEN").encode('utf-8')
    AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
