# HashPIM: Accelerating SHA-3 Algorithm with Memristive Stateful Logic
## Overview
This is a logic simulator to verify the theoretical results (latency, energy, and area) of HashPIM. This logic simulator models a memristive crossbar array with partitions, and then simulates running the HashPIM algorithm. The correctness of the operations is verified externally, and the number of cycles is measured, including initialization cycles.

`B. Oved, O. Leitersdorf, R. Ronen, and S. Kvatinsky, “HashPIM: High-Throughput SHA-3 via Memristive Digital Processing-in-Memory,” 2022.`

## Results
| Algorithm | Latency (Cycles) | Switches | Area (Memristors) | Partitions | Gates
| ---- | :----: | :----: | :----: | :----: | :----: |
| HashPIM | 3,494 | 119,571 | 1024<sup>2</sup> | 378 | XOR/NOR/NOT/OR |

The results for a single round:

| Step | Latency (Cycles) | Swithches |
| :---- | :----: | :----: |
| Theta | TBD | TBD |
| Rho | TBD | TBD |
| Pi | TBD | TBD |
| Chi | TBD | TBD |
| Iota | TBD | TBD |
| Total | 3,494 | 119,571 |

Note that the latency and the number of switches per a single unit, for one SHA3 round (out of 24), are evaluated.

## User Information
### Dependencies
In order to use the project, you will need:
1. python3
2. pytorch

### User Manual
Running `python TestHashPIM_SHA3-224.py` will run HashPIM for SHA3-224 on the simulator for a random 378 sample of bit arrays with a random size each (limited to size r-4). The simulator verifies the correctness
of the simulator output and counts the exact number of cycles and switches used. As HashPIM is deterministic, this cycle count is identical for all samples.

Running `python TestHashPIM_SHA3-256.py` will run HashPIM for SHA3-256 on the simulator for a random 378 sample of bit arrays with a random size each (limited to size r-4). The simulator verifies the correctness
of the simulator output and counts the exact number of cycles and switches used. As HashPIM is deterministic, this cycle count is identical for all samples.

Running `python TestHashPIM_SHA3-384.py` will run HashPIM for SHA3-384 on the simulator for a random 378 sample of bit arrays with a random size each (limited to size r-4). The simulator verifies the correctness
of the simulator output and counts the exact number of cycles and switches used. As HashPIM is deterministic, this cycle count is identical for all samples.

Running `python TestHashPIM_SHA3-512.py` will run HashPIM for SHA3-512 on the simulator for a random 378 sample of bit arrays with a random size each (limited to size r-4). The simulator verifies the correctness
of the simulator output and counts the exact number of cycles and switches used. As HashPIM is deterministic, this cycle count is identical for all samples.

## Implementation Details
The implementation is divided into the following files: 
1. `simulator.py`. Provides the interface for a memristive crossbar array.
2. `HashPIM.py`. Simulates the HashPIM algorithm for Secure Hash Algorithm-3 (SHA-3).
3. `TestHashPIM.py`. Tests the HashPIM algorithm for varying (r, digest)={(1152,224),(1088,256),(832,384),(576,512)}.
4. `Utilities.py`. Simplify the use of the logic functions within the memristive crossbar array.
