from const import *
from error import VariableAlreadyDefined, UnrecognisedType, WrongSize
from base import get_register
import data_types.unsigned as unsigned
import data_types.pointer as pointer
import data_types.array as array

def parse_def(tokens:list[str], vars:dict) -> tuple[str, dict]:
    if tokens[2] in vars.keys(): raise VariableAlreadyDefined(tokens[2], tokens, -1)

    if len(vars.keys()) > 0:
        last = max(vars.values(), key=lambda var: var["rel_pos"])
        rel_pos = last["rel_pos"]+get_size(last["type"])
    else:
        rel_pos = 0
        
    vars[tokens[2]] = {
        "type": tokens[1],
        "rel_pos": rel_pos
    }

    if tokens[1] not in TYPES: 
        if not tokens[1][:5] == "list:" and not (tokens[1][0] == "*" and tokens[1][1:] in TYPES):
            raise UnrecognisedType(tokens[1], tokens, -1)
        


    if tokens[1] in UNSIGNED:
        return unsigned.define_asm(tokens, vars)

    if tokens[1][1:] in TYPES:
        return pointer.define_asm(tokens, vars)

    if tokens[1].split(":")[0] == "list":
        return array.define_asm(tokens, vars)
    

