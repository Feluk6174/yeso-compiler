import io

def generate_asm_start() -> str:
    return """global _start

section .data
    mem: times 10000 db 0
    alloc: times 100 dd 0
    mem_fi dd 0
    p_buf_ptr: dq 0
    p_buf: times 100 db 0

section .text

print_buffer:
    push rcx
    push rax
    push rsi
    push rdi
    push r11

    mov rax, 1          ; syscall for syswrite
    mov rdi, 1          ; stdout file descriptor
    mov rsi, p_buf      ; bytes to write (by reference?)
    mov rdx, rbx        ; number of bytes to write
    syscall             ; call syscall

    pop r11
    pop rdi
    pop rsi
    pop rax
    pop rcx
    ret

print_char:
    push rbx
    mov rsi, QWORD[p_buf_ptr]
    mov BYTE[p_buf+rsi], al
    inc rsi
    mov QWORD[p_buf_ptr], rsi

    cmp rsi, 100
    jne fi_print_char
    mov rbx, 100
    call print_buffer
    xor rbx, rbx
    mov [p_buf_ptr], rbx
    fi_print_char:
    pop rbx
    ret

new_line:
    push rax
    mov al, 10
    call print_char
    pop rax
    ret

print_u8:
    push rbx

    mov ah, 0
    mov bl, 10
    div bl
    mov bh, ah
    mov ah, 0
    div bl

    or al, 48
    call print_char

    mov al, ah
    or al, 48
    call print_char

    mov al, bh
    or al, 48
    call print_char

    pop rbx
    ret

print_u16:
    push rbx
    push rcx

    mov bx, 10

    mov dx, 0
    div bx
    mov cl, dl
    shl rcx, 8
    
    mov dx, 0
    div bx
    mov cl, dl
    shl rcx, 8

    mov dx, 0
    div bx
    mov cl, dl
    shl rcx, 8

    mov dx, 0
    div bx
    mov cl, dl
    shl rcx, 8

    mov dx, 0
    div bx
    mov cl, dl

    mov al, cl
    or al, 48
    call print_char
    shr rcx, 8

    mov al, cl
    or al, 48
    call print_char
    shr rcx, 8

    mov al, cl
    or al, 48
    call print_char
    shr rcx, 8

    mov al, cl
    or al, 48
    call print_char
    shr rcx, 8

    mov al, cl
    or al, 48
    call print_char

    pop rcx
    pop rbx
    ret

print_u32:
    push rbx
    push rcx
    push rdx

    mov ebx, 10

    mov edx, 0
    div ebx
    mov cl, dl
    shl rcx, 8

    mov edx, 0
    div ebx
    mov cl, dl
    shl rcx, 8

    mov edx, 0
    div ebx
    mov cl, dl
    shl rcx, 8

    mov edx, 0
    div ebx
    mov cl, dl
    shl rcx, 8

    mov edx, 0
    div ebx
    mov cl, dl
    shl rcx, 8

    mov edx, 0
    div ebx
    mov cl, dl
    shl rcx, 8

    mov edx, 0
    div ebx
    mov cl, dl
    shl rcx, 8

    mov edx, 0
    div ebx
    mov cl, dl
    
    mov edx, 0
    div ebx

    or al, 48
    call print_char

    mov al, dl
    or al, 48
    call print_char

    mov al, cl
    or al, 48
    call print_char
    shr rcx, 8

    mov al, cl
    or al, 48
    call print_char
    shr rcx, 8

    mov al, cl
    or al, 48
    call print_char
    shr rcx, 8

    mov al, cl
    or al, 48
    call print_char
    shr rcx, 8

    mov al, cl
    or al, 48
    call print_char
    shr rcx, 8

    mov al, cl
    or al, 48
    call print_char
    shr rcx, 8

    mov al, cl
    or al, 48
    call print_char
    shr rcx, 8

    mov al, cl
    or al, 48
    call print_char

    pop rdx
    pop rcx
    pop rbx
    ret


print_u64:
    push rbx
    push rcx
    push rdx
    push r8
    push r9

    mov rbx, 10

    mov rdx, 0
    div rbx
    mov r8b, dl
    shl r8, 8

    mov rdx, 0
    div rbx
    mov r8b, dl
    shl r8, 8

    mov rdx, 0
    div rbx
    mov r8b, dl
    shl r8, 8

    mov rdx, 0
    div rbx
    mov r8b, dl
    shl r8, 8

    mov rdx, 0
    div rbx
    mov r8b, dl
    shl r8, 8

    mov rdx, 0
    div rbx
    mov r8b, dl
    shl r8, 8

    mov rdx, 0
    div rbx
    mov r8b, dl
    shl r8, 8

    mov rdx, 0
    div rbx
    mov r8b, dl

    mov rdx, 0
    div rbx
    mov r9b, dl
    shl r9, 8

    mov rdx, 0
    div rbx
    mov r9b, dl
    shl r9, 8

    mov rdx, 0
    div rbx
    mov r9b, dl
    shl r9, 8

    mov rdx, 0
    div rbx
    mov r9b, dl
    shl r9, 8

    mov rdx, 0
    div rbx
    mov r9b, dl
    shl r9, 8

    mov rdx, 0
    div rbx
    mov r9b, dl
    shl r9, 8

    mov rdx, 0
    div rbx
    mov r9b, dl
    shl r9, 8

    mov rdx, 0
    div rbx
    mov r9b, dl

    mov rdx, 0
    div rbx
    mov cl, dl

    mov rdx, 0
    div rbx
    mov ch, dl

    mov rdx, 0 
    div rbx

    or al, 48
    call print_char

    mov al, dl
    or al, 48
    call print_char

    mov al, ch
    or al, 48
    call print_char

    mov al, cl
    or al, 48
    call print_char

    mov al, r9b
    or al, 48
    call print_char
    shr r9, 8

    mov al, r9b
    or al, 48
    call print_char
    shr r9, 8

    mov al, r9b
    or al, 48
    call print_char
    shr r9, 8

    mov al, r9b
    or al, 48
    call print_char
    shr r9, 8

    mov al, r9b
    or al, 48
    call print_char
    shr r9, 8

    mov al, r9b
    or al, 48
    call print_char
    shr r9, 8

    mov al, r9b
    or al, 48
    call print_char
    shr r9, 8

    mov al, r9b
    or al, 48
    call print_char

    mov al, r8b
    or al, 48
    call print_char
    shr r8, 8

    mov al, r8b
    or al, 48
    call print_char
    shr r8, 8

    mov al, r8b
    or al, 48
    call print_char
    shr r8, 8

    mov al, r8b
    or al, 48
    call print_char
    shr r8, 8

    mov al, r8b
    or al, 48
    call print_char
    shr r8, 8

    mov al, r8b
    or al, 48
    call print_char
    shr r8, 8

    mov al, r8b
    or al, 48
    call print_char
    shr r8, 8

    mov al, r8b
    or al, 48
    call print_char

    
    pop r9
    pop r8
    pop rdx
    pop rcx
    pop rbx
    ret
    
panic_program:
    mov rbx, QWORD[p_buf_ptr]
    call print_buffer

    mov rax, 60
    mov rdi, 120
    syscall

_start:
    call main
    ;end execution
    
    mov rbx, QWORD[p_buf_ptr]
    call print_buffer

    mov rax, 60
    mov rdi, 0
    syscall
"""


def get_register(letter:str|int, size:int) -> str:
    if isinstance(letter, str):
        sizes = {
            1: ["", "l"],
            2: ["", "x"],
            4: ["e", "x"],
            8: ["r", "x"]
        }
        return sizes[size][0]+letter+sizes[size][1]

    elif isinstance(letter, int):
        letter = str(letter)
        sizes = {
            1: "b",
            2: "w",
            4: "d",
            8: ""
        }
        return "r"+letter+sizes[size]

