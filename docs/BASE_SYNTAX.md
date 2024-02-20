# Feluk langueage

## Datatypes:
usigned integer: u+size (`u8`, `u16`, `u32`, `u64`)

Arrays: `list:T:n`, where `T` is an unsigned integer type, and `n` the length of the list.

## Syntax:
### Function:

``` 
func type name type arg1 type arg2 ...
    [code]
```
The entrypoint of the program is the main function.

### Variable declaration:
```
def type name = value
```

### Modyfy variable:
```
mod name = value
mod name = value1 + value2
mod name = value1 - value2
mod name = value1 * value2
mod name = value1 / value2
mod name = value1 % value2
mod name = call func_name arg1 arg2 ...
```

### Conditionals
```
if condition {
    [code]
}
```
Allowed conditions:
```
arg == arg
arg != arg
arg < arg
arg <= arg
arg >= arg
```

### Loops
```
while condition {
    [code]
}
```
The conditions are the same as in a if condition


### function calling
```
call name1 arg1 arg2 arg3 ...
```

### returning
```
return x
```

### Inline assembly
Inline assembly is suported by putting it between `asm` tags:
```
asm 
    [some assembly code]
asm
```

You can also store the value of a register in a variable:
```
store [register] [variable]
```