import data_types.unsigned as unsigned
import data_types.array as array
from const import BUILTIN, EXPECTED, SIZES, ASM_TYPES, get_part_size, get_part_type
from base import get_register
from error import UnknownFunction, WrongReturnType, MismatchedArguments, WrongArgument

def parse_none_call(tokens, vars, function_dict) -> str:
    asm = "\n push rdi\n"
    if tokens[1] in function_dict.keys():
        for i, arg in enumerate(tokens):
            if i < 2:
                continue
            
            if unsigned.is_num(arg):
                asm += f"""
mov {get_register("b", SIZES[function_dict[tokens[1]]["vars"][list(function_dict[tokens[1]]["vars"].keys())[i-2]]["type"]])}, {arg}
mov {ASM_TYPES[SIZES[function_dict[tokens[1]]["vars"][list(function_dict[tokens[1]]["vars"].keys())[i-2]]["type"]]]}[mem+rdi], {get_register("b", SIZES[function_dict[tokens[1]]["vars"][list(function_dict[tokens[1]]["vars"].keys())[i-2]]["type"]])}
add rdi, {SIZES[function_dict[tokens[1]]["vars"][list(function_dict[tokens[1]]["vars"].keys())[i-2]]["type"]]}
"""

            elif unsigned.is_var(arg, vars):
                if get_part_type(vars, arg) not in EXPECTED[function_dict[tokens[1]]["vars"][list(function_dict[tokens[1]]["vars"].keys())[i-2]]["type"]]: raise WrongArgument(f"{i-1}th argument of {tokens[1]}", EXPECTED[function_dict[tokens[1]]["return"]], tokens, -1)
                
                asm += f"""
{unsigned.load_variable(vars, arg, get_register("b", get_part_size(vars, arg)))}
mov {ASM_TYPES[get_part_size(vars, arg)]}[mem+rdi], {get_register("b", get_part_size(vars, arg))}
add rdi, {get_part_size(vars, arg)}
"""
        asm += f"""
pop rdi
call {tokens[1]}

"""

        return asm
    
    elif tokens[1] in BUILTIN.keys(): 
        if not BUILTIN[tokens[1]]["return_type"] == "none": raise WrongReturnType(tokens, -1)
        if not len(tokens) == len(BUILTIN[tokens[1]]["args"])+2: raise 

        asm = ""

        for i, arg in enumerate(tokens):
            if i < 2:
                continue

            if unsigned.is_num(arg):
                asm += f'\nmov {BUILTIN[tokens[1]]["regs"][i-2]}, {arg}\n'

            elif unsigned.is_var(arg, vars):
                if get_part_type(vars, arg) not in EXPECTED[BUILTIN[tokens[1]]["args"][i-2]]: raise WrongArgument(f"{i-1}th argument of {tokens[1]}", EXPECTED[BUILTIN[tokens[1]]["args"][i-2]], tokens, -1)
                
                asm += f"""
{unsigned.load_variable(vars, arg, get_register(14, get_part_size(vars, arg)))}
mov {BUILTIN[tokens[1]]["regs"][i-2]}, {get_register(14, get_part_size(vars, arg))}
"""
        asm += f"\ncall {tokens[1]}\n"

        return asm

    else: raise UnknownFunction(tokens[1], tokens, -1)
