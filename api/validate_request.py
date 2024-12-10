import re, os

# It will be an object in new version

def is_coordinate_cell_valid(coordinate:str) -> int:
    '''Check if coordinate is valid'''
    if re.search(fr'^[A-Z]+[0-9]+$', coordinate): return True
    return False

def is_savepath_exists(body_request:dict) -> int:
    '''Check if savepath exists'''
    try:
        is_requested_filepath_in_body = is_required_data_in_request(body_request, "savepath")
        if is_requested_filepath_in_body == 0: return 1
        if os.path.exists(fr"{body_request['savepath']}"): return 1
    except Exception as e:
        return -1
    return 0

def is_required_data_in_request(request:dict, required_data:str) -> int:
    '''Check if required data exists in request'''
    if required_data in request.keys(): return 1
    return 0

def is_request_valid(request:dict) -> int:
    '''Check if request is valid'''
    required_data = ["coordinate", "filename"]
    if set(required_data).issubset(request.keys()): return 1
    return 0
