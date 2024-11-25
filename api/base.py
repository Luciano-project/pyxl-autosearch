#from configs.config import Setup
import sys, os, re

# Adiciona o diretório pai ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from configs.config import Setup


class SearchFile(Setup):
    def __init__(self, files = [{"namefile":"2409999", "coordenate":"C1", "value":""}, {"namefile":"2409999", "coordenate":"C1", "value":"Olá mundo"}]):
        super().__init__()
        self.files = files

    def search(self):
        '''Search files in path'''
        for root, dirs, files in os.walk(self.path, topdown=False):
            for name in files:
                path = os.path.join(root, name)
                #print(path)
                self.check_path(name, path, self.files)
                if not len(self.files): return 0

    def check_path(self, name_file, path, in_search:list[dict]):
        '''
        Check if file is in search list (in_search)
        '''
        for index_list, item in enumerate(in_search):
            if self.search_in(item['namefile'], name_file) and self.ignored_files_str(path)!=1:
                self.proc_load_list(path, name_file, index_list)
                self.remove_found(index_list)
                self.check_path(name_file, path, in_search)

    def proc_load_list(self, path, name_file, index_list):
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

#IGNORED ITENS METHODS
    def ignored_files_str(self, haystack):
        for item in self.ignored_str:
            if(self.search_in(item, haystack) == 1):
                return 1
        return 0

    def not_substr(self, needle, haystack):
        values_fmt1 = haystack.replace("_"," ")
        values_list = values_fmt1.split(" ")
        needle = needle.upper()
        for item in values_list:
            if needle == item:
                return 1
        return 0

if __name__ == "__main__":
    search = SearchFile()
    search.search()
