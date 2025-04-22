# ERAL Algorithm

## Introduction
The ERAL (Error In Alignment) algorithm is a state-of-the-art method designed for time series alignment and averaging.
The method obtains the average time series (the prototype) from a set of time series (a class).

## Installation

To use ERAL, please install the package from pypi.org using pip:
```bash
pip install eral
```

## Usage

The main entry point for the end user is `obtain_prototype` method in `eral.eral`:

```py
from eral.eral import obtain_prototype

class_prototype = obtain_prototype(...)
```

The function takes several arguments, most important are:
- `class_segments`: a list of time series to be aligned and averaged
- `prototyping_function`: determines how the average is computed, typically the function `get_new_prototype_variable_clipping` from `eral.alignment_prototyping_functions` can be used.
- `exclustion_zone`: percentage of forbidden alignments (see [1])

The basic function call is:

```py
import numpy as np
from eral.eral import obtain_prototype
from eral.alignment_prototyping_functions import get_new_prototype_variable_clipping

X: list[np.ndarray] = [...]  # Class data

class_prototype = obtain_prototype(X,
                                   prototyping_function=get_new_prototype_variable_clipping,
                                   exclusion_zone=0.2)
```

For full examples, please refer to the `examples/` directory at [our repository](https://repo.ijs.si/zstrzinar/eral).

## Demonstration
The following figure demonstrates ERAL algorithm on a set of time series from the Trace dataset from UCR Archive. The dataset contains 100 time series, each with 275 samples. The time series are aligned and averaged using ERAL, and the resulting prototype is shown in the figure.
![ERAL demonstration](https://repo.ijs.si/zstrzinar/eral/-/raw/9a75930a589c796514094ed5a9ca1eb821907853/docs/assets/trace-comparison.png)


## Examples

The `examples/` directory at [our repository](https://repo.ijs.si/zstrzinar/eral) contains Jupyter notebooks that illustrate different uses and capabilities of the ERAL algorithm. 
To run an example, navigate to the `examples/` directory and execute the desired notebook.

- Notebook titled `01 ERAL demo` demonstrates the ERAL prototyping method using the Trace dataset from UCR Archive.
- Notebook titled `02 ERAL demo on industrial data` downloads an industrial dataset from Mendeley Data, and calculates the prototypes for all classes.
- Notebook titled `03 Comparison` compares ERAL to DBA, SSG and others, using implementations in `tslearn`


## References
[1] STRŽINAR, Žiga; PREGELJ, Boštjan; ŠKRJANC, Igor. Non-elastic time series fuzzy clustering for efficient analysis of industrial data sets. Applied Soft Computing, 2024, 112398, doi: [10.1016/j.asoc.2024.112398](https://doi.org/10.1016/j.asoc.2024.112398).\
[2] Stržinar, Žiga; Pregelj, Boštjan; Petrovčič, Janko; Škrjanc, Igor; Dolanc, Gregor (2024), “Pneumatic Pressure and Electrical Current Time Series in Manufacturing”, Mendeley Data, V2, doi: 10.17632/ypzswhhzh9.2, url: https://data.mendeley.com/datasets/ypzswhhzh9/2
