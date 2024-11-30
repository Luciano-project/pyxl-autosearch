import os
from dotenv import load_dotenv
#import mysql.connector

load_dotenv("../.env")

class Setup:
    def __init__(self):
        self.path = os.getenv("SEARCH_PATH")
        self.base_str_find = [] # STRINGS MUST BE INCLUDED IN NAME FILE
        self.ignored_str = []
        self.default_sheetname = "test"
        self.default_savepath = os.getenv("DEFAULT_SAVEPATH")
