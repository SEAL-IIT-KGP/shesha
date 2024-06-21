global fuzz_instruction_extensions
align 64
fuzz_instruction_extensions:

;;;;;; SIMD-Vector transition ;;;;;;
    vxorpd ymm10, ymm10, ymm10
    xorpd xmm11, xmm11
    vaddpd ymm10, ymm10, ymm0
    vaddpd ymm11, ymm11, ymm1
    divsd xmm10, xmm11
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

ret
