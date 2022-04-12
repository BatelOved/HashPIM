# HashPIM: Accelerating SHA-3 Algorithm with Memristive Stateful Logic
## Overview
This is a logic simulator to verify the theoretical results (latency, energy, and area) of HashPIM. This logic simulator models a memristive crossbar array with partitions, and then simulates running the HashPIM algorithm. The correctness of the operations is verified externally, and the number of cycles is measured, including initialization cycles.

`B. Oved, O. Leitersdorf, R. Ronen, and S. Kvatinsky, “HashPIM: High-Throughput SHA-3 via Memristive Digital Processing-in-Memory,” 2022.`

## Results
| Algorithm | Latency (Cycles) | Gates | Area (Memristors) | Partitions | Gates |
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
| **Total** | **3,494** | **119,571** |

## Evaluation
<img src="https://latex.codecogs.com/svg.image?\bg{black}{\color{DarkBlue}&space;Tput_{Unit}=\frac{r}{Latency_{Round}}*f}&space;\\\\{\color{DarkBlue}&space;Tput_{System}=Tput_{Unit}*U_{XB}*N_{XB}}&space;\\\\{\color{DarkBlue}&space;Power_{System}=\frac{Tput_{System}*Energy_{Unit}}{r}}" title="https://latex.codecogs.com/svg.image?\bg{black}{\color{DarkBlue} Tput_{Unit}=\frac{r}{Latency_{Round}}*f} \\\\{\color{DarkBlue} Tput_{System}=Tput_{Unit}*U_{XB}*N_{XB}} \\\\{\color{DarkBlue} Power_{System}=\frac{Tput_{System}*Energy_{Unit}}{r}}" />

### Performance Comparison of SHA-3 Hardware Designs:

<table>
  <tr>
    <th>Work</th>
    <th><i>f</i> (MHz)</th>
    <th>Tput (Gbps)</th>
    <th>Tput/W (Gbps/W)</th>
<<<<<<< HEAD
    <th>Tput/Area (bps/<i>F</i><sup>2</sup>)</th>
=======
    <th>Tput/Area (Gbps/F<sup>2</sup>)</th>
>>>>>>> 7d5a2e728ac72241f553fb3da78388c316434009
  </tr>
  <tr>
    <td align="left">65nm ASIC [1]</td>
    <td align="center">1K</td>
    <td align="center">48</td>
    <td align="center">-</td>
    <td align="center">7,619</td>
  </tr>
  <tr>
    <td align="left">SHINE-1 [2]</td>
    <td align="center">2K</td>
    <td align="center">54</td>
    <td align="center">263</td>
    <td align="center">21,916</td>
  </tr>
  <tr>
    <td align="left">SHINE-2 [2]</td>
    <td align="center">2K</td>
    <td align="center">33.4</td>
    <td align="center">311</td>
    <td align="center">22,227</td>
  </tr>
  <tr>
    <td align="left"><b>HashPIM (1 XB)</b></td>
    <td rowspan="2" align="center"><b>333</b></td>
    <td align="center"><b>39.2</b></td>
    <td rowspan="2" align="center"><b>1,422</b></td>
    <td rowspan="2" align="center"><b>9,354</b></td>
  </tr>
  <tr>
    <td align="left"><b>HashPIM (2 XB)</b></td>
    <td align="center"><b>78.4</b></td>
  </tr>
</table>


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

### References

[1] M. M. Wong et al., “A new high throughput and area efficient SHA-3 implementation,” ISCAS, 2018.

[2] K. Nagarajan et al., “SHINE: A novel SHA-3 implementation using reram-based in-memory computing,” ISLPED, 2019.
