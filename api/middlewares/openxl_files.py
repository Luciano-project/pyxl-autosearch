from middlewares.json_bridge import ConfigSearchDefinitions
from openpyxl import load_workbook

import logging

logger = logging.getLogger(__name__)

class OpenxlFiles():
    def __init__(self, filepath=None):
        self.wb_file = None
        self.wb_sheet = None
        self.extension = filepath.split(".")[-1] if filepath else None
        self.filepath = filepath

    def open_file(self, filepath, data_only=False):
        try:
            self.wb_file = load_workbook(filename=filepath, data_only=data_only) #keep_vba=True for Macros
            logger.info(msg=f"File opened: {filepath}")
            self.filepath = filepath
            return 0

        except Exception as e:
            logger.error(msg=f"{e} at OpenxlFiles.open_file()")
            return -1

    def save_file(self, filepath_save, extension=None):
        if extension is None:
            extension = self.extension
        filename = f"{filepath_save}.{extension}"
        try:
            self.wb_file.save(filename=filename)
            logger.info(msg=f"File saved: {filename}")

            return 0
        except Exception as e:
            logger.warning(msg=f"{e} at OpenxlFiles.save_file();")
            return -1

    def get_wb_sheet(self): return self.wb_sheet
    def set_wb_sheet(self, sheet_name): self.wb_sheet = self.wb_file[sheet_name]

    def get_filepath(self): return self.filepath
    def set_filepath(self, path): self.filepath = path

    def update_data(self, coodenate, value): self.wb_sheet[coodenate] = value
    def get_data(self, coodenate): return self.wb_sheet[coodenate].value


if __name__ == "__main__":
    openxl = OpenxlFiles()
    print(openxl.get_filepath())