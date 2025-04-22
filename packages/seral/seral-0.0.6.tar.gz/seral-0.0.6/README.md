# Streaming ERAL Algorithm and application to Evolving Clustering

## Introduction
The sERAL (Streaming Error In Alignment) algorithm is a state-of-the-art method designed for online time series alignment and averaging.
The method obtains the average time series (the prototype) from a set of time series (a class).

## Installation
### pip package

To use sERAL, please install the package from pypi.org using pip:
```bash
pip install seral
```

### From source
To access sERAL source code, please clone the git repository:
```bash
git clone https://repo.ijs.si/zstrzinar/streaming-eral.git
```

The repository contains a requirements file, ensure you have all the requirements
```
pip install -r requirements.txt
```

## Usage

The main entry point for the end user is `Cluster` class in `seral.seral`:

```py
from src.seral.seral import Cluster as sERAL

searl = sERAL(sample=initial_sample, id=0)
```

The class constructor accepts two parameters:
- `sample` - the initial sample to be used for the prototype calculation
- `id` - the class identifier

The basic function call is:

```py
import numpy as np
from src.seral.seral import Cluster as sERAL

data: list[np.ndarray] = [...]

seral: sERAL = sERAL(sample=data[0], id=id, alpha=0.5)
for sample in data[1:]:
    seral.add_sample(sample=sample)

prototype = seral.prototype
    
```

For full examples, please refer to the `examples/` directory.

## Demonstration
The following figure demonstrates sERAL algorithm on a set of time series from the Trace dataset from UCR Archive. The dataset contains 100 time series, each with 275 samples. The time series are aligned and averaged using sERAL, and the resulting prototype is shown in the figure.
![sERAL demonstration](docs/assets/trace.png)

## Examples
The `examples/` directory contains Jupyter notebooks that illustrate different uses and capabilities of the sERAL algorithm. 
To run an example, navigate to the `examples/` directory and execute the desired notebook.

- Notebook titled `01 sERAL demo` demonstrates the sERAL prototyping method using the Trace dataset from UCR Archive.
- Notebook titled `02 sERAL demo on industrial data` downloads an industrial dataset from Mendeley Data [2], and calculates the prototypes for all classes.
- Notebook titled `03 sERAL vs ERAL vs DBA vs SBD` demonstrates the performance of sERAL, ERAL, DBA, and SBD algorithms on the industrial dataset from [2].
- Notebook titled `04 Evolving Time Series Clustering` demonstrates the application of sERAL in the Evolving Time Series Clustering method [1].

## References
[1] Stržinar, Žiga; Škrjanc, Igor; Pratama, Mahardhika and Pregelj, Boštjan (2024), "Evolving Clustering of Time Series for Unsupervised Analysis of Industrial Data Streams", available at SSRN: https://ssrn.com/abstract=5026151 \
[2] Stržinar, Žiga; Pregelj, Boštjan; Petrovčič, Janko; Škrjanc, Igor; Dolanc, Gregor (2024), “Pneumatic Pressure and Electrical Current Time Series in Manufacturing”, Mendeley Data, V2, doi: 10.17632/ypzswhhzh9.2, url: https://data.mendeley.com/datasets/ypzswhhzh9/2
