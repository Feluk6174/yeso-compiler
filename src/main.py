import sys

from func import parse_functions, func_dec_start_asm_gen, func_dec_end_asm_gen, loader, parse_function
from base import generate_asm_start

def main():
    out = "out.asm"
    code = loader(sys.argv[1])

    global_keywords = {
        "while": 0,
        "if": 0,
        "else": 0,
    }

    asm = generate_asm_start()

    function_dict = parse_functions(code)
    for name, f_dict in function_dict.items():
        new_asm, vars = func_dec_start_asm_gen(name, f_dict["vars"])
        asm += new_asm

        asm += parse_function(name, f_dict["code"], function_dict, global_keywords, vars)

        asm += func_dec_end_asm_gen()

    with open(out, "w") as f:
        f.write(asm)
        


# 1 parse functions
# 2 parse line by line in function

if __name__ == "__main__":
    main()