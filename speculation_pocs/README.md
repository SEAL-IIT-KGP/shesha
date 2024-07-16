## How to run the artifacts
Contained within are proof-of-concept codes for various scenarios mentioned in the paper: mixing of SIMD-Vector instructions, mixing of precision, and intermixing of AES-SIMD instructions.

Each folder contains a Makefile two targets: *perfmon* and *leak*. The *perfmon* target demonstrates the relevant performance counters (for Alder Lake) for the ASM snippet contained within *fuzz.S*. This target can be built by `make all` and run using `sudo ./fuzz`

Likewise, the target *leak* works on two files - *leak.c* and *fp.S*. The code contained within *leak.c* is responsible for setting up the flush-reload buffer, and attempting to leak a dummy string "This is a test to verify if it leaks". This target can be built by `make all` and run using `sudo ./leak` (note that we need ring 3 sudo for perfmon analysis. Should the perfmon descriptors be removed, the actual flush-reload + our transient ASMs do not require sudo privileges to run). These experiments require huge page tables enabled. This can be enabled using the following command: `echo 16 | sudo tee  /proc/sys/vm/nr_hugepages 1>/dev/null`

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
### SSE-AVX intermixing
Affected CPUs (tested): Intel 12, 13 gen client and Intel 4 gen Xeon processors
Operating System (tested): Ubuntu 20, Ubuntu 22
Hyperthreading required?: no

### precision intermixing
Affected CPUs (tested): Intel 12, 13 gen client and Intel 4 gen Xeon processors
Operating System (tested): Ubuntu 20, Ubuntu 22
Hyperthreading required?: no

### SSE-AES intermixing
Affected CPUs (tested): Intel 11, 12, 13 gen client and Intel 3, 4 gen Xeon processors
Operating System (tested): Ubuntu 20, Ubuntu 22
Hyperthreading required?: no
Special input required?: Works only with denormal numbers

## Resource Estimation:
For each artifact, it is expected to take around 15-30 minutes (depending on processor clock) to observe the leakage. The storage and memory usage is not significant.