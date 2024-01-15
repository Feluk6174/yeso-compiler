from const import EXPECTED, SIZES, ASM_TYPES
from error import WrongReturnReturnType
from base import get_register

def return_asm(tokens:list[str], vars:dict, function_dict:dict, name:str) -> str:
    if tokens[1] in vars.keys():
        if vars[tokens[1]]["type"] not in EXPECTED[function_dict[name]["return"]]: raise WrongReturnReturnType(name, tokens[1], vars[tokens[1]]["type"], function_dict[name]["return"], tokens, -1)
        return f"""
mov rbx, {vars[tokens[1]]["rel_pos"]}
lea rsi, [r15+rbx]
mov {get_register("a", SIZES[function_dict[name]["return"]])}, {ASM_TYPES[SIZES[function_dict[name]["return"]]]}[mem+rsi]
pop r15
pop rdi
ret
"""

    else:
        return f"""
mov {get_register("a", SIZES[function_dict[name]["return"]])}, {tokens[1]}
pop r15
pop rdi
ret
"""