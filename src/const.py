TYPES = ["u8", "u16", "u32", "u64", "none"]

SIZES = {
    "u8": 1,
    "u16": 2,
    "u32": 4,
    "u64": 8,
    "none": 0,
}

def get_part_size(vars:dict, var:str) -> int:
    if var in vars.keys():
        return SIZES[vars[var]["type"]]
    elif var.split(":")[0] in vars.keys():
        return get_array_var_size(vars, var)

def get_size(T) -> int:
    if T in SIZES.keys():
        return SIZES[T]
    elif T[:5] == "list:":
        _, T, num = T.split(":")
        return SIZES[T] * int(num) + 8

ASM_TYPES = {
    1: "BYTE",
    2: "WORD",
    4: "DWORD",
    8: "QWORD"
}

UNSIGNED = ["u8", "u16", "u32", "u64"]

EXPECTED = {
    "u8": ["u8", "char?"],
    "u16": ["u16"],
    "u32": ["u32"],
    "u64": ["u64"],
    "none": ["none"],
}

BUILTIN = {
    "new_line":{
        "return_type": "none",
        "args": [],
        "regs": []
    },
    "print_char": {
        "return_type": "none",
        "args": ["u8"],
        "regs": ["al"]
    },
    "print_u8": {
        "return_type": "none",
        "args": ["u8"],
        "regs": ["al"]
    },
    "print_u16": {
        "return_type": "none",
        "args": ["u16"],
        "regs": ["ax"]
    },
    "print_u32": {
        "return_type": "none",
        "args": ["u32"],
        "regs": ["eax"]
    },
    "print_u64": {
        "return_type": "none",
        "args": ["u64"],
        "regs": ["rax"]
    }
}

from data_types.array import get_array_var_size
