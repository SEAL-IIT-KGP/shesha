;ASSISTS.SSE_AVX_MIX:23
global fuzz_instruction_extensions
align 64
fuzz_instruction_extensions:
VMOVDQU XMM10, XMM11
RCPSS XMM11, XMM6
MAXSD XMM8, XMM11
VPERMPS YMM9, YMM5, YMM7
SFENCE
RCPPS XMM15, XMM11
VANDNPS XMM8, XMM1, XMM5
VPAVGW XMM14, XMM2, XMM13
PHADDW MM2, MM6
PADDW XMM2, XMM9
VDIVPD YMM0, YMM0, YMM7
PHSUBW MM0, MM5
MOVQ XMM1, RAX
PADDB XMM0, XMM9
MULSS XMM5, XMM15
RCPSS XMM3, XMM6
VMOVUPS XMM9, XMM8
VPHSUBD YMM12, YMM5, YMM15
CVTTSS2SI RAX, XMM6
PABSD XMM12, XMM0
VPAVGW YMM9, YMM9, YMM11
VADDPD YMM8, YMM13, YMM9
PSIGNB XMM14, XMM0
RSQRTSS XMM6, XMM3
PSIGNW XMM14, XMM13
VPADDW YMM1, YMM12, YMM14
ANDNPS XMM10, XMM2
PMULHUW XMM15, XMM2
PHADDW XMM5, XMM3
VPSUBUSB XMM2, XMM5, XMM14
MOVUPS XMM3, XMM10
PHSUBSW MM2, MM7
PAVGW XMM15, XMM13
ADDSS XMM12, XMM6
PSIGNW XMM5, XMM12
PSIGNB MM0, MM3
PHSUBSW XMM11, XMM13
UNPCKLPS XMM9, XMM8
VPMAXSB XMM2, XMM9, XMM4
PSIGNW XMM1, XMM2
ret
