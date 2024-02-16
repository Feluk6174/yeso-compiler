import io

def generate_asm_start() -> str:
    return """
; Coded in YESO
; https://github.com/Feluk6174/yeso-compiler
global _start

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
    push r13
    mov r13, 1
    mov ah, 0
    mov bl, 10
    div bl
    mov bh, ah
    mov ah, 0
    div bl

    or al, 48
    cmp al, 48
    jne nstep0
    cmp r13, 1
    je next1
    nstep0:
    xor r13, r13
    call print_char
    
    next1:
    mov al, ah
    or al, 48
    cmp al, 48
    jne nstep1
    cmp r13, 1
    je next2
    nstep1:
    xor r13, r13
    call print_char
    
    next2:
    mov al, bh
    or al, 48
    call print_char
    
    pop r13
    pop rbx
    ret

print_u16:
    push rbx
    push rcx
    push r13
    mov r13, 1
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
    cmp al, 48
    jne nstep2
    cmp r13, 1
    je next3
    nstep2:
    xor r13, r13
    call print_char

    next3:
    shr rcx, 8
    mov al, cl
    or al, 48
    cmp al, 48
    jne nstep3
    cmp r13, 1
    je next4
    nstep3:
    xor r13, r13
    call print_char

    next4:
    shr rcx, 8
    mov al, cl
    or al, 48
    cmp al, 48
    jne nstep4
    cmp r13, 1
    je next5
    nstep4:
    xor r13, r13
    call print_char
    shr rcx, 8

    next5:
    mov al, cl
    or al, 48
    cmp al, 48
    jne nstep5
    cmp r13, 1
    je next6
    nstep5:
    xor r13, r13
    call print_char

    next6:
    shr rcx, 8
    mov al, cl
    or al, 48
    call print_char

    pop r13
    pop rcx
    pop rbx
    ret

print_u32:
    push rbx
    push rcx
    push rdx
    push r13

    mov r13, 1
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
    cmp al, 48
    jne nstep06
    cmp r13, 1
    je next06
    nstep06:
    xor r13, r13
    call print_char

    next06:
    mov al, dl
    or al, 48
    cmp al, 48
    jne nstep6
    cmp r13, 1
    je next7
    nstep6:
    xor r13, r13
    call print_char

    next7:
    mov al, cl
    or al, 48
    cmp al, 48
    jne nstep7
    cmp r13, 1
    je next8
    nstep7:
    xor r13, r13
    call print_char

    next8:
    shr rcx, 8
    mov al, cl
    or al, 48
    cmp al, 48
    jne nstep8
    cmp r13, 1
    je next9
    nstep8:
    xor r13, r13
    call print_char

    next9
    shr rcx, 8
    mov al, cl
    or al, 48
    cmp al, 48
    jne nstep9
    cmp r13, 1
    je next10
    nstep9:
    xor r13, r13
    call print_char

    next10:
    shr rcx, 8
    mov al, cl
    or al, 48
    cmp al, 48
    jne nstep10
    cmp r13, 1
    je next11
    nstep10:
    xor r13, r13
    call print_char

    next11:
    shr rcx, 8
    mov al, cl
    or al, 48
    cmp al, 48
    jne nstep11
    cmp r13, 1
    je next12
    nstep11:
    xor r13, r13
    call print_char

    next12:
    shr rcx, 8
    mov al, cl
    or al, 48
    cmp al, 48
    jne nstep12
    cmp r13, 1
    je next13
    nstep12:
    xor r13, r13
    call print_char

    next13:
    shr rcx, 8
    mov al, cl
    or al, 48
    cmp al, 48
    jne nstep13
    cmp r13, 1
    je next14
    nstep13:
    xor r13, r13
    call print_char

    next14:
    shr rcx, 8
    mov al, cl
    or al, 48
    call print_char

    pop r13
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
    push r13

    mov r13, 1

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
    cmp al, 48
    jne nstep14
    cmp r13, 1
    je next15
    nstep14:
    xor r13, r13
    call print_char

    next15:
    mov al, dl
    or al, 48
    cmp al, 48
    jne nstep15
    cmp r13, 1
    je next16
    nstep15:
    xor r13, r13
    call print_char

    next16:
    mov al, ch
    or al, 48
    cmp al, 48
    jne nstep16
    cmp r13, 1
    je next17
    nstep16:
    xor r13, r13
    call print_char

    next17:
    mov al, cl
    or al, 48
    cmp al, 48
    jne nstep17
    cmp r13, 1
    je next18
    nstep17:
    xor r13, r13
    call print_char

    next18:
    mov al, r9b
    or al, 48
    cmp al, 48
    jne nstep18
    cmp r13, 1
    je next20
    nstep18:
    xor r13, r13
    call print_char

    next20:
    shr r9, 8
    mov al, r9b
    or al, 48
    cmp al, 48
    jne nstep20
    cmp r13, 1
    je next21
    nstep20:
    xor r13, r13
    call print_char

    next21:
    shr r9, 8
    mov al, r9b
    or al, 48
    cmp al, 48
    jne nstep21
    cmp r13, 1
    je next22
    nstep21:
    xor r13, r13
    call print_char

    next22:
    shr r9, 8
    mov al, r9b
    or al, 48
    cmp al, 48
    jne nstep22
    cmp r13, 1
    je next24
    nstep22:
    xor r13, r13
    call print_char

    next24:
    shr r9, 8
    mov al, r9b
    or al, 48
    cmp al, 48
    jne nstep24
    cmp r13, 1
    je next25
    nstep24:
    xor r13, r13
    call print_char

    next25:
    shr r9, 8
    mov al, r9b
    or al, 48
    cmp al, 48
    jne nstep25
    cmp r13, 1
    je next26
    nstep25:
    xor r13, r13
    call print_char

    next26:
    shr r9, 8
    mov al, r9b
    or al, 48
    cmp al, 48
    jne nstep26
    cmp r13, 1
    je next27
    nstep26:
    xor r13, r13
    call print_char

    next27:
    shr r9, 8
    mov al, r9b
    or al, 48
    cmp al, 48
    jne nstep27
    cmp r13, 1
    je next28
    nstep27:
    xor r13, r13
    call print_char

    next28:
    mov al, r8b
    or al, 48
    cmp al, 48
    jne nstep28
    cmp r13, 1
    je next29
    nstep28:
    xor r13, r13
    call print_char

    next29:
    shr r8, 8
    mov al, r8b
    or al, 48
    cmp al, 48
    jne nstep29
    cmp r13, 1
    je next30
    nstep29:
    xor r13, r13
    call print_char

    next30:
    shr r8, 8
    mov al, r8b
    or al, 48
    cmp al, 48
    jne nstep30
    cmp r13, 1
    je next31
    nstep30:
    xor r13, r13
    call print_char

    next31:
    shr r8, 8
    mov al, r8b
    or al, 48
    cmp al, 48
    jne nstep31
    cmp r13, 1
    je next32
    nstep31:
    xor r13, r13
    call print_char

    next32:
    shr r8, 8
    mov al, r8b
    or al, 48
    cmp al, 48
    jne nstep32
    cmp r13, 1
    je next33
    nstep32:
    xor r13, r13
    call print_char

    next33:
    shr r8, 8
    mov al, r8b
    or al, 48
    cmp al, 48
    jne nstep33
    cmp r13, 1
    je next34
    nstep33:
    xor r13, r13
    call print_char

    next34:
    shr r8, 8
    mov al, r8b
    or al, 48
    cmp al, 48
    jne nstep34
    cmp r13, 1
    je next35
    nstep34:
    xor r13, r13
    call print_char

    next35:
    shr r8, 8
    mov al, r8b
    or al, 48
    call print_char

    pop r13
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

