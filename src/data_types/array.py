from error import WrongType, WrongSize
from const import ASM_TYPES, SIZES, get_part_size
from base import get_register

def is_var(var, vars):
    return vars[var]["type"][:5] == "list:"

def get_array_var_size(vars:dict, variable:str):
    var, idx = variable.split(":")
    if idx == "len":
        return SIZES["u64"]
    return SIZES[vars[var]["type"].split(":")[1]]


def store_unsigned_in_list(vars:dict, variable:str, register:str):
    _, T, num = vars[variable.split(":")[0]]["type"].split(":")
    var, idx = variable.split(":")
    if idx in vars.keys(): 
        return f"""
mov r14, {vars[idx]["rel_pos"]}
lea rsi, [r15+r14]
mov r13, QWORD[mem+rsi]
mov r14, {vars[var]["rel_pos"]}
lea rsi, QWORD[r15+r14]
mov r14, QWORD[mem+rsi]
sub r14, 1
cmp r13, r14
jg panic_program
{f"shl r13, {SIZES[T]//2}" if not SIZES[T] == 1 else ""}
mov r14, {vars[var]["rel_pos"]}
add r13, 8
lea rsi, [r15+r13]
add rsi, r14
mov {ASM_TYPES[SIZES[T]]}[mem+rsi], {register}
"""

    if int(idx) < int(num): 
        return f"""
mov r14, {vars[var]["rel_pos"]+int(idx)*SIZES[T]+8}
lea rsi, [r15+r14]
mov {ASM_TYPES[SIZES[T]]}[mem+rsi], {register}"""

    raise IndexError(f"Variable {var} has only {num} entries, (< {idx})")


def store_imediate_in_list(vars:dict, val:int, variable_name:str):
    _, T, num = vars[variable_name.split(":")[0]]["type"].split(":")
    var, idx = variable_name.split(":")
    if idx in vars.keys(): 
        return f"""
mov {get_register("a", SIZES[T])}, {val}
mov r14, {vars[idx]["rel_pos"]}
lea rsi, [r15+r14]
mov r13, QWORD[mem+rsi]
mov r14, {vars[var]["rel_pos"]}
lea rsi, QWORD[r15+r14]
mov r14, QWORD[mem+rsi]
sub r14, 1
cmp r13, r14
jg panic_program
{f"shl r13, {SIZES[T]//2}" if not SIZES[T] == 1 else ""}
mov r14, {vars[var]["rel_pos"]}
add r13, 8
lea rsi, [r15+r13]
add rsi, r14
mov {ASM_TYPES[SIZES[T]]}[mem+rsi], {get_register("a", SIZES[T])}
"""

    if int(idx) < int(num): 
        return f"""
mov {get_register("a", SIZES[T])}, {val}
mov r14, {vars[var]["rel_pos"]+int(idx)*SIZES[T]+8}
lea rsi, [r15+r14]
mov {ASM_TYPES[SIZES[T]]}[mem+rsi], {get_register("a", SIZES[T])}"""

    raise IndexError(f"Variable {var} has only {num} entries, (< {idx})")


def load_unsigned_from_list(vars:dict, variable:str, register:str):
    _, T, num = vars[variable.split(":")[0]]["type"].split(":")
    var, idx = variable.split(":")

    if idx == "len":
        return f"""
mov r14, {vars[var]["rel_pos"]}
lea rsi, [r15+r14]
mov {register}, {ASM_TYPES[SIZES["u64"]]}[mem+rsi]
"""

    if idx in vars.keys():
        if not vars[idx]["type"] == "u64": raise WrongType(idx, "u64", vars[idx]["type"], "list indexing", None, -1)
        return f"""
mov r14, {vars[idx]["rel_pos"]}
lea rsi, [r15+r14]
mov r13, QWORD[mem+rsi]
mov r14, {vars[var]["rel_pos"]}
lea rsi, QWORD[r15+r14]
mov r14, QWORD[mem+rsi]
sub r14, 1
cmp r13, r14
jg panic_program
{f"shl r13, {SIZES[T]//2}" if not SIZES[T] == 1 else ""}
mov r14, {vars[var]["rel_pos"]}
add r13, 8
lea rsi, [r15+r13]
add rsi, r14
mov {register}, {ASM_TYPES[SIZES[T]]}[mem+rsi]
"""
    if int(idx) < int(num):
        return f"""
mov r14, {vars[var]["rel_pos"]+int(idx)*SIZES[T]+8}
lea rsi, [r15+r14]
mov {register}, {ASM_TYPES[SIZES[T]]}[mem+rsi]"""

    else: raise IndexError(f"Variable {var} has only {num} entries, (< {idx})")


def define_asm(tokens:list[str], vars:dict) -> tuple[str, dict]:
    _, T, num = tokens[1].split(":")
    asm = f"""
mov rax, {num}
mov {ASM_TYPES[8]}[mem+rdi], rax
add rdi, 8
        """

    if len(tokens) == 5:
        if tokens[4] in vars.keys():
            if not tokens[1] == vars[tokens[4]]["type"]: raise WrongType(tokens[2], tokens[1], vars[tokens[4]]["type"], "assign", tokens, -1)
            vars[tokens[2]]["rel_pos"] = vars[tokens[4]]["rel_pos"]
            return "", vars

        elif tokens[4].split(":")[0] == "list":
            _, val, gnum = tokens[4].split(":")
            if not num == gnum: raise WrongSize(tokens[1], tokens[4], tokens, -1)
            for _ in range(int(gnum)):
                asm += f"""
mov {get_register("a", SIZES[T])}, {val}
mov {ASM_TYPES[SIZES[T]]}[mem+rdi], {get_register("a", SIZES[T])}
add rdi, {SIZES[T]}"""

            return asm, vars
            
        elif (tokens[4][0] == "\"" or tokens[4][0] == "\'") and (tokens[4][-1] == "\"" or tokens[4][-1] == "\'"):
            if not T == "u8": raise WrongType(tokens[2], "list:u8:n", f"list:{T}:n", "assign", tokens, -1)
            if not int(num) == len(tokens[4])-2: raise WrongType(tokens[2], tokens[1], f"list:{T}:{len(tokens[4])-2}", "assign", tokens, -1)
            for char in tokens[4][1:-1]:
                asm += f"""
    mov {get_register("a", SIZES[T])}, {ord(char)}
    mov {ASM_TYPES[SIZES[T]]}[mem+rdi], {get_register("a", SIZES[T])}
    add rdi, {SIZES[T]}"""

            return asm, vars

        else:
            pass

    else:        
        if (tokens[4][0] == "\"" or tokens[4][0] == "\'") and (tokens[-1][-1] == "\"" or tokens[-1][-1] == "\'"):
            text = " ".join(tokens[4:])
            if not T == "u8": raise WrongType(tokens[2], "list:u8:n", f"list:{T}:n", "assign", tokens, -1)
            if not int(num) == len(text)-2: raise WrongType(tokens[2], tokens[1], f"list:{T}:{len(text)-2}", "assign", tokens, -1)
            for char in text[1:-1]:
                asm += f"""
    mov {get_register("a", SIZES[T])}, {ord(char)}
    mov {ASM_TYPES[SIZES[T]]}[mem+rdi], {get_register("a", SIZES[T])}
    add rdi, {SIZES[T]}"""

            return asm, vars

        if not int(num) == len(tokens) - 4: raise WrongType(tokens[2], tokens[1], f"list:{T}:{len(tokens)-4}", "assign", tokens, -1)
        for val in tokens[4:]:
            asm += f"""
mov {get_register("a", SIZES[T])}, {val}
mov {ASM_TYPES[SIZES[T]]}[mem+rdi], {get_register("a", SIZES[T])}
add rdi, {SIZES[T]}"""

        return asm, vars
