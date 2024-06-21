global fuzz_instruction_extensions
align 64
fuzz_instruction_extensions:

;;;;;; AES-SIMD denormal arithmetic ;;;;;;;
   aesdeclast xmm4, xmm9
   mulss xmm4, xmm7
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

ret
