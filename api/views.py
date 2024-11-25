from . import base
from middlewares.openxl_files import OpenxlFiles


class ReadFile(base.SearchFile):
    def __init__(self):
        super().__init__()
        self.sheetname = None
    
    def proc_load_list(self, path, name_file, index_list, sheetname):
        xl_file = OpenxlFiles(path)
        self.sheetname = sheetname
        xl_file.open_file(path)
        xl_file.set_wb_sheet(sheetname)
        xl_file.get_data(self.files[index_list]["coordenate"])

class WriteFile(base.SearchFile):
    def __init__(self):
        super().__init__()
        self.sheetname = None
    
    def proc_load_list(self, path, name_file, index_list, sheetname):
        xl_file = OpenxlFiles(path)
        self.sheetname = sheetname
        xl_file.open_file(path)
        xl_file.set_wb_sheet(sheetname)
        xl_file.update_data(self.files[index_list]["coordenate"], self.files[index_list]["value"])
        xl_file.save_file(path)

def update_file(files:list[dict]):
    file = ReadFile(files = dict)

def read_file(files:list[dict]):
    file = WriteFile(files = dict)