from data_types.unsigned import store_variable

def store_register(tokens, vars):
    asm = store_variable(vars, tokens[2], tokens[1]) + "\n"
    return asm