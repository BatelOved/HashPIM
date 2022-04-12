# HashPIM: Accelerating SHA-3 Algorithm with Memristive Stateful Logic
## Overview
This is a logic simulator to verify the theoretical results (latency, energy, and area) of HashPIM. This logic simulator models a memristive crossbar array with partitions, and then simulates running the HashPIM algorithm. The correctness of the operations is verified externally, and the number of cycles is measured, including initialization cycles.

`B. Oved, O. Leitersdorf, R. Ronen, and S. Kvatinsky, “HashPIM: High-Throughput SHA-3 via Memristive Digital Processing-in-Memory,” 2022.`

## Results
| Algorithm | Latency (Cycles) | Gates | Area (Memristors) | Partitions | Gates
| ---- | :----: | :----: | :----: | :----: | :----: |
| HashPIM | 3,494 | 119,571 | 1024<sup>2</sup> | 378 | XOR/NOR/NOT/OR |

The results for a single unit, for one SHA3 round (out of 24):

| Step | Latency (Cycles) | Gates |
| :---- | :----: | :----: |
| Theta | 330 | 15,127 |
| Rho | 2,911 | 82,300 |
| Pi | 81 | 6,976 |
| Chi | 140 | 14,720 |
| Iota | 32 | 448 |
| Total | 3,494 | 119,571 |

## Evaluation
https://latex.codecogs.com/svg.image?Tput_%7BUnit%7D=%5Cfrac%7Br%7D%7BLatency_%7BRound%7D%7D*f%20%5C%5C%5C%5CTput_%7BSystem%7D=Tput_%7BUnit%7D*U_%7BXB%7D*N_%7BXB%7D%20%5C%5C%5C%5CPower_%7BSystem%7D=%5Cfrac%7BTput_%7BSystem%7D*Energy_%7BUnit%7D%7D%7Br%7D%20

## User Information
### Dependencies
In order to use the project, you will need:
1. python3
2. pytorch

### User Manual
Running `python TestHashPIM_SHA3-224.py` will run HashPIM for SHA3-224 on the simulator for a random 378 sample of bit arrays with a random size each (limited to size r-4). The simulator verifies the correctness
of the simulator output and counts the exact number of cycles and gates used. As HashPIM is deterministic, this cycle count is identical for all samples.

Running `python TestHashPIM_SHA3-256.py` will run HashPIM for SHA3-256 on the simulator for a random 378 sample of bit arrays with a random size each (limited to size r-4). The simulator verifies the correctness
of the simulator output and counts the exact number of cycles and gates used. As HashPIM is deterministic, this cycle count is identical for all samples.

Running `python TestHashPIM_SHA3-384.py` will run HashPIM for SHA3-384 on the simulator for a random 378 sample of bit arrays with a random size each (limited to size r-4). The simulator verifies the correctness
of the simulator output and counts the exact number of cycles and gates used. As HashPIM is deterministic, this cycle count is identical for all samples.

Running `python TestHashPIM_SHA3-512.py` will run HashPIM for SHA3-512 on the simulator for a random 378 sample of bit arrays with a random size each (limited to size r-4). The simulator verifies the correctness
of the simulator output and counts the exact number of cycles and gates used. As HashPIM is deterministic, this cycle count is identical for all samples.

## Implementation Details
The implementation is divided into the following files: 
1. `simulator.py`. Provides the interface for a memristive crossbar array.
2. `HashPIM.py`. Simulates the HashPIM algorithm for Secure Hash Algorithm-3 (SHA-3).
3. `TestHashPIM.py`. Tests the HashPIM algorithm for varying (r, digest)={(1152,224),(1088,256),(832,384),(576,512)}.
4. `Utilities.py`. Simplify the use of the logic functions within the memristive crossbar array.
