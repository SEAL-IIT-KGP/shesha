;ASSISTS.FP:32
global fuzz_instruction_extensions
align 64
fuzz_instruction_extensions:
MINPS XMM8, XMM13
PSHUFB XMM2, XMM13
SUBPS XMM1, XMM2
PAND XMM5, XMM15
MOVQ XMM12, XMM12
VPMADDWD YMM1, YMM8, YMM2
PAVGB XMM0, XMM1
RCPSS XMM8, XMM11
PUNPCKLWD XMM11, XMM4
VPSHUFB YMM14, YMM0, YMM8
PSIGNW XMM6, XMM13
VPUNPCKHQDQ YMM4, YMM5, YMM12
SFENCE
MAXSS XMM2, XMM14
VPSUBQ XMM0, XMM7, XMM9
VPSUBSB YMM6, YMM8, YMM6
PABSW XMM11, XMM7
VPMULUDQ XMM3, XMM15, XMM13
PADDSB XMM14, XMM1
MOVAPS XMM15, XMM8
VBROADCASTSS YMM3, XMM4
VPSLLW XMM15, XMM5, XMM12
PSIGNW XMM0, XMM0
PSIGND XMM14, XMM7
MOVAPS XMM11, XMM13
MOVAPS XMM15, XMM0
VANDNPD XMM13, XMM9, XMM4
SQRTPS XMM4, XMM1
ADDSS XMM8, XMM15
VPMINUD YMM10, YMM0, YMM3
VPUNPCKLBW XMM8, XMM10, XMM0
CVTSI2SS XMM15, R10D
MULSS XMM9, XMM9
VPSRLQ YMM1, YMM11, XMM10
PMULHUW XMM15, XMM1
PSRAW XMM1, XMM13
XORPS XMM1, XMM13
PSIGNB MM0, MM6
MINPS XMM2, XMM6
VPACKSSWB XMM13, XMM6, XMM6
ret
