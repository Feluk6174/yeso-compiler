from condition import parse_if, JMP_OPS

def parse_while(tokens:list[str], vars:dict, condition_stack:list, global_keywords:dict[str, int]):
    while_tag = f"while{global_keywords['while']}"
    condition_stack.append(while_tag)
    global_keywords['while'] += 1

    asm = while_tag+":"
    asm += parse_if(tokens, vars, condition_stack, global_keywords)
    condition_stack.pop()
    global_keywords["if"] -= 1
    asm = "\n".join(asm.split("\n")[:-2])+"\n"
    asm += f"{JMP_OPS[tokens[2]]} {while_tag+'_end'}"

    return asm