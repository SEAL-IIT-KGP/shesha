Contained within are proof-of-concept codes for various scenarios mentioned in the paper: mixing of SIMD-Vector instructions, mixing of precision, or intermixing of AES-SIMD instructions.

Each folder contains a Makefile two targets: *perfmon* and *leak*. The *perfmon* target demonstrates the relevant performance counters (for Alder Lake) for the ASM snippet contained within *fuzz.S*. This target can be built by `make all` and run using `sudo ./fuzz`

Likewise, the target *leak* works on two files - *leak.c* and *fp.S*. The code contained within *leak.c* is responsible for setting up the flush-reload buffer, and attempting to leak a dummy string "This is a test to verify if it leaks", in line with similar analysis done in https://github.com/vusec/fpvi-scsb. This target can be built by `make all` and run using `sudo ./leak` (note that we need ring 3 sudo for perfmon analysis. Should the perfmon descriptors be removed, the actual flush-reload + our transient ASMs do not require sudo privileges to run). These experiments require huge page tables enabled, and thus can be done with `echo 16 | sudo tee  /proc/sys/vm/nr_hugepages 1>/dev/null`

Finally, we have also included sample runs of the *leak* target in subdirectory *sample_runs*, and a sample run of the *perfmon* target in *sample_perfmon*.

A sample run of *leak* target looks like:

0xADDR:
   COUNT: HEX (DEC)

where ADDR represents the address of the byte to leaked, COUNT represents the hits of the leaked byte in the flush-reload buffer, HEX represents the exact byte leaked, while DEC is the decimal representation of HEX. Below attached is one example (`aes_simd/sample_runs/run_2`). All sample runs are on Alder Lake.


0x0000000000402058 :
	00001000: 54 (T)

0x0000000000402059 :
	00001000: 68 (h)

0x000000000040205a :
	00001000: 69 (i)

0x000000000040205b :
	00000999: 73 (s)

0x000000000040205c :
	00001000: 20 ( )

0x000000000040205d :
	00001000: 69 (i)

0x000000000040205e :
	00001000: 73 (s)

0x000000000040205f :
	00001000: 20 ( )

0x0000000000402060 :
	00001000: 61 (a)

0x0000000000402061 :
	00000999: 20 ( )

0x0000000000402062 :
	00000999: 74 (t)

0x0000000000402063 :
	00001000: 65 (e)

0x0000000000402064 :
	00001000: 73 (s)

0x0000000000402065 :
	00001000: 74 (t)

0x0000000000402066 :
	00001000: 20 ( )

0x0000000000402067 :
	00001000: 74 (t)

0x0000000000402068 :
	00001000: 6f (o)

0x0000000000402069 :
	00000999: 20 ( )

0x000000000040206a :
	00000999: 76 (v)

0x000000000040206b :
	00001000: 65 (e)

0x000000000040206c :
	00001000: 72 (r)

0x000000000040206d :
	00001000: 69 (i)

0x000000000040206e :
	00001000: 66 (f)

0x000000000040206f :
	00001000: 79 (y)

0x0000000000402070 :
	00001000: 20 ( )

0x0000000000402071 :
	00001000: 74 (t)

0x0000000000402072 :
	00001000: 68 (h)

0x0000000000402073 :
	00001000: 61 (a)

0x0000000000402074 :
	00001000: 74 (t)

0x0000000000402075 :
	00001000: 20 ( )

0x0000000000402076 :
	00001000: 69 (i)

0x0000000000402077 :
	00001000: 73 (s)

0x0000000000402078 :
	00001000: 20 ( )

0x0000000000402079 :
	00001000: 6c (l)

0x000000000040207a :
	00001000: 65 (e)

0x000000000040207b :
	00001000: 61 (a)

0x000000000040207c :
	00000998: 6b (k)

0x000000000040207d :
	00001000: 73 (s)

## System Details

Architecture**:            x86_64                                                                                                               
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
