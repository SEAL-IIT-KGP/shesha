# shesha

This repository contains the accompanying code for "Shesha: Multi-head Microarchitectural Leakage Discovery in new-generation Intel Processors" presented at USENIX Security Symposium, 2024.

## Directory Structure

1. `tool`: Contains the optimizer code with details on tuning and executing the same. This shall reproduce results from Section 3 and Section 5 of the [paper (full version)](https://arxiv.org/pdf/2406.06034)

2. `speculation_pocs`: Contains code triggering the various avenues of bad speculation unearthed by Shesha. This shall reproduce results from Section 4, Section 6, and Section 7 of the [paper (full version)](https://arxiv.org/pdf/2406.06034)

3. `fma_data_leak`: Contains code triggering speculation in FMA execution unit, and eventual data leak from FMA execution unit to the AVX execution unit. This shall reproduce results from Section 8 of the [paper (full version)](https://arxiv.org/pdf/2406.06034).

Please note that `speculation_pocs` was tested on Alder lake (12th Gen Intel(R) Core(TM) i7-12700 : Microcode version 0x34), while `fma_data_leak` was tested on Rocket Lake (11th Gen Intel(R) Core(TM) i5-11500 : Microcode version 0x57). Also note that the `msr.config` in `tool` is configured to Alder Lake. If you are running the tool or PoCs on any other system, please adapt accordingly (the appropriate README captures the steps of adaptation).
