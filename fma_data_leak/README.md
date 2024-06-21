Proof of Concept codes to test transient leakage of data from FMA execution engine to 
speculatively executing AVX instructions.

## Structure

1. fma_source_leak_artifact : PoC for section 8.2.2 in the paper
2. ams52_artifact : PoC for section 8.3.1 in the paper

## Usage

In either of the subdirectories, 

1. make clean
2. make
3. ./fma_leak 0 0 4 

(change the third argument from 1-8 to control the length of leakage; lower the number, faster the signal, albeit with more noise)

## Expected output:

25 25 25 25 25 25 25 25 %%%%%%%% 8

25 25 25 25 25 25 25 25 %%%%%%%% 8

25 25 25 25 25 25 25 25 %%%%%%%% 8

25 25 25 25 25 25 25 25 %%%%%%%% 8

25 25 25 25 25 25 25 25 %%%%%%%% 8

25 25 25 25 25 25 25 25 %%%%%%%% 8

25 25 25 25 25 25 25 25 %%%%%%%% 8

This designates leaking victim data `0x25` from co-located thread on the same core. 
Change `address_fma` in `asm.S` in either sub-directories from `0x25` to some other data in order to 
modify the victim's leaked data.

For example, set `address_fma` to `0xfa` to reproduce results from the paper

## Configuration options

Change the following options in config.h as per requirement:

1. CPU_VICTIM / CPU_ATTACKER : set these to co-located hyperthreads 
2. AVX_512 : Set `1` if AVX_512 extension is available on the machine
3. SILENT_MODE : Set `1` to observe the leaked output on the terminal


## System details:

Architecture:                    x86_64

CPU op-mode(s):                  32-bit, 64-bit

Address sizes:                   39 bits physical, 48 bits virtual

Byte Order:                      Little Endian

CPU(s):                          12

On-line CPU(s) list:             0-11

Vendor ID:                       GenuineIntel

Model name:                      11th Gen Intel(R) Core(TM) i5-11500 @ 2.70GHz

Microcode version:               0x57

CPU family:                      6

Model:                           167

Thread(s) per core:              2

Core(s) per socket:              6

Socket(s):                       1

Stepping:                        1

CPU max MHz:                     4600.0000

CPU min MHz:                     800.0000

BogoMIPS:                        5424.00

Flags:                           fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc cpuid aperfmperf tsc_known_freq pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm 3dnowprefetch cpuid_fault epb invpcid_single ssbd ibrs ibpb stibp ibrs_enhanced tpr_shadow vnmi flexpriority ept vpid ept_ad fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid mpx avx512f avx512dq rdseed adx smap avx512ifma clflushopt intel_pt avx512cd sha_ni avx512bw avx512vl xsaveopt xsavec xgetbv1 xsaves dtherm ida arat pln pts hwp hwp_notify hwp_act_window hwp_epp hwp_pkg_req avx512vbmi umip pku ospke avx512_vbmi2 gfni vaes vpclmulqdq avx512_vnni avx512_bitalg avx512_vpopcntdq rdpid fsrm md_clear flush_l1d arch_capabilities

Virtualization:                  VT-x

L1d cache:                       288 KiB (6 instances)

L1i cache:                       192 KiB (6 instances)

L2 cache:                        3 MiB (6 instances)

L3 cache:                        12 MiB (1 instance)

NUMA node(s):                    1

NUMA node0 CPU(s):               0-11

Vulnerability Itlb multihit:     Not affected

Vulnerability L1tf:              Not affected

Vulnerability Mds:               Not affected

Vulnerability Meltdown:          Not affected

Vulnerability Mmio stale data:   Mitigation; Clear CPU buffers; SMT vulnerable

Vulnerability Retbleed:          Mitigation; Enhanced IBRS

Vulnerability Spec store bypass: Mitigation; Speculative Store Bypass disabled via prctl

Vulnerability Spectre v1:        Mitigation; usercopy/swapgs barriers and __user pointer sanitization

Vulnerability Spectre v2:        Mitigation; Enhanced IBRS, IBPB conditional, RSB filling, PBRSB-eIBRS SW sequence

Vulnerability Srbds:             Not affected

Vulnerability Tsx async abort:   Not affected
