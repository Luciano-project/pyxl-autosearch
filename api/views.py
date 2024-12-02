from . import base
from .middlewares.openxl_files import OpenxlFiles
from .validate_request import is_coordinate_cell_valid, is_savepath_exists, is_request_valid

class ReadFile(base.SearchFile):
    def __init__(self, files):
        super().__init__(files)
        self.sheetname = None

    def proc_load_list(self, path, name_file, index_list, sheetname=None):
        if is_coordinate_cell_valid(self.files[index_list]["coordinate"]) == False:
            self.handle_invalid_ref(self.files[index_list])
            return 0
        
        xl_file = OpenxlFiles(path)
        xl_file.open_file(path, data_only=True)
        if xl_file.is_sheetname_valid(sheetname, xl_file) == 0:
            self.handle_invalid_sheetname(self.files[index_list])
            return 0
        
        self.sheetname = self.default_sheetname if sheetname == None else sheetname
        xl_file.set_wb_sheet(sheetname)
        check_merged = self.check_merged_cell(self.files[index_list]["coordinate"], xl_file.get_wb_sheet())
        try:
            value = xl_file.get_value(self.files[index_list]["coordinate"]) if check_merged == 0 else xl_file.get_value(check_merged)
            self.insert_data_response({"coordinate":self.files[index_list]["coordinate"],
                                           "value": value,
                                           "path": path,
                                           "error": "" if check_merged == 0 else \
                                                f"It is a warning, the cell is merged and the value is from the first cell of the merged cell: {check_merged}"})
            xl_file.close_file()
            return 1

        except Exception as e:
            self.insert_data_response({"value": "",
                                       "path":path,
                                       "coordinate": self.files[index_list]["coordinate"],
                                       "error": e})
            xl_file.close_file()
            return 0

class WriteFile(base.SearchFile):
    def __init__(self, files):
        super().__init__(files)
        self.sheetname = None
    
    def proc_load_list(self, path, name_file, index_list, sheetname=None):
        if is_coordinate_cell_valid(self.files[index_list]["coordinate"]) == 0:
            self.handle_invalid_ref(self.files[index_list])
            return 0
    
        try:
            xl_file = OpenxlFiles(path)

            if is_savepath_exists(self.files[index_list]["savepath"]) == 0:
                self.handle_invalid_path(self.files[index_list])
                return 0
            
            self.sheetname = self.default_sheetname if sheetname == None else sheetname
            xl_file.open_file(path)

            if xl_file.is_sheetname_valid(sheetname, xl_file) == 0:
                self.handle_invalid_sheetname(self.files[index_list])
                return 0
            
            xl_file.set_wb_sheet(sheetname)
            check_merged = self.check_merged_cell(self.files[index_list]["coordinate"], xl_file.get_wb_sheet())
            old_value = xl_file.get_value(self.files[index_list]["coordinate"]) if check_merged == 0 else xl_file.get_value(check_merged)
            xl_file.update_value(self.files[index_list]["coordinate"], self.files[index_list]["value"]) \
                if check_merged == 0 else xl_file.update_value(check_merged, self.files[index_list]["value"])
            try:
                self.insert_data_response({**self.files[index_list],
                                           "path": path,
                                           "old_value": old_value,
                                           "error": "" if check_merged == 0 else f"It is a warning, the cell is merged and the value was written in the first cell of the merged cell: {check_merged}"})
                is_requested_savepath = 1 if self.files[index_list]["savepath"] else 0
                
                xl_file.save_file(path if is_requested_savepath == 0 else f"{self.files[index_list]["savepath"]}\\{name_file}")
                xl_file.close_file()
                return 1
            
            except Exception as e:
                self.insert_data_response({**self.files[index_list],
                                           "path": path,
                                           "old_value": old_value,
                                           "error": f"Trying to write data and {e}"})
                xl_file.close_file()
                return 0

        except Exception as e:
            self.insert_data_response({**self.files[index_list],
                                       "path": path,
                                       "error": f"Check the requested data. {e}"})
            return 0
 
    def is_valid_parameters(self, requested_item:dict):
        if is_request_valid(requested_item)==0: return 0
        return 1

def write_file(files:list[dict]):
    file = WriteFile(files)
    file.search()
    return file.return_values

def read_file(files:list[dict]):
    file = ReadFile(files)
    file.search()
    return file.return_values