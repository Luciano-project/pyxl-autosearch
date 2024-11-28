import os
#import mysql.connector
DEBUG = True


class Setup:
    def __init__(self):
        self.path = rf"C:\Users\lucia\Projects\python\tests" #Path de procura
        self.base_str_find = [] # STRINGS MUST BE INCLUDED IN NAME FILE
        self.ignored_str = []
        self.default_sheetname = "test"
        self.default_savepath = rf"C:\Users\lucia\Projects\python\tests"
