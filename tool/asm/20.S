;ASSISTS.SSE_AVX_MIX:28
global fuzz_instruction_extensions
align 64
fuzz_instruction_extensions:
VPCMPGTD YMM11, YMM1, YMM13
PHSUBSW XMM13, XMM7
VSQRTPD XMM0, XMM6
PHADDD XMM13, XMM6
VPMULUDQ XMM11, XMM1, XMM7
PMULHRSW XMM2, XMM11
VBLENDVPS XMM11, XMM11, XMM11, XMM0
PSRAD XMM0, XMM11
VPADDB XMM9, XMM8, XMM12
SQRTPS XMM3, XMM0
VPMINSD YMM3, YMM8, YMM7
CVTSD2SS XMM13, XMM10
VPSUBSW XMM11, XMM1, XMM5
PSUBD XMM9, XMM7
VPSRLW YMM9, YMM14, XMM1
CVTSI2SS XMM14, R8D
VPADDB YMM15, YMM12, YMM14
SQRTPS XMM13, XMM6
VADDSUBPS YMM14, YMM4, YMM0
MAXPD XMM10, XMM0
VMAXSS XMM11, XMM12, XMM6
SQRTPS XMM13, XMM6
VPMULUDQ YMM2, YMM9, YMM14
CVTTSS2SI ESI, XMM6
CVTSI2SS XMM15, R12
VPSUBUSB YMM9, YMM12, YMM5
MOVQ2DQ XMM13, MM0
VCVTPD2PS XMM7, YMM2
SQRTPS XMM13, XMM6
VPMOVZXWQ XMM10, XMM11
ret