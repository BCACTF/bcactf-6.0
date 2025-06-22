section .data
    prompt      db  "Input: ", 0
    prompt_len  equ $ - prompt

    flag_path   db  "./flag.txt", 0
    flag_len    equ 35
    flag        times flag_len db 0

    newline db 0xA
    buf db "0x00000000", 0  ; Placeholder buffer for address

section .text
    global _start

_start:
    ; Get the address of _start (or any label)
    mov eax, _start

    ; Save EAX (the address) to be converted to hex string
    push eax
    mov esi, buf + 2  ; Skip '0x'
    mov ecx, 8        ; 8 hex digits

.convert_loop:
    pop eax
    push eax          ; keep original for next iteration
    rol eax, 4
    and al, 0xF
    cmp al, 10
    jl .digit
    add al, 'A' - 10
    jmp .store
.digit:
    add al, '0'
.store:
    mov [esi], al
    inc esi
    loop .convert_loop

    ; write(1, buf, 10)
    mov eax, 4          ; sys_write
    mov ebx, 1          ; stdout
    mov ecx, buf
    mov edx, 10         ; length of '0x' + 8 hex digits
    int 0x80

    ; write(1, newline, 1)
    mov eax, 4
    mov ebx, 1
    mov ecx, newline
    mov edx, 1
    int 0x80

    ; write(1, prompt, prompt_len)
    mov eax, 4          ; sys_write
    mov ebx, 1          ; stdout
    mov ecx, prompt
    mov edx, prompt_len
    int 0x80

    ; open("./flag.txt", O_RDONLY)
    mov eax, 5              ; sys_open
    mov ebx, flag_path      ; filename
    mov ecx, 0              ; O_RDONLY
    int 0x80
    mov esi, eax            ; save fd in esi

    ; read(fd, flag, flag_len)
    mov eax, 3              ; sys_read
    mov ebx, esi            ; fd
    mov ecx, flag           ; buffer
    mov edx, flag_len       ; count
    int 0x80
    mov edi, eax            ; save number of bytes read in edi

    ; close(fd)
    mov eax, 6              ; sys_close
    mov ebx, esi            ; fd
    int 0x80

    ; Call function
    call func
    jmp exit

func:
    push ebp
    mov ebp, esp
    sub esp, 100

    mov eax, 3          ; sys_read
    mov ebx, 0          ; stdin
    mov ecx, esp        
    mov edx, 200        
    int 0x80

    mov esp, ebp
    pop ebp
    ret

win:
    mov eax, 4    
    mov ebx, 1    
    mov ecx, flag 
    mov edx, flag_len  
    int 0x80

exit:
    mov eax, 1
    xor ebx, ebx
    int 0x80