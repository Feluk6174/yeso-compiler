from typing import overload

from const import TYPES, SIZES



class ParserError(Exception):
    def __init__(self, error_name:str|None, message:str|None, line:int|None, line_content:str|None, fix:str|None):
        super().__init__(f"ERROR<{error_name}>: {message} on line {line}:\n{line_content}\n\n{fix}")

class WrongReturnType(ParserError):
    def __init__(self, signature:list[str], line:int):
        content = f"Wrong return type. {signature[0]} not recognised"
        line_content = f"func " + " ".join(signature)
        fix = f"Allowed types are {' '.join(TYPES)}"
        super().__init__("WrongReturnType", content, line, line_content, fix)

class FunctionAlreadyDefined(ParserError):
    def __init__(self, signature:list[str], line:int):
        content = f"Function {signature[1]} already defined"
        line_content = f"func " + " ".join(signature)
        fix = "Try Changing its name"
        super().__init__("FunctionAlreadyDefined", content, line, line_content, fix)

class MismatchedArguments(ParserError):
    def __init__(self, signature:list[str], line:int):
        content = f"Function {signature[1]} has mismatched types on its arguments."
        line_content = f"func " + " ".join(signature)
        fix = "Every argument has to have a defined type. Function declaration syntax:\nfunc type name type arg0 type arg1 ..."
        super().__init__("MismatchedArguments", content, line, line_content, fix)


class WrongArgumentType(ParserError):
    def __init__(self, signature:list[str], idx:int, line:int): 
        content = f"The argument {signature[idx+1]} has unrecognised type '{signature[idx]}' at {signature[1]} declaration"
        line_content = f"func " + " ".join(signature)
        fix = f"Allowed types are {' '.join(TYPES)}"
        super().__init__("WrongArgumentType", content, line, line_content, fix)


class VariableAlreadyDefined(ParserError):
    def __init__(self, name:str, tokens:list[str], line):
        content = f"Variable {name} is already defined"
        line_content = " ".join(tokens)
        fix = "Change the name of Variable"
        super().__init__("VariableAlreadyDefined", content, line, line_content, fix)


class UnrecognisedType(ParserError):
    def __init__(self, t:str, line:str|list[str], line_num:int):
        content = f"Type {t} is not recognised"
        line_content = line if isinstance(line, str) else " ".join(line)
        fix = f"Allowed types are {' '.join(TYPES)}"
        super().__init__("UnrecognisedError", content, line_num, line_content, fix)

class WrongSize(ParserError):
    def __init__(self, type1:str, type2:str, line:str|list, line_num:int):
        content = f"Wrong size, {type1} is {SIZES[type1]} bytes long but {type2} is {SIZES[type2]} bytes long"
        line_content = line if isinstance(line, str) else " ".join(line)
        fix = f"Try using a variable of size {SIZES[type1]}"
        super().__init__("WrongSize", content, line_num, line_content, fix)

class UnknownVariable(ParserError):
    def __init__(self, name:str, line:str|list, line_num:int):
        content = f"Variable {name} is not defined."
        line_content = line if isinstance(line, str) else " ".join(line)
        fix = f"Declare check for typos or define the variable"
        super().__init__("UnknownVariable", content, line_num, line_content, fix)


class UnknownFunction(ParserError):
    def __init__(self, name:str, line:str|list, line_num:int):
        content = f"Function {name} is not defined."
        line_content = line if isinstance(line, str) else " ".join(line)
        fix = f"Declare check for typos or define the function"
        super().__init__("UnknownFunction", content, line_num, line_content, fix)

class WrongArgument(ParserError):
    def __init__(self, name:str, expected:str|list, line:str|list, line_num:int):
        content = f"Variable {name} expected a {expected} or a variable of type {expected}."
        line_content = line if isinstance(line, str) else " ".join(line)
        fix = f"Add two arguments of type {expected}"
        super().__init__("Wrong Argument", content, line_num, line_content, fix)

class WrongNumOfArguments(ParserError):
    def __init__(self, name:str, expected:str|list, line:str|list, line_num:int):
        content = f"Variable {name} expected a {expected} or aa variable of type {expected}."
        line_content = line if isinstance(line, str) else " ".join(line)
        fix = f"Add two arguments of type {expected}"
        super().__init__("Wrong Argument", content, line_num, line_content, fix)

class UnrecognisedKeyword(ParserError):
    def __init__(self, keyword:str, line:str|list, line_num:int):
        content = f"Unrecognised keybword {keyword}."
        line_content = line if isinstance(line, str) else " ".join(line)
        fix = f"Use a recognised keyword"
        super().__init__("Unrecognized keyword", content, line_num, line_content, fix)

class WrongReturnReturnType(ParserError):
    def __init__(self, name:str, var:str, expected:str, got:str,  line:str|list, line_num:int):
        content = f"Function {name} expected {expected} but variable {var} is a {got}."
        line_content = line if isinstance(line, str) else " ".join(line)
        fix = f"Uns a variable of type {expected}"
        super().__init__("Wrong Return Type", content, line_num, line_content, fix)



class WrongType(ParserError):
    def __init__(self, var:str, expected:str, got:str, action:str,  line:str|list, line_num:int):
        content = f"{action} expected {expected} but variable {var} is a {got}."
        line_content = line if isinstance(line, str) else " ".join(line)
        fix = f"Uns a variable of type {expected}"
        super().__init__("Wrong Return Type", content, line_num, line_content, fix)