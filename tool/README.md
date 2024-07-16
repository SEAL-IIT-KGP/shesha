# Shesha

Contains the main implementation of the particle swarm optimizer of "Shesha: Multi-head Microarchitectural Leakage Discovery in new-generation Intel Processors" presented at USENIX Security '24.


## Directory structure

1. `shesha.py`  : Contains the optimizer loop

2. `msr.config` : Configuration of events observed (refer to [Intel perfmon events](https://perfmon-events.intel.com/) to modify). By default, `msr.config` is tuned for Alder Lake.

3. `optimizer.config` : Configuration for the optimizer (refer to [Section full version of the paper](https://arxiv.org/abs/2406.06034) for details on tuning these).

4. `boilerplate.c` and `fuzz.S` : Interfaced with `shesha.py` to discover bad speculation

5. `asm/` : Where the optimizer dumps ASMs in which speculation is discovered

## Setup

First, install the necessary packages through `pip3 install -r requirements.txt`. Note that `xml.etree`, `argparse`, `os`, `subprocess`, `random`, and `re` are part of standard Python library, and hence are implicitly installed with Python 3.x. We have tested this tool with **Python 3.10.12**.

Then, use `bash setup.sh` to:

1. Download [instructions.xml](https://uops.info/). This is used by `shesha.py` to define the search space for the optimizer.

2. Install `gcc` and `nasm`. We used `gcc-11.4.0` and `nasm-2.15.05` for our tests.

3. Install the Intel MSR debug module

4. Check the available extensions on the system. This helps in choosing the right flags for `shesha.py`.


## Example run

The following sequence of commands is used to test `shesha.py` on `Intel(R) Core(TM) i7-12700` with microcode version `0x34`, with enabled extensions `-avx -avx2 -sse -ssse3 -sse2`

1. Install required dependencies : `pip3 install -r requirements.txt`

2. Setup : `bash setup.sh`

3. Tweek optimizer configuration in `optimizer.config`

   - `POPULATION_SIZE` : Number of particles in the population 
   - `COGNITIVE_BETA`  : Probability of exploration in the cognitive phase
   - `COGNITIVE_GAMMA` : Probability of exploitation in the cognitive phase
   - `MIXED_BETA`      : Probability of exploration in the mixed phase
   - `MIXED_GAMMA`     : Probability of exploitation in the mixed phase
   - `THRESHOLD`       : Number of iterations when to switch the optimizer from the cognitive phase to the mixed phase
   - `DUMP_ASM`        : Number of iterations post which the ASM of the particles in population are dumped

4. Run `python3 shesha.py -h` to dump all the available extensions. The only required argument is `--num-instructions`, or the number of instructions in the ASM of each particle.

5. In this example, we focus on SIMD and Vector extensions, hence we run `python3 shesha.py --num-instructions 40 -avx -avx2 -sse -ssse3 -sse2`

  This command runs Shesha on a search space of `586` instructions, where each particle manages `40` instructions.

6. Shesha is not expected to terminate. Use `kill` to manually terminate. From our observations, around 400-500 generations of evolution are sufficient to uncover the major types of bad speculation (and further reduce their dimensionality).

**Note**: Initially, the user may observe **make: *** [Makefile:4: all] Error 139**. This is because Shesha's initialization may have generated an ASM that SEGFAULTs. This does not hamper the convergence, since after a while, Shesha converges on the correctly functioning ASM.

## Analyse output

The tool dumps set of instructions into the `asm\` directory in which particular bad speculation event is triggered. A sample ASM file looks as following:
```
;ASSISTS.SSE_AVX_MIX:23
global fuzz_instruction_extensions
align 64
fuzz_instruction_extensions:
VPAVGB XMM3, XMM2, XMM11
ADDPS XMM5, XMM2
MOVD XMM9, R15D
VBROADCASTSD YMM0, XMM12
MOVQ XMM1, XMM14
PSHUFB MM2, MM4
PSIGNB MM5, MM6
VPSLLVD YMM8, YMM9, YMM4
VPMOVSXBW YMM5, XMM10
...
ret
``` 
The first line (commented using `;`) denotes the type of bad speculation event triggered by the sequences of instructions in the particular file along with the total number of such events encountered. As the tool runs, it passes through three phases (refer to the [paper](https://www.usenix.org/conference/usenixsecurity24/presentation/chakraborty) for details on each phase): Initialization, Cognitive and Mixed. In the Mixed phase, dimentionality reduction operation is performed (along with PSO search) that removes non-participating instructions from the set of instructions. In other words, after multiple iterations of Mixed phase, some of the non-participating instructions are removed from the asm files, making the list smaller. However, multiple combination of instructions could trigger the same bad speculation event, as evident from the example where `23` such events have been triggered by the instructions. To segregate the optimal set of instruction that could trigger the same bad speculation event, the user could manually remove some of the instructions to make smaller subsets as long as such subsets triggers the same event. 

To test if a set of instruction display a particular bad speculation event, one can use `perfmon.c` from the appropriate directory. For example, we can observe from the example above that the particular sequence of instruction triggered multiple `SSE_AVX_MIX` assists. To segregate the sub-sets of instructions that could optimally trigger the same `SSE_AVX_MIX` assists, the user can replace the code snippet in the `fuzz.S` file inside `/speculation_pocs/simd_vector/` and execute `sudo ./fuzz` (More details on executing `fuzz` can be found in [speculation_pocs](../speculation_pocs/README.md)). The output of `fuzz` shows the number and types of bad speculation events triggered by the given instruction sequence.

## Resource Estimation:
To run the tool, it is expected to take around 3 hours (depending on processor clock) to obtain signifant number of instruction sequences (as asm files) triggering different bad speculation events. The longer the tool runs, the amount of dimentionality reduction of the instruction sequences increases. Available disk space of around 5GB and 16GB RAM is preferred. 

