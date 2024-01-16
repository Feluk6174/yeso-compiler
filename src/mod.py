from const import TYPES, SIZES, ASM_TYPES, UNSIGNED
from error import UnknownVariable, WrongSize, WrongArgumentType
from base import get_register
import data_types.unsigned as unsigned

def parse_mod(tokens:list[str], vars:dict, func_dict) -> str:
    if tokens[2] in vars.keys(): raise UnknownVariable(tokens[2], tokens, -1)

    if unsigned.is_var(tokens[1], vars):
        if tokens[3] == "call":
            return unsigned.call_asign(tokens, vars, func_dict)

        elif len(tokens) == 4:
            return unsigned.mod_asm(tokens, vars)

        elif len(tokens) == 6:
            if tokens[4] == "+":
                return unsigned.add_asm(tokens, vars)

            elif tokens[4] == "-":
                return unsigned.sub_asm(tokens, vars)

            elif tokens[4] == "*":
                return unsigned.mul_asm(tokens, vars)

            elif tokens[4] == "/":
                return unsigned.div_asm(tokens, vars)

            elif tokens[4] == "%":
                return unsigned.modul_asm(tokens, vars)
            
            else:
                pass

    else:
        pass
    