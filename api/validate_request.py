import re, os

# It will be an object in new version

def is_coordinate_cell_valid(coordinate:str) -> int:
    '''Check if coordinate is valid'''
    if re.search(fr'^[A-Z]+[0-9]+$', coordinate): return True
    return False

def is_savepath_exists(savepath:str) -> int:
    '''Check if savepath exists'''
    if os.path.exists(savepath):
        return 1
    return 0

def is_request_valid(request:dict) -> int:
    '''Check if request is valid'''

    required_data = ["coordinate", "filename"]
    if set(required_data).issubset(request.keys()): return 1

    return 0
