from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

class JsonFile:
    def __init__(self, name=fr"config.json"):
        self.filename=name #relative path
        self.filedata=""

    def open_json_file(self):
        try:
            with open(self.filename, encoding= 'utf-8') as file: #open file
                self.filedata = json.load(file, strict=True)
                logger.info(f'JSON File: {self.filename} opened.')
            return 0
        except Exception as e:
            print(e)
            logger.error(f'{e} at JsonFile.open_json_file()')
            return 1
    
    """def search_corresp(self, desc):
        for tube in self.filedata["tubos"]:
            if str(tube["tipo"]).upper()==desc.upper():
                return str(tube["codigo"]).upper()"""

    ## Development functions
    def print_file(self): print(self.filedata)

CONFIG = JsonFile()

class ConfigSearchDefinitions:
    def __init__(self):
        self.filedata=CONFIG.filedata

        #Files definitions
        self.definitions_field = self.filedata["file_definition"]
        self.sheetname=self.definitions_field["sheetname"]
        self.column_start_key=self.definitions_field["column_start_key"]
        self.column_start_value=self.definitions_field["column_start_value"]
        self.column_title=self.definitions_field["column_title"]
        self.row_start=self.definitions_field["row_start"]
        self.ignore_terms_in_key=self.definitions_field["ignore_terms_in_key"]
        self.metadata_fields=self.definitions_field["metadata_fields"]
        self.extensions_file = self.filedata["general_config"]["extensions_file"]

    
    #Field Definitions
    def get_sheetname(self): return self.sheetname
    def get_column_start_key(self): return self.column_start_key
    def get_column_start_value(self): return self.column_start_value
    def get_column_title(self): return self.column_title
    def get_row_start(self): return self.row_start
    def get_ignore_terms_in_key(self): return self.ignore_terms_in_key
    def get_metadata_fields(self): return self.metadata_fields


class ConfigFromFile:
    def __init__(self):
        self.filedata=CONFIG.filedata

        #General config
        self.config_field = self.filedata["general_config"]
        self.server_path = self.config_field["server_path"]
        self.search_dir = self.config_field["search_dir"]
        self.extensions_file = self.config_field["extensions_file"]
        self.endpoint_compare = self.config_field["endpoint_compare_file_in_json"]

    #General Functions
    def get_search_dir(self): return self.search_dir
    def get_server_path(self): return self.server_path
    def get_extensions_file(self): return self.extensions_file
    def get_endpoint_compare(self): return self.endpoint_compare
    

if __name__ == "__main__":
    infor = ConfigFromFile().get_search_dir()
    print(infor)