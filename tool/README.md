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
