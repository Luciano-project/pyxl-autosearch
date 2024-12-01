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
        try:
            xl_file = OpenxlFiles(path)
            self.sheetname = self.default_sheetname if sheetname == None else sheetname
            xl_file.open_file(path)
            xl_file.set_wb_sheet(sheetname)
            check_merged = self.check_merged_cell(self.files[index_list]["coordinate"], xl_file.get_wb_sheet())
            old_value = xl_file.get_value(self.files[index_list]["coordinate"]) if check_merged == 0 else check_merged
            xl_file.update_value(self.files[index_list]["coordinate"], self.files[index_list]["value"]) if check_merged == 0 else check_merged
            try:
                self.insert_data_response({"old_value": old_value, "coordinate":self.files[index_list]["coordinate"] if check_merged == 0 else check_merged, "value": self.files[index_list]["value"], "path":path})
                xl_file.save_file(path)
                xl_file.close_file()
                return 1
            
            except Exception as e:
                self.insert_data_response({"old_value": old_value, "coordinate": self.files[index_list]["coordinate"], "value": "", "path": path, "error": f"Trying to write data and {e}"})
                xl_file.close_file()
                return 0

        except AttributeError as e:
            self.insert_data_response({"value": "", "path":path, "coordinate": self.files[index_list]["coordinate"], "error": "Merged Cell, not possible to write in this cell"})
            return 0
        
        except Exception as e:
            self.insert_data_response({"value": "", "path":path, "coordinate": self.files[index_list]["coordinate"], "error": e})
            return 0
        

def write_file(files:list[dict]):
    file = WriteFile(files)
    file.search()
    return file.return_values

def read_file(files:list[dict]):
    file = ReadFile(files)
    file.search()
    return file.return_values