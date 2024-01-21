
from const import ASM_TYPES, get_part_size
from base import get_register

def is_var(token, vars):
    pass

def load_unsigned_pointer(vars:dict, variable:str, register:str):
    return f"""mov r14, {vars[variable]["rel_pos"]}
lea rsi, [r15+r14]
mov r13, QWORD[mem+rsi]
mov {register}, {ASM_TYPES[get_part_size(vars, variable)]}[mem+r13]"""

def store_unsigned_pointer(vars:dict, variable:str, register:str):
    return f"""mov r14, {vars[variable]["rel_pos"]}
lea rsi, [r15+r14]
mov r13, QWORD[mem+rsi]
mov {ASM_TYPES[get_part_size(vars, variable)]}[mem+r13], {register}"""

def store_unsigned_immediate_pointer(vars:dict, val:int, variable_name:str):
    return f"""
mov {get_register("a", get_part_size(vars, variable_name))}, {val}
mov r14, {vars[variable_name]["rel_pos"]}
lea rsi, [r15+r14]
mov r13, QWORD[mem+rsi]
mov {ASM_TYPES[get_part_size(vars, variable_name)]}[mem+r13], {get_register("a", get_part_size(vars, variable_name))}"""

def define_asm(tokens, vars):
    return f"""
mov rax, {vars[tokens[4]]["rel_pos"]}
add rax, r15
mov QWORD[mem+rdi], rax
add rdi, 8
""", vars