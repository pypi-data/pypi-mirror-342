HLrainflow
# HLrainflow

A simple and efficient implementation of the Rainflow counting algorithm for fatigue analysis in Python.

## Features

- Rainflow cycle counting for fatigue analysis
- Lightweight and dependency-free
- Supports peak-valley sequences or raw time-series input
- Easy to test and extend

## Installation

You can install the package via pip:

```bash
pip install HLrainflow
```

## Usage
ASTM E1049-85(2017) Rainflow Counting Example   
Refer to [Astm e 1049 85 standard practice for cycle counting in fatigue analysis](https://www.slideshare.net/slideshow/astm-e-1049-85-standard-practice-for-cycle-counting-in-fatigue-analysis/42141102)
```python
from HLrainflow import rainflow
Sample1=[-2,1,-3,5,-1,3,-4,4,-2]
peak=Sample1
hl=rainflow.HL()
hl.SetPeak(peak)
halfR,halfM=hl.hloop()
print('half range=',halfR)
print('half mean=',halfM)  
```

## Example Output
half range= [4.0, 4.0, 3.0, 4.0, 8.0, 9.0, 8.0, 6.0]   
half mean= [1.0, 1.0, -0.5, -1.0, 1.0, 0.5, 0.0, 1.0]

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
