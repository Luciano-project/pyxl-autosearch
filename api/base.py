#from configs.config import Setup
from configs.settings import Setup
from configs.logging import setup_logging 
import logging
import sys, os, re

setup_logging()


# Adiciona o diretório pai ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

logger = logging.getLogger(__name__)

class SearchFile(Setup):
    def __init__(self, files:list[dict]):
        super().__init__()
        self.files = files
        self.return_values = []

    def search(self):
        '''Search files in path'''
        for root, dirs, files in os.walk(self.path, topdown=False):
            for name in files: 
                path = os.path.join(root, name)
                #print(path)
                self.check_path(name, path, self.files)
                if not len(self.files): return 0
        self.handle_not_found()

    def check_path(self, name_file, path, in_search:list[dict]):
        '''
        Check if file is in search list (in_search)
        '''
        for index_list, item in enumerate(in_search):
            if self.check_file_is_opened(path):
                self.handle_file_blocked(item, path)
                self.remove_found(index_list)

            elif self.search_in(item['filename'], name_file) and self.ignored_files_str(path)!=1 and self.check_extension(name_file):
                sheetname = item['sheetname'] if 'sheetname' in item else self.default_sheetname
                self.proc_load_list(path, name_file, index_list, sheetname = sheetname)
                self.remove_found(index_list)
                self.check_path(name_file, path, in_search)

    def proc_load_list(self, path, name_file, index_list, sheetname):
        """
        Here is where decision to processing the file is made, read or write. By using the parameter method: write, read.
        ~ This function will be overrided in the child class from views.
        """
        pass

    def remove_found(self, index_list): self.files.pop(index_list)  

    def search_in(self, file_name:str, haystack:str) -> int:
        '''Search if file_name is in haystack'''
        if file_name in [None, ""] or haystack in [None, ""]: return 0
        if re.search(f"{file_name}", haystack, re.IGNORECASE): return 1
        return 0

    def handle_not_found(self):
        '''Handle files not found'''
        for item in self.files:
            self.insert_data_response({
                                "coordinate": item["coordinate"],
                                "value": item["value"] if "value" in item else "Not found",
                                "path": "Not found",
                                "error": f"Filename: {item["filename"]} not found. Extensions expected: {self.extensions}",
                                })
            logger.error(f"File not found: {item['filename']} from the request:{item}. Extensions expected: {self.extensions}")
        return 0
    
    def handle_invalid_ref(self, requested_item):
        self.insert_data_response({"error": f"Invalid reference: {requested_item['coordinate']}", **requested_item})
        logger.error(f"Invalid reference: {requested_item}")
        return 1
    
    def handle_file_blocked(self, data_response, file_path:str):
        self.insert_data_response({**data_response, "error": f"File is blocked: {file_path}"})
        logger.error(f"File is blocked: {file_path}")
        return 1

    def insert_data_response(self, values:dict):
        '''insert data to the respose list'''
        self.return_values.append(values)

    def check_extension(self, file_name:str) -> int:
        '''Check if file has a valid extension'''
        for ext in self.extensions:
            if file_name.endswith(ext): return 1
        return 0
    
    def check_merged_cell(self, coordinate:str, ws_obj:object) -> int | str:
        '''Check if cell is merged and return the first cell of the merged cell'''
        try:
            for i in ws_obj.merged_cells:
                merged_splited = str(i).split(":")
                for cell in merged_splited:
                    if coordinate == cell: return merged_splited[0]
            return 0

        except Exception as e:
            logger.error(f"Error checking merged cell: {e}")
            return 0
    
    def check_file_is_opened(self, file_path:str) -> int:
        '''Check if file is opened'''
        try:
            with open(file_path, 'a'):
                pass
            return 0  # O arquivo não está bloqueado
        except PermissionError:
            return 1

#IGNORED ITENS METHODS
    def ignored_files_str(self, haystack):
        for item in self.ignored_str:
            if(self.search_in(item, haystack) == 1):
                return 1
        return 0

if __name__ == "__main__":
    search = SearchFile()
    search.search()