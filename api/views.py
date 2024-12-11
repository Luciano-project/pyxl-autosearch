from . import base
from .middlewares.openxl_files import OpenxlFiles
from .validate_request import is_coordinate_cell_valid, is_savepath_exists, is_request_valid, is_required_data_in_request

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

            if is_savepath_exists(self.files[index_list]) == 0:
                self.handle_invalid_path(self.files[index_list])
                return 0
            
            self.sheetname = self.default_sheetname if sheetname == None else sheetname
            xl_file.open_file(path, data_only=True)

            if xl_file.is_sheetname_valid(sheetname, xl_file) == 0:
                self.handle_invalid_sheetname(self.files[index_list])
                return 0
            xl_file.set_wb_sheet(sheetname)
            check_merged = self.check_merged_cell(self.files[index_list]["coordinate"], xl_file.get_wb_sheet())
            old_value = xl_file.get_value(self.files[index_list]["coordinate"]) if check_merged == 0 else xl_file.get_value(check_merged)
            xl_file.update_value(self.files[index_list]["coordinate"], self.files[index_list]["value"]) if check_merged == 0 else xl_file.update_value(check_merged, self.files[index_list]["value"])
            
            try:
                self.insert_data_response({**self.files[index_list],
                                           "path": path,
                                           "old_value": old_value,
                                           "error": "" if check_merged == 0 else f"It is a warning, the cell is merged and the value was written in the first cell of the merged cell: {check_merged}"})
                
                to_savepath = self.check_savepath_and_return_if_valid(self.files[index_list])
                if to_savepath == -1: raise Exception("Savepath is invalid") if to_savepath == 0 else None
                xl_file.save_file(path if to_savepath == 0 else f"{to_savepath}\\{name_file}")
                xl_file.close_file()
                return 1
            
            except Exception as e:
                self.insert_data_response({**self.files[index_list],
                                           "path": path,
                                           "old_value": old_value,
                                           "error": f"Error when trying to write data: {e}"})
                xl_file.close_file()
                return 0

        except Exception as e:
            self.insert_data_response({**self.files[index_list],
                                       "path": path,
                                       "error": f"Check the requested data. {e}"})
            return 0
    
    def check_savepath_and_return_if_valid(self, requested_item:dict):
        '''Check if savepath exists in request and return\n
        if it does not exist, try the default savepath\n
        else return 0'''
        if is_required_data_in_request(requested_item, "savepath") == 1: return requested_item["savepath"]
        elif self.default_savepath: return self.default_savepath

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