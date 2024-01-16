from const import SIZES, ASM_TYPES, TYPES, EXPECTED, BUILTIN, UNSIGNED, get_part_size
from base import get_register
from error import WrongSize, UnknownVariable, WrongArgument, UnknownFunction
from data_types.array import load_unsigned_from_list, store_unsigned_in_list, store_imediate_in_list

def store_immediate(vars:dict, val:int, variable_name:str):
    if variable_name in vars:
        return f"""
mov {get_register("a", SIZES[vars[variable_name]["type"]])}, {val}
mov rbx, {vars[variable_name]["rel_pos"]}
lea rsi, [r15+rbx]
mov {ASM_TYPES[SIZES[vars[variable_name]["type"]]]}[mem+rsi], {get_register("a", SIZES[vars[variable_name]["type"]])}
"""
    elif variable_name.split(":")[0] in vars:
        return store_imediate_in_list(vars, val, variable_name)

def load_variable(vars:dict, variable:str, register:str):
    """
    WARNING overwrites r14 and rsi (i if list index is a variable r13)
    """
    if variable in vars:
        return f"""mov r14, {vars[variable]["rel_pos"]}
lea rsi, [r15+r14]
mov {register}, {ASM_TYPES[SIZES[vars[variable]["type"]]]}[mem+rsi]"""

    elif variable.split(":")[0] in vars:
        return load_unsigned_from_list(vars, variable, register)

def store_variable(vars:dict, variable:str, register:str):
    """
    WARNING overwrites rsi and r14
    """
    if variable in vars:
        return f"""mov r14, {vars[variable]["rel_pos"]}
lea rsi, [r15+r14]
mov {ASM_TYPES[SIZES[vars[variable]["type"]]]}[mem+rsi], {register}"""

    elif variable.split(":")[0] in vars:
        return store_unsigned_in_list(vars, variable, register)
        


def define_asm(tokens, vars) -> tuple[str, dict]:
    if is_num(tokens[4]):
        return f"""
mov {get_register("a", SIZES[tokens[1]])}, {tokens[4]}
mov {ASM_TYPES[SIZES[tokens[1]]]}[mem+rdi], {get_register("a", SIZES[tokens[1]])}
add rdi, {SIZES[tokens[1]]}
""", vars

    elif tokens[4].split(":")[0] in vars.keys():
        if not SIZES[tokens[1]] == get_part_size(vars, tokens[4]): raise WrongSize(tokens[1], vars[tokens[4]]["type"], tokens, -1)
        return f"""
{load_variable(vars, tokens[4], get_register("a", SIZES[tokens[1]]))}
mov {ASM_TYPES[SIZES[tokens[1]]]}[mem+rdi], {get_register("a", SIZES[tokens[1]])}
add rdi, {SIZES[tokens[1]]}
""", vars


def mod_asm(tokens, vars) -> str:
    if is_var(tokens[3], vars):
        if not get_part_size(vars, tokens[3]) == get_part_size(vars, tokens[1]): raise WrongSize(vars[tokens[3]]["type"], vars[tokens[1]]["type"], tokens, -1)
        return f"""
{load_variable(vars, tokens[3], get_register("a", get_part_size(vars, tokens[1])))}
{store_variable(vars, tokens[1], get_register("a", get_part_size(vars, tokens[1])))}
"""
    else:
        try:
            num  = int(tokens[3])
            return store_immediate(vars, int(tokens[3]), tokens[1])
        except ValueError:
            raise UnknownVariable(tokens[3], tokens, -1)


def is_num(token:str):
    try:
        int(token)
    except ValueError:
        return False
    return int(token) >= 0
    

def is_var(token:str, vars:dict):
    var = token.split(":")[0]
    if not var in vars.keys(): return False
    if token in vars.keys(): return vars[var]["type"] in UNSIGNED
    else: return vars[var]["type"].split(":")[1] in UNSIGNED



def add_asm(tokens:list[str], vars:dict) -> str:
    if not is_var(tokens[3], vars) and not is_num(tokens[3]): raise WrongArgument(tokens[3], EXPECTED[vars[tokens[1]]["type"]], tokens, -1)
    if not is_var(tokens[5], vars) and not is_num(tokens[5]): raise WrongArgument(tokens[5], EXPECTED[vars[tokens[5]]["type"]], tokens, -1)

    if is_num(tokens[3]) and is_num(tokens[5]):
        return store_immediate(vars, int(tokens[3])+int(tokens[5]), tokens[1])


    elif (is_num(tokens[3]) and is_var(tokens[5], vars)) or (is_num(tokens[5]) and is_var(tokens[3], vars)):
        num = tokens[3] if is_num(tokens[3]) else tokens[5]
        var = tokens[3] if not is_num(tokens[3]) else tokens[5]
        if not get_part_size(vars, tokens[1]) == get_part_size(vars, var): raise WrongSize(vars[tokens[1]]["type"], vars[var]["type"], tokens, -1)
        return f"""
{load_variable(vars, var, get_register("a", get_part_size(vars, var)))}
add {get_register("a", get_part_size(vars, var))}, {num}
{store_variable(vars, tokens[1], get_register("a", get_part_size(vars, var)))}
"""


    else:
        if not get_part_size(vars, tokens[1]) == get_part_size(vars, tokens[3]): raise WrongSize(vars[tokens[1]]["type"], vars[tokens[3]]["type"], tokens, -1)
        if not get_part_size(vars, tokens[1]) == get_part_size(vars, tokens[5]): raise WrongSize(vars[tokens[1]]["type"], vars[tokens[5]]["type"], tokens, -1)
        return f"""
{load_variable(vars, tokens[3], get_register("a", get_part_size(vars, tokens[3])))}
{load_variable(vars, tokens[5], get_register("b", get_part_size(vars, tokens[5])))}
add {get_register("a", get_part_size(vars, tokens[3]))}, {get_register("b", get_part_size(vars, tokens[5]))}
{store_variable(vars, tokens[1], get_register("a", get_part_size(vars, tokens[1])))}
"""


def sub_asm(tokens:list[str], vars:dict) -> str:
    if not is_var(tokens[3], vars) and not is_num(tokens[3]): raise WrongArgument(tokens[3], EXPECTED[vars[tokens[1]]["type"]], tokens, -1)
    if not is_var(tokens[5], vars) and not is_num(tokens[5]): raise WrongArgument(tokens[5], EXPECTED[vars[tokens[5]]["type"]], tokens, -1)


    if is_num(tokens[3]) and is_num(tokens[5]):
        return store_immediate(vars, int(tokens[3])-int(tokens[5]), tokens[1])

    elif (is_num(tokens[3]) and is_var(tokens[5], vars)) or (is_num(tokens[5]) and is_var(tokens[3], vars)):
        num = tokens[3] if is_num(tokens[3]) else tokens[5]
        var = tokens[3] if not is_num(tokens[3]) else tokens[5]
        if not get_part_size(vars, tokens[1]) == get_part_size(vars, var): raise WrongSize(vars[tokens[1]]["type"], vars[var]["type"], tokens, -1)
        var_register = "a" if is_num(tokens[3]) else "b"
        num_register = "b" if is_num(tokens[3]) else "a"
        asm = f"""
{load_variable(vars, var, get_register(var_register, get_part_size(vars, var)))}
mov {get_register(num_register, get_part_size(vars, tokens[1]))}, {num}
sub {get_register("b", get_part_size(vars, tokens[1]))}, {get_register("a", get_part_size(vars, tokens[1]))}
{store_variable(vars, tokens[1], get_register("b", get_part_size(vars, tokens[1])))}
"""
        return asm

    else:
        if not get_part_size(vars, tokens[1]) == get_part_size(vars, tokens[3]): raise WrongSize(vars[tokens[1]]["type"], vars[tokens[3]]["type"], tokens, -1)
        if not get_part_size(vars, tokens[1]) == get_part_size(vars, tokens[5]): raise WrongSize(vars[tokens[1]]["type"], vars[tokens[5]]["type"], tokens, -1)
        return f"""
{load_variable(vars, tokens[3], get_register("a", get_part_size(vars, tokens[3])))}
{load_variable(vars, tokens[5], get_register("b", get_part_size(vars, tokens[5])))}
sub {get_register("a", get_part_size(vars, tokens[3]))}, {get_register("b", get_part_size(vars, tokens[5]))}
{store_variable(vars, tokens[1], get_register("a", get_part_size(vars, tokens[1])))}
"""


def mul_asm(tokens:list[str], vars:dict) -> str:
    if not is_var(tokens[3], vars) and not is_num(tokens[3]): raise WrongArgument(tokens[3], EXPECTED[vars[tokens[1]]["type"]], tokens, -1)
    if not is_var(tokens[5], vars) and not is_num(tokens[5]): raise WrongArgument(tokens[5], EXPECTED[vars[tokens[5]]["type"]], tokens, -1)


    if is_num(tokens[3]) and is_num(tokens[5]):
        return store_immediate(vars, int(tokens[3])*int(tokens[5]), tokens[1])


    elif (is_num(tokens[3]) and is_var(tokens[5], vars)) or (is_num(tokens[5]) and is_var(tokens[3], vars)):
        num = tokens[3] if is_num(tokens[3]) else tokens[5]
        var = tokens[3] if not is_num(tokens[3]) else tokens[5]
        if not get_part_size(vars, tokens[1]) == get_part_size(vars, var): raise WrongSize(vars[tokens[1]]["type"], vars[var]["type"], tokens, -1)
        return f"""
{load_variable(vars, var, get_register("b", get_part_size(vars, var)))}
mov {get_register("a", get_part_size(vars, tokens[1]))}, {num}
mul {get_register("b", get_part_size(vars, var))}
{store_variable(vars, tokens[1], get_register("a", get_part_size(vars, var)))}
"""

    else:
        if not get_part_size(vars, tokens[1]) == get_part_size(vars, tokens[3]): raise WrongSize(vars[tokens[1]]["type"], vars[tokens[3]]["type"], tokens, -1)
        if not get_part_size(vars, tokens[1]) == get_part_size(vars, tokens[5]): raise WrongSize(vars[tokens[1]]["type"], vars[tokens[5]]["type"], tokens, -1)
        return f"""
{load_variable(vars, tokens[5], get_register("b", get_part_size(vars, tokens[5])))}
{load_variable(vars, tokens[3], get_register("a", get_part_size(vars, tokens[3])))}
mul {get_register("b", get_part_size(vars, tokens[1]))}
{store_variable(vars, tokens[1], get_register("a", get_part_size(vars, tokens[1])))}
"""


def div_asm(tokens:list[str], vars:dict) -> str:
    if not is_var(tokens[3], vars) and not is_num(tokens[3]): raise WrongArgument(tokens[3], EXPECTED[vars[tokens[1]]["type"]], tokens, -1)
    if not is_var(tokens[5], vars) and not is_num(tokens[5]): raise WrongArgument(tokens[5], EXPECTED[vars[tokens[5]]["type"]], tokens, -1)


    if is_num(tokens[3]) and is_num(tokens[5]):
        return store_immediate(vars, int(tokens[3])//int(tokens[5]), tokens[1])


    elif (is_num(tokens[3]) and is_var(tokens[5], vars)) or (is_num(tokens[5]) and is_var(tokens[3], vars)):
        num = tokens[3] if is_num(tokens[3]) else tokens[5]
        var = tokens[3] if not is_num(tokens[3]) else tokens[5]
        if not get_part_size(vars, tokens[1]) == get_part_size(vars, var): raise WrongSize(vars[tokens[1]]["type"], vars[var]["type"], tokens, -1)
        var_register = "b" if is_num(tokens[3]) else "a"
        num_register = "a" if is_num(tokens[3]) else "b"
        return f"""
mov rdx, 0
{load_variable(vars, var, get_register(var_register, get_part_size(vars, var)))}
mov {get_register(num_register, get_part_size(vars, tokens[1]))}, {num}
div {get_register("b", get_part_size(vars, tokens[1]))}
{store_variable(vars, tokens[1], get_register("a", get_part_size(vars, tokens[1])))}
        """


    else:
        if not get_part_size(vars, tokens[1]) == get_part_size(vars, tokens[3]): raise WrongSize(vars[tokens[1]]["type"], vars[tokens[3]]["type"], tokens, -1)
        if not get_part_size(vars, tokens[1]) == get_part_size(vars, tokens[5]): raise WrongSize(vars[tokens[1]]["type"], vars[tokens[5]]["type"], tokens, -1)
        return f"""
mov rdx, 0
{load_variable(vars, tokens[3], get_register("a", get_part_size(vars, tokens[3])))}
{load_variable(vars, tokens[5], get_register("b", get_part_size(vars, tokens[5])))}
div {get_register("b", get_part_size(vars, tokens[5]))}
{store_variable(vars, tokens[1], get_register("a", get_part_size(vars, tokens[1])))}
"""


def modul_asm(tokens:list[str], vars:dict) -> str:
    if not is_var(tokens[3], vars) and not is_num(tokens[3]): raise WrongArgument(tokens[3], EXPECTED[vars[tokens[1]]["type"]], tokens, -1)
    if not is_var(tokens[5], vars) and not is_num(tokens[5]): raise WrongArgument(tokens[5], EXPECTED[vars[tokens[5]]["type"]], tokens, -1)

    if is_num(tokens[3]) and is_num(tokens[5]):
        return store_immediate(vars, int(tokens[3])%int(tokens[5]), tokens[1])


    elif (is_num(tokens[3]) and is_var(tokens[5], vars)) or (is_num(tokens[5]) and is_var(tokens[3], vars)):
        num = tokens[3] if is_num(tokens[3]) else tokens[5]
        var = tokens[3] if not is_num(tokens[3]) else tokens[5]
        if not get_part_size(vars, tokens[1]) == get_part_size(vars, var): raise WrongSize(vars[tokens[1]]["type"], vars[var]["type"], tokens, -1)
        var_register = "b" if is_num(tokens[3]) else "a"
        num_register = "a" if is_num(tokens[3]) else "b"
        return f"""
mov rdx, 0
{load_variable(vars, var, get_register(var_register, get_part_size(vars, var)))}
mov {get_register(num_register, get_part_size(vars, tokens[1]))}, {num}
div {get_register("b", get_part_size(vars, tokens[1]))}
{"mov dl, ah" if get_part_size(vars, tokens[1]) == 1 else ""}
{store_variable(vars, tokens[1], get_register("d", get_part_size(vars, tokens[1])))}
        """


    else:
        if not get_part_size(vars, tokens[1]) == get_part_size(vars, tokens[3]): raise WrongSize(vars[tokens[1]]["type"], vars[tokens[3]]["type"], tokens, -1)
        if not get_part_size(vars, tokens[1]) == get_part_size(vars, tokens[5]): raise WrongSize(vars[tokens[1]]["type"], vars[tokens[5]]["type"], tokens, -1)
        return f"""
mov rdx, 0
{load_variable(vars, tokens[3], get_register("a", get_part_size(vars, tokens[3])))}
{load_variable(vars, tokens[5], get_register("b", get_part_size(vars, tokens[5])))}
div {get_register("b", get_part_size(vars, tokens[5]))}
{"mov dl, ah" if get_part_size(vars, tokens[1]) == 1 else ""}
{store_variable(vars, tokens[1], get_register("d", get_part_size(vars, tokens[1])))}
"""


def call_asign(tokens:list[str], vars:dict, function_dict:dict) -> str:
    asm = "push rdi"
    if tokens[4] in function_dict.keys():
        for i, arg in enumerate(tokens):
            if i < 5:
                continue
            
            if arg not in vars.keys():
                asm += f"""
mov {get_register("b", SIZES[function_dict[tokens[4]]["vars"][list(function_dict[tokens[4]]["vars"].keys())[i-5]]["type"]])}, {arg}
mov {ASM_TYPES[SIZES[function_dict[tokens[4]]["vars"][list(function_dict[tokens[4]]["vars"].keys())[i-5]]["type"]]]}[mem+rdi], {get_register("b", SIZES[function_dict[tokens[4]]["vars"][list(function_dict[tokens[4]]["vars"].keys())[i-5]]["type"]])}
add rdi, {SIZES[function_dict[tokens[4]]["vars"][list(function_dict[tokens[4]]["vars"].keys())[i-5]]["type"]]}
"""

            else:
                if vars[arg]["type"] not in EXPECTED[function_dict[tokens[4]]["return"]]: raise WrongArgument(f"{i-1}th argument of {tokens[1]}", EXPECTED[function_dict[tokens[4]]["return"]], tokens, -1)
                
                asm += f"""
mov rax, {vars[arg]["rel_pos"]}
lea rsi, [r15+rax]
mov {get_register("b", SIZES[vars[arg]["type"]])}, {ASM_TYPES[SIZES[vars[arg]["type"]]]}[mem+rsi]
mov {ASM_TYPES[SIZES[vars[arg]["type"]]]}[mem+rdi], {get_register("b", SIZES[vars[arg]["type"]])}
add rdi, {SIZES[vars[arg]["type"]]}
"""
        asm += f"""
pop rdi
call {tokens[4]}

mov rbx, {vars[tokens[1]]["rel_pos"]}
lea rsi, [r15+rbx]
mov {ASM_TYPES[SIZES[vars[tokens[1]]["type"]]]}[mem+rsi], {get_register("a", SIZES[function_dict[tokens[4]]["return"]])}
"""

        return asm


    elif tokens[4] in BUILTIN.keys():
        pass

    else:
        raise UnknownFunction(tokens[4], tokens, -1)