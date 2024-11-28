import re

def is_coordinate_cell_valid(coordinate:str) -> int:
    '''Check if coordinate is valid'''
    if re.search(fr'^[A-Z]+[0-9]+$', coordinate): return True
    return False