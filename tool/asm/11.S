;ASSISTS.SSE_AVX_MIX:29
global fuzz_instruction_extensions
align 64
fuzz_instruction_extensions:
VMOVLHPS XMM7, XMM2, XMM15
VPADDSB YMM1, YMM1, YMM7
VPSUBB YMM4, YMM14, YMM13
SQRTSS XMM14, XMM13
PHADDW XMM8, XMM3
VPMOVZXBD YMM9, XMM7
VPMAXUB YMM7, YMM13, YMM10
VPSUBB YMM7, YMM3, YMM0
VMAXPS XMM11, XMM10, XMM13
VDIVPD YMM0, YMM7, YMM11
VMOVUPD XMM12, XMM14
PHSUBW XMM8, XMM7
VPSRAW YMM1, YMM12, XMM8
VPMOVZXWQ YMM6, XMM3
VPCMPEQW YMM9, YMM11, YMM13
ANDPS XMM8, XMM9
PMADDWD XMM6, XMM3
MOVD XMM8, R8D
PSUBQ MM4, MM1
MOVQ2DQ XMM7, MM0
UNPCKHPS XMM9, XMM12
VPMAXUW YMM3, YMM4, YMM15
VSQRTPS XMM4, XMM2
VPSLLW XMM4, XMM6, XMM2
VORPD YMM10, YMM11, YMM3
VANDNPD XMM12, XMM8, XMM0
VPADDSB YMM8, YMM9, YMM13
VPADDUSW YMM5, YMM1, YMM1
PHSUBSW MM0, MM0
MOVSS XMM4, XMM4
SUBSS XMM9, XMM1
PSIGND MM0, MM3
PHSUBD MM6, MM4
PHADDW XMM0, XMM10
VPCMPGTD YMM10, YMM3, YMM0
CVTSD2SS XMM14, XMM13
SUBSS XMM4, XMM7
VANDPS YMM9, YMM12, YMM9
VPCMPGTD YMM2, YMM13, YMM13
VPHSUBSW XMM11, XMM13, XMM10
ret
