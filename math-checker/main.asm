global _start

section .data
    buf times 10 db 0
    good_msg db 'A+'
    fail_msg db 'F'

section .text
_start:
    mov eax, 3
    mov ebx, 0
    mov ecx, buf
    mov edx, 10
    int 0x80

    ;check input[1] * 5 == 40
    movzx eax, byte [buf+1]
    sub eax, '0'
    imul eax, eax, 5
    cmp al, 40
    jne exit
    push eax           

    ; check (((input[2] * 2) << 3) + 2) // 26 == 5
    ; basically if input[2] == 8
    movzx eax, byte [buf+2]
    sub eax, '0'
    mov ecx, 2
    mul ecx 
    shl eax, 3
    add eax, 2
    mov ecx, 0x1a
    xor edx, edx
    idiv ecx
    cmp eax, 5
    jne exit
    cmp edx, 0
    jne exit

    ; simple check if input[0] == 1
    movzx eax, byte [buf]
    cmp eax, '1'
    jne exit
    
    ; store input[3] and input[4] as one 2-digit number
    movzx eax, byte [buf+3]
    sub eax, '0'
    mov ecx, 0xa
    mul ecx
    mov ebx, eax
    movzx eax, byte [buf+4]
    sub eax, '0'
    add ebx, eax
    
    ; add the earlier pushed value (should be 40)
    xor eax, eax
    pop eax
    add eax, ebx

    ; check if (input[3:4] + 40) // 19 == 7
    ; essentially if input[3:4] == 93
    mov ecx, 19
    xor edx, edx
    idiv ecx
    cmp eax, 7
    jne exit
    cmp edx, 0
    jne exit

    ; lazy so i copied the same check over to the next 5 digits

    ;check input[6] * 5 == 40
    movzx eax, byte [buf+1+5]
    sub eax, '0'
    imul eax, eax, 5
    cmp al, 40
    jne exit
    push eax           

    ; check (((input[7] * 2) << 3) + 2) // 26 == 5
    ; basically if input[7] == 8
    movzx eax, byte [buf+2+5]
    sub eax, '0'
    mov ecx, 2
    mul ecx 
    shl eax, 3
    add eax, 2
    mov ecx, 0x1a
    xor edx, edx
    idiv ecx
    cmp eax, 5
    jne exit
    cmp edx, 0
    jne exit

    ; simple check if input[5] == 1
    movzx eax, byte [buf+5]
    cmp eax, '2'
    jne exit
    
    ; store input[8] and input[9] as one 2-digit number
    movzx eax, byte [buf+3+5]
    sub eax, '0'
    mov ecx, 0xa
    mul ecx
    mov ebx, eax
    movzx eax, byte [buf+4+5]
    sub eax, '0'
    add ebx, eax
    
    ; add the earlier pushed value (should be 40)
    xor eax, eax
    pop eax
    add eax, ebx

    ; check if (input[3:4] + 40) // 19 == 7
    ; essentially if input[3:4] == 93
    mov ecx, 19
    xor edx, edx
    idiv ecx
    cmp eax, 7
    jne exit
    cmp edx, 0
    jne exit

    jmp end

print_newline:
    mov eax, 4
    mov ebx, 1
    mov DWORD [buf], 0xa
    mov ecx, buf
    mov edx, 1
    int 0x80
    ret

end:
    mov eax, 4
    mov ebx, 1
    mov ecx, good_msg
    mov edx, 2
    int 0x80

    call print_newline

    mov ebx, 0
    mov eax, 1
    int 0x80

exit:
    mov eax, 4
    mov ebx, 1
    mov ecx, fail_msg
    mov edx, 1
    int 0x80

    call print_newline

    mov ebx, 1
    mov eax, 1
    int 0x80