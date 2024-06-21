global fuzz_instruction_extensions
align 64
fuzz_instruction_extensions:

;;;;;; Intermixing precision ;;;;;;;
   haddpd xmm3, xmm4
   vaddsubps xmm13, xmm3
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

ret
