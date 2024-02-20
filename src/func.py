from const import TYPES, SIZES
from error import ParserError, WrongReturnType, FunctionAlreadyDefined, MismatchedArguments, WrongArgumentType, UnrecognisedKeyword
from mod import parse_mod
from define import parse_def
from call import parse_none_call
from ret import return_asm
from condition import parse_if, parse_brakets
from loop import parse_while
from assembly import store_register

ASM_MODE = False

def parse_functions(code: str, prev_dict:dict={}):
    """Parses the code into functions
Returns a function_dict, with the function information

    Args:
        code (str): The code to be parsed

    Raises:
        WrongReturnType: _description_
        FunctionAlreadyDefined: _description_
        MismatchedArguments: _description_
        WrongArgumentType: _description_

    Returns:
        function_dict (dict): contains the information of the functions
    """

    function_list = [func for func in code.split("\nfunc") if not func == ""]
    function_dict = prev_dict
    pos = 0
    for function in function_list:
        signature = function.split("\n")[0].split()
        if signature[0] == "func":
            signature.pop(0)
        if not signature[0] in TYPES:
            raise WrongReturnType(signature, pos)

        if signature[1] in function_dict.keys():
            raise FunctionAlreadyDefined(signature, pos)

        if len(signature) % 2 == 1:
            raise MismatchedArguments(signature, pos)

        temp = {
            "return": signature[0],
            "start": pos,
            "code": [line.lstrip() for line in function.split("\n")[1::] if not len(line) == line.count(" ")],
            "vars": {}
        }
        pos += len(function.split("\n"))

        for i in range(2, len(signature), 2):
            if signature[i] not in TYPES:
                raise WrongArgumentType(signature, i, pos)

            temp["vars"][signature[i+1]] = {
                "type": signature[i]
            }
            

        function_dict[signature[1]] = temp

    return function_dict
        

def parse_function(name:str, code:list[str], function_dict:dict, global_keywords:dict[str, int], vars:dict) -> str:
    global ASM_MODE
    asm = ""
    condition_stack = []
    for line in code:
        tokens = line.split()
        if ASM_MODE:
            if tokens[0] == "asm":
                asm += "\n"
                ASM_MODE = False
            else:
                asm += " ".join(tokens)
                asm += "\n"
        elif tokens[0] == "asm":
            asm += "\n"
            ASM_MODE = True

        elif tokens[0] == "mod":
            asm += parse_mod(tokens, vars, function_dict)

        elif tokens[0] == "def":
            new_asm, vars = parse_def(tokens, vars)
            asm += new_asm

        elif tokens[0] == "if":
            asm += parse_if(tokens, vars, condition_stack, global_keywords)

        elif tokens[0] == "while":
            asm += parse_while(tokens, vars, condition_stack, global_keywords)

        elif tokens[0] == "call":
            asm += parse_none_call(tokens, vars, function_dict)

        elif tokens[0] == "}":
            asm += parse_brakets(tokens, condition_stack)

        elif tokens[0] == "return":
            asm += return_asm(tokens, vars, function_dict, name)

        elif tokens[0] == "store":
            asm += store_register(tokens, vars)

        elif tokens[0] == "//":
            pass

        else:
            raise UnrecognisedKeyword(tokens[0], tokens, -1)
    return asm


def func_call_asm_gen() -> dict:
    pass

def func_dec_end_asm_gen() -> str:
    return """
pop r15
pop rdi
ret
"""

def func_dec_start_asm_gen(name:str, args:dict[str, dict[str, str]]) -> tuple[dict, str]:
    var_dict = {}
    pos = 0
    for arg in args.keys():
        var_dict[arg] = {
            "type": args[arg]["type"],
            "rel_pos": pos
        }
        pos += SIZES[args[arg]["type"]]

    asm = f"""{name}:
push rdi
push r15
mov  r15, rdi
add  rdi, {pos}
"""
    return asm, var_dict

def loader(path):
    with open(path, "r") as f:
        return f.read()


if __name__ == "__main__":
    try:
        print(parse_functions(loader("test.flx")))
    except ParserError as e:
        print(e)