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
2. SILENT_MODE : Set `1` to observe the leaked output on the terminal

### Optional
This parameter is only available for the FMA PoC in `fma_source_leak_artifact`. Since AMS algorithm in `ams52_artifact` uses AVX-512 instructions, the system needs to have AVX-512 support to run the artifact.
3. AVX_512 : Set `1` if AVX_512 extension is available on the machine (default)


## System Details
Affected CPUs (tested): Intel 11th Gen Intel(R) Core(TM) i5-11500
Operating System (tested): Ubuntu 22
Hyperthreading required?: yes
**Note:** *The vulnerability is mitigated by GDS (Gather Data Sampling) mitigation. If your processor is not vulnerable to GDS, you might not be able to observe the FMA leakage. However, all other leakages presented in this repository shall work as they are not affected by GDS mitigation.*

## Resource Estimation:
For each artifact, it is expected to take around 15-30 minutes (depending on processor clock) to observe the leakage. The storage and memory usage is not significant.