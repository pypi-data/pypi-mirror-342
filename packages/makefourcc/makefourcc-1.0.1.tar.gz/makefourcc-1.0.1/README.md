# makefourcc

A minimal Python module that replicates the `MAKEFOURCC` macro from Windows APIs. This is useful for creating FOURCC codes in graphics, multimedia, or game development contexts.

## Installation

```bash
pip install makefourcc
```

## Usage

```python
from makefourcc import MAKEFOURCC

code = MAKEFOURCC('D', 'X', 'T', '1')
print(hex(code))  # Outputs: 0x31545844
```
