# HashPIM: Accelerating SHA-3 Algorithm with Memristive Stateful Logic
## Overview
This is a logic simulator to verify the theoretical results (latency, energy, and area) of HashPIM, a hardware design for the implementation of SHA3-224, SHA3-256, SHA3-384, SHA3-512. This logic simulator models a memristive crossbar array with partitions, and then simulates running the HashPIM algorithm. The correctness of the operations is verified externally, and the number of cycles is measured, including initialization cycles.

`B. Oved, O. Leitersdorf, R. Ronen, and S. Kvatinsky, “HashPIM: High-Throughput SHA-3 via Memristive Digital Processing-in-Memory,” 2022.`

## Results

The results for a single crossbar (*XB*) for one SHA3 round (out of 24):

<table>
  <tr>
    <th>Entity</th>
    <th>Latency (Cycles)</th>
    <th>#Switchings</th>
    <th>Area (Memristors)</th>
    <th>Units</th>
    <th>Gates</th>
  </tr>
  <tr>
    <td align="left">1 Unit</td>
    <td rowspan="2" align="center">3,494</td>
    <td align="center">119,571</td>
    <td align="center">72x37</td>
    <td align="center">1</td>
    <td rowspan="2" align="center">MAGIC<sup>[1]</sup> NOT/NOR, FELIX<sup>[2]</sup> OR/XOR</td>
  </tr>
  <tr>
    <td align="left">1 XB</td>
    <td align="center">45,197,838</td>
    <td align="center">1024x1024</td>
    <td align="center">378</td>
  </tr>
</table>

Note: memristors's area is equivalent to 4*F*<sup>2</sup>.


The results for each SHA3 step for a single round: 

| Step | Latency (Cycles) | #Switchings |
| :---- | :----: | :----: |
| Theta | 330 | 15,127 |
| Rho | 2,911 | 82,300 |
| Pi | 81 | 6,976 |
| Chi | 140 | 14,720 |
| Iota | 32 | 448 |
| **Total** | **3,494** | **119,571** |

## Evaluation
<img src="https://latex.codecogs.com/svg.image?\bg{black}\color{DarkBlue}&space;{Tput_{Unit}=\frac{r}{Latency_{Round}}*f}&space;\\\\\color{DarkBlue}&space;{Tput_{System}=Tput_{Unit}*U_{XB}*N_{XB}}&space;\\\\\color{DarkBlue}&space;{Power_{System}=\frac{Tput_{System}*Energy_{Unit}}{r}}" title="https://latex.codecogs.com/svg.image?\bg{black}\color{DarkBlue} {Tput_{Unit}=\frac{r}{Latency_{Round}}*f} \\\\\color{DarkBlue} {Tput_{System}=Tput_{Unit}*U_{XB}*N_{XB}} \\\\\color{DarkBlue} {Power_{System}=\frac{Tput_{System}*Energy_{Unit}}{r}}" />


Assuming e.g., *r*=1088 (SHA3-256), and MAGIC<sup>[1]</sup> gate parameters of 3*ns* delay (333*MHz*) and 6.4*fJ* energy<sup>[3]</sup>.


### Performance Comparison of SHA-3 Hardware Designs:

<table>
  <tr>
    <th>Work</th>
    <th><i>f</i> (MHz)</th>
    <th>Tput (Gbps)</th>
    <th>Tput/W (Gbps/W)</th>
    <th>Tput/Area (bps/<i>F</i><sup>2</sup>)</th>
  </tr>
  <tr>
    <td align="left">65nm ASIC<sup>[4]</sup></td>
    <td align="center">1K</td>
    <td align="center">48</td>
    <td align="center">-</td>
    <td align="center">7,619</td>
  </tr>
  <tr>
    <td align="left">SHINE-1<sup>[5]</sup></td>
    <td align="center">2K</td>
    <td align="center">33.4</td>
    <td align="center">263</td>
    <td align="center">21,916</td>
  </tr>
  <tr>
    <td align="left">SHINE-2<sup>[5]</sup></td>
    <td align="center">2K</td>
    <td align="center">54</td>
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

Note that HashPIM design was evaluated within a single *XB*, containing 378 *Unit*s, to compare a single SHA3-256 round performance.


## User Information
### Dependencies
In order to use the project, you will need:
1. python3
2. pytorch
3. cryptodome

### User Manual
Running `python TestHashPIM_SHA3-224.py` will run HashPIM for SHA3-224 on the simulator for a random 378 sample of bit arrays with a random size each (limited to size r-4). The simulator verifies the correctness
of the simulator output and counts the exact number of cycles and memristors' switchings made. As HashPIM is deterministic, this cycle count is identical for all samples.

Running `python TestHashPIM_SHA3-256.py` will run HashPIM for SHA3-256 on the simulator for a random 378 sample of bit arrays with a random size each (limited to size r-4). The simulator verifies the correctness
of the simulator output and counts the exact number of cycles and memristors' switchings made. As HashPIM is deterministic, this cycle count is identical for all samples.

Running `python TestHashPIM_SHA3-384.py` will run HashPIM for SHA3-384 on the simulator for a random 378 sample of bit arrays with a random size each (limited to size r-4). The simulator verifies the correctness
of the simulator output and counts the exact number of cycles and memristors' switchings made. As HashPIM is deterministic, this cycle count is identical for all samples.

Running `python TestHashPIM_SHA3-512.py` will run HashPIM for SHA3-512 on the simulator for a random 378 sample of bit arrays with a random size each (limited to size r-4). The simulator verifies the correctness
of the simulator output and counts the exact number of cycles and memristors' switchings made. As HashPIM is deterministic, this cycle count is identical for all samples.

## Implementation Details
The implementation is divided into the following files: 
1. `simulator.py`. Provides the interface for a memristive crossbar array.
2. `HashPIM.py`. Simulates the HashPIM algorithm for Secure Hash Algorithm-3 (SHA-3).
3. `TestHashPIM.py`. Tests the HashPIM algorithm for varying (r, digest)={(1152,224),(1088,256),(832,384),(576,512)}.
4. `Utilities.py`. Simplify the use of the logic functions within the memristive crossbar array.

### References

[1] S. Kvatinsky et al., “MAGIC—memristor-aided logic,” TCAS-II, September 2014.

[2] S. Gupta et al., “FELIX: Fast and energy-efficient logic in memory,” ICCAD 2018.

[3] M. S. Q. Truong et al., “RACER: Bit-pipelined processing using resistive memory,” MICRO 2021.

[4] M. M. Wong et al., “A new high throughput and area efficient SHA-3 implementation,” ISCAS 2018.

[5] K. Nagarajan et al., “SHINE: A novel SHA-3 implementation using reram-based in-memory computing,” ISLPED 2019.
