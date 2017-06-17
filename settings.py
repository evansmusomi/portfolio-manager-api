""" Loads environment configuration """
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Config(object):
    """ Defines config variables """

    DB_ENGINE = os.environ.get("DB_ENGINE")
    USERNAME = os.environ.get("USERNAME")
    PASSWORD = os.environ.get("PASSWORD")
