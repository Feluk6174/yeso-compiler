import data_types.unsigned as unsigned
from const import ASM_TYPES, EXPECTED, UNSIGNED, SIZES
from error import UnknownVariable, WrongType
from base import get_register

JMP_OPS = {
    "==": "jne",
    "!=": "je",
    ">": "jle",
    "<": "jge",
    ">=": "jl",
    "<=": "jg"
}

def parse_if(tokens:list[str], vars:dict, condition_stack:list, global_keywords:dict[str, int]):
    if tokens[1] not in vars.keys(): raise UnknownVariable(tokens[1], tokens, -1)

    if tokens[3] in vars.keys():
        if not vars[tokens[1]]["type"] == vars[tokens[3]]["type"]: raise WrongType(tokens[3], EXPECTED[tokens[1]], vars[tokens[3]]["type"], "compare", tokens, -1)

        jmp_label = f"fi_if{global_keywords['if']}"
        global_keywords["if"] += 1
        condition_stack.append(jmp_label)

        return f"""
mov rcx, {vars[tokens[1]]["rel_pos"]}
mov rdx, {vars[tokens[3]]["rel_pos"]}
lea rsi, [r15+rcx]
lea r10, [r15+rdx]
mov {get_register("a", SIZES[vars[tokens[1]]["type"]])}, {ASM_TYPES[SIZES[vars[tokens[1]]["type"]]]}[mem+rsi]
mov {get_register("b", SIZES[vars[tokens[3]]["type"]])}, {ASM_TYPES[SIZES[vars[tokens[3]]["type"]]]}[mem+r10]
cmp {get_register("a", SIZES[vars[tokens[1]]["type"]])}, {get_register("b", SIZES[vars[tokens[3]]["type"]])}
{JMP_OPS[tokens[2]]} {jmp_label}
        """

    else:
        if vars[tokens[1]]["type"] in UNSIGNED:
            if not unsigned.is_num(tokens[3]): raise WrongType(tokens[3], EXPECTED[tokens[1]], "unknown", "compare", tokens, -1)
            
            jmp_label = f"fi_if{global_keywords['if']}"
            global_keywords["if"] += 1
            condition_stack.append(jmp_label)

            return f"""
mov rcx, {vars[tokens[1]]["rel_pos"]}
lea rsi, [r15+rcx]
mov {get_register("a", SIZES[vars[tokens[1]]["type"]])}, {ASM_TYPES[SIZES[vars[tokens[1]]["type"]]]}[mem+rsi]
cmp {get_register("a", SIZES[vars[tokens[1]]["type"]])}, {tokens[3]}
{JMP_OPS[tokens[2]]} {jmp_label}
            """



def parse_brakets(tokens:list[str], condition_stack:list):
    label = condition_stack.pop()
    if label[:5] == "while":
        return f"""
jmp {label}
{label}_end:
        """
    return f"""{label}:"""

