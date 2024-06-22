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

Vulnerability Srbds:             Not affected

Vulnerability Tsx async abort:   Not affected


## System Details

Architecture:            x86_64                                                                                                               

  CPU op-mode(s):        32-bit, 64-bit                                                                                                       

  Address sizes:         46 bits physical, 48 bits virtual                                                                                    

  Byte Order:            Little Endian                                                                                                        

CPU(s):                  12                                                                                                                   

  On-line CPU(s) list:   0-11                                                                                                                 

Vendor ID:               GenuineIntel                                                                                                         

  Model name:            12th Gen Intel(R) Core(TM) i7-12700                                                                                  

    CPU family:          6                                                                                                                    

    Model:               151                                                                                                                  

    Thread(s) per core:  1                                                                                                                    

    Core(s) per socket:  12                                                                                                                   

    Socket(s):           1                                                                                                                    

    Stepping:            2                                                                                                                    

    CPU max MHz:         4900.0000

    CPU min MHz:         800.0000

    BogoMIPS:            4224.00

    Flags:               fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm p
                         be syscall nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc cpuid aper
                         fmperf tsc_known_freq pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 sdbg fma cx16 xtpr pdcm sse4_1 sse4_2
                          x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm 3dnowprefetch cpuid_fault epb ssbd ibrs
                          ibpb stibp ibrs_enhanced tpr_shadow vnmi flexpriority ept vpid ept_ad fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms i
                         nvpcid rdseed adx smap clflushopt clwb intel_pt sha_ni xsaveopt xsavec xgetbv1 xsaves split_lock_detect avx_vnni dthe
                         rm ida arat pln pts hwp hwp_notify hwp_act_window hwp_epp hwp_pkg_req umip pku ospke waitpkg gfni vaes vpclmulqdq tme
                          rdpid movdiri movdir64b fsrm md_clear serialize pconfig arch_lbr flush_l1d arch_capabilities


Virtualization features: 

  Virtualization:        VT-x

Caches (sum of all):     

  L1d:                   512 KiB (12 instances)

  L1i:                   512 KiB (12 instances)

  L2:                    12 MiB (9 instances)

  L3:                    25 MiB (1 instance)

NUMA:                    

  NUMA node(s):          1

  NUMA node0 CPU(s):     0-11

Vulnerabilities:         

  Gather data sampling:  Not affected

  Itlb multihit:         Not affected

  L1tf:                  Not affected

  Mds:                   Not affected

  Meltdown:              Not affected

  Mmio stale data:       Not affected

  Retbleed:              Not affected

  Spec rstack overflow:  Not affected

  Spec store bypass:     Mitigation; Speculative Store Bypass disabled via prctl and seccomp

  Spectre v1:            Mitigation; usercopy/swapgs barriers and __user pointer sanitization

  Spectre v2:            Mitigation; Enhanced IBRS, IBPB always-on, RSB filling, PBRSB-eIBRS SW sequence

  Srbds:                 Not affected

  Tsx async abort:       Not affected

