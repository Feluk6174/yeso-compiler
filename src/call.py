from const import BUILTIN, EXPECTED, SIZES, ASM_TYPES
from base import get_register
from error import UnknownFunction, WrongReturnType, MismatchedArguments, WrongArgument

def parse_none_call(tokens, vars, function_dict) -> str:
    asm = "\n push rdi\n"
    if tokens[1] in function_dict.keys():
        for i, arg in enumerate(tokens):
            if i < 2:
                continue
            
            if arg not in vars.keys():
                asm += f"""
mov {get_register("b", SIZES[function_dict[tokens[1]]["vars"][list(function_dict[tokens[1]]["vars"].keys())[i-2]]["type"]])}, {arg}
mov {ASM_TYPES[SIZES[function_dict[tokens[1]]["vars"][list(function_dict[tokens[1]]["vars"].keys())[i-2]]["type"]]]}[mem+rdi], {get_register("b", SIZES[function_dict[tokens[1]]["vars"][list(function_dict[tokens[1]]["vars"].keys())[i-2]]["type"]])}
add rdi, {SIZES[function_dict[tokens[1]]["vars"][list(function_dict[tokens[1]]["vars"].keys())[i-2]]["type"]]}
"""

            else:
                if vars[arg]["type"] not in EXPECTED[function_dict[tokens[1]]["vars"][list(function_dict[tokens[1]]["vars"].keys())[i-2]]["type"]]: raise WrongArgument(f"{i-1}th argument of {tokens[1]}", EXPECTED[function_dict[tokens[1]]["return"]], tokens, -1)
                
                asm += f"""
mov rax, {vars[arg]["rel_pos"]}
lea rsi, [r15+rax]
mov {get_register("b", SIZES[vars[arg]["type"]])}, {ASM_TYPES[SIZES[vars[arg]["type"]]]}[mem+rsi]
mov {ASM_TYPES[SIZES[vars[arg]["type"]]]}[mem+rdi], {get_register("b", SIZES[vars[arg]["type"]])}
add rdi, {SIZES[vars[arg]["type"]]}
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

            if arg not in vars.keys():
                asm += f'\nmov {BUILTIN[tokens[1]]["regs"][i-2]}, {arg}\n'

            else:
                if vars[arg]["type"] not in EXPECTED[BUILTIN[tokens[1]]["args"][i-2]]: raise WrongArgument(f"{i-1}th argument of {tokens[1]}", EXPECTED[BUILTIN[tokens[1]]["args"][i-2]], tokens, -1)
                
                asm += f"""
mov r14, {vars[arg]["rel_pos"]}
lea rsi, [r15+r14]
mov {get_register(14, SIZES[vars[arg]["type"]])}, {ASM_TYPES[SIZES[vars[arg]["type"]]]}[mem+rsi]
mov {BUILTIN[tokens[1]]["regs"][i-2]}, {get_register(14, SIZES[vars[arg]["type"]])}
"""
        asm += f"\ncall {tokens[1]}\n"

        return asm

    else: raise UnknownFunction(tokens[1], tokens, -1)
