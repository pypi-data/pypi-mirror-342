# mensura

#### By *Albert Dow*

#### *A simple Python package for converting between units*

## Description

A lightweight and simple package for converting between units,
`mensura` uses a graph-based approach to determine the shortest
path to the desired unit.

Currently only supports basic length and time units.

## Usage

```python
from mensura import Converter
converter = Converter()
converter.convert(1.0, "km", "m")
```
