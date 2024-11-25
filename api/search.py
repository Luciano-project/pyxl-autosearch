
#from configs.config import Setup
import os, re


class Setup:
    def __init__(self):
        self.path = rf"C:\Users\lucia\Projects\python\tests" #Path de procura
        self.root_dir = "PROJECTOS CLIENTES"
        self.base_str_find = [] # STRINGS MUST BE INCLUDED IN NAME FILE
        self.ignored_str = ["~$"]



class SearchFile(Setup):
    def __init__(self, files = [{"namefile":"2301999", "coodenate":"C1", "value":""}, {"namefile":"2301999", "coodenate":"C1", "value":"Olá mundo"}]):
        super().__init__()
        self.files = files

    def search(self):
        '''Search files in path'''
        for root, dirs, files in os.walk(self.path, topdown=False):
            for name in files:
                path = os.path.join(root, name)
                print(path)
                self.check_path(name, path, self.files)
                if not len(self.files): return 0

    def check_path(self, name_file, path, in_search:list[dict]):
        '''
        Check if file is in search list (in_search)
        '''
        for count, item in enumerate(in_search):
            print("count:", count, "item:", item)
            if self.search_in(item, name_file) and self.ignored_files_str(path)!=1:
                self.proc_load_list(path, name_file, count)
                self.check_path(name_file, path, in_search)

    def proc_load_list(self, path, name, count):
        if self.process_xl(path, self.files[count][1], self.files[count][0]): pass
            #self.save_file_status(path, self.files[count][1], self.files[count][0])       
        self.remove_found(count)

    def remove_found(self, count): self.files.pop(count)  

    def search_base(self, name) -> None:
        for item in self.base_str_find:
            if not self.search_in(item, name):
                return 0
        return 1

    def search_in(self, file_name:str, haystack:str) -> None:
        if re.search(f"{file_name}", haystack, re.IGNORECASE):
            return 1

#REFATORATING METHODS START
    def process_xl(self, path, of, nbr) -> None:
        try:
            return 1

        except Exception as e:
            self.save_file_status(path, of, nbr, e)
            return 0

    def validate_final_position(self, name_file, path, in_search):
        final_position = name_file.split(".xlsx")[0].split(" ")[-1]
        if final_position==in_search[0].upper(): return 0
        return 1

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
        self.status_file.append({"of" : f"{of}", "peca" : f"{nbr}", "caminho" : f"{path}","log":f"{e}"})
        if e!="":
            #conec.add_record(of, nbr, path, str(e))
            #self.connection_on=1
            pass

if __name__ == "__main__":
    search = SearchFile()
    print(search.files[0])
    search.search()
