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
