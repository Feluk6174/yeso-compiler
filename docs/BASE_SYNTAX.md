# Feluk langueage

## Datatypes:
usigned integer: u+size (`u8`, `u16`, `u32`, `u64`)

## Syntax:
### Function:

```feluk 
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

### if 
```
if condition {
    [code]
}
```

### while
```
while condition {
    [code]
}
```

### function calling
```
call name1 arg1 arg2 arg3 ...
```

### returning
```
return x
```