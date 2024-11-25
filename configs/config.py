import os
#import mysql.connector
DEBUG = True
SECRET_KEY = 'your_secret_key'

class Setup:
    def __init__(self):
        self.path = rf"C:\Users\lucia\Projects\python\tests" #Path de procura
        self.root_dir = "PROJECTOS CLIENTES"
        self.base_str_find = [] # STRINGS MUST BE INCLUDED IN NAME FILE


        #for list status
"""        self.pending_path=rf"{self.server_path}\jet 3\LISTAS"
        self.loaded_path=rf"{self.server_path}\jet 3\LISTAS\Tratados"
        self.repeated_path=rf"{self.server_path}\jet 3\LISTAS\OFsRepetidas"
        self.rejected_path=rf"{self.server_path}\jet 3\LISTAS\FicheirosRejeitados"
        self.invalid_path=rf"{self.server_path}\jet 3\LISTAS\FicheirosInvalidos"
"""
