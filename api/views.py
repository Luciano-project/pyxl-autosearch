from . import base
from .middlewares.openxl_files import OpenxlFiles
from .validate_request import is_coordinate_cell_valid

class ReadFile(base.SearchFile):
    def __init__(self, files):
        super().__init__(files)
        self.sheetname = None

    def proc_load_list(self, path, name_file, index_list, sheetname=None):
        if is_coordinate_cell_valid(self.files[index_list]["coordinate"]) == False:
            self.handle_invalid_ref(self.files[index_list])
            return 0
        xl_file = OpenxlFiles(path)
        self.sheetname = self.default_sheetname if sheetname == None else sheetname
        xl_file.open_file(path, data_only=True)
        xl_file.set_wb_sheet(sheetname)
        value = None
        try:
            value = xl_file.get_value(self.files[index_list]["coordinate"])
            self.insert_data_response({"value": value, "path":path, "coordinate": self.files[index_list]["coordinate"]})
        except Exception as e:
            self.insert_data_response({"value": "", "path":path, "coordinate": self.files[index_list]["coordinate"], "error": e})

class WriteFile(base.SearchFile):
    def __init__(self, files):
        super().__init__(files)
        self.sheetname = None
    
    def proc_load_list(self, path, name_file, index_list, sheetname=None):
        if is_coordinate_cell_valid(self.files[index_list]["coordinate"]) == False:
            self.handle_invalid_ref(self.files[index_list])
            return 0
        xl_file = OpenxlFiles(path)
        self.sheetname = self.default_sheetname if sheetname == None else sheetname
        xl_file.open_file(path)
        xl_file.set_wb_sheet(sheetname)
        old_value = xl_file.get_value(self.files[index_list]["coordinate"])
        xl_file.update_value(self.files[index_list]["coordinate"], self.files[index_list]["value"])
        try:
            self.insert_data_response({"old_value": old_value, "coodinate":self.files[index_list]["coordinate"], "value": self.files[index_list]["value"], "path":path})
            xl_file.save_file(path)
            xl_file.close_file()
            return 1
        
        except Exception as e:
            self.insert_data_response({"old_value": old_value, "coodinate": self.files[index_list]["coordinate"], "value": "", "path": path, "error": e})
            return 0

        

def write_file(files:list[dict]):
    file = WriteFile(files)
    file.search()
    return file.return_values

def read_file(files:list[dict]):
    file = ReadFile(files)
    file.search()
    return file.return_values