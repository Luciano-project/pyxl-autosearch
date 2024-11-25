
#from configs.config import Setup
import sys, os, re

# Adiciona o diretório pai ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from configs.config import Setup
from middlewares.openxl_files import OpenxlFiles


class SearchFile(Setup):
    def __init__(self, files = [{"namefile":"2409999", "coordenate":"C1", "value":""}, {"namefile":"2409999", "coordenate":"C1", "value":"Olá mundo"}]):
        super().__init__()
        self.files = files
        self.openxl_files = OpenxlFiles

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
        for count, item in enumerate(in_search):
            if self.search_in(item['namefile'], name_file) and self.ignored_files_str(path)!=1:
                self.proc_load_list(path, name_file, count)
                self.check_path(name_file, path, in_search)


    def proc_load_list(self, path, name, count, method:str):
        """
        Here is where decision to processing the file is made, read or write. By using the parameter method: write, read.
        """
        if method == "write": self.write_file(path, name)
        elif method == "read": self.read_file(path, name)
        method(path, name, count)
        
        if self.process_xl(path, self.files[count]["coordenate"], self.files[count]["value"]): pass
            #self.save_file_status(path, self.files[count][1], self.files[count][0])       
        self.remove_found(count)

    def remove_found(self, count): self.files.pop(count)  

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

    def save_file_status(self, path, of, nbr, e = ""):
        #self.status_file.append({"of" : f"{of}", "peca" : f"{nbr}", "caminho" : f"{path}","log":f"{e}"})
        if e!="":
            #conec.add_record(of, nbr, path, str(e))
            #self.connection_on=1
            pass

if __name__ == "__main__":
    search = SearchFile()
    search.search()
