# Wyckoff

A Python package for working with Wyckoff positions in crystallography.

## Installation

```bash
pip install wyckoff
```
OR
```bash
uv add wyckoff
```

## Usage

Simple Example:

```python
from wyckoff import WyckoffDatabase

wyckoff = WyckoffDatabase()
data = wyckoff.data

for items in data["2"]:
    print(items)

print("Spacegroup 3 (which is 3-b varient):")
print(data["3"][0])
```
for more complex example checkout the [example](https://github.com/anoopkcn/wyckoff/blob/main/examples/example_usage.py) file

# Info

If spacegroup variations are available, and functions are called without specifying the variabtion then first variation will be returned.

**Following variation types are included in the database:**

1. **Unique axis settings**: Suffixes like "-b" and "-c" typically indicate which crystallographic axis is chosen as the unique axis, especially in monoclinic and orthorhombic systems. For example:
   - "3-b" means space group 3 with b-axis as the unique axis
   - "3-c" means space group 3 with c-axis as the unique axis

Example:
```python
wyckoff_positions = WyckoffDatabase().wyckoff_positions
positions = wyckoff_positions("3-b")  # Space group 3 with b-axis as the unique axis
print(positions)
```

2. **Origin choice**: Suffixes like "-1" and "-2" usually indicate different origin choices for the same space group:
   - "48-1" is space group 48 with origin choice 1
   - "48-2" is space group 48 with origin choice 2

Example:
```python
positions = wyckoff_positions("48-1")  # Space group 48 with origin choice 1
print(positions)
```
3. **Cell choices**: Some suffixes may represent different conventional cell choices (hexagonal vs. rhombohedral settings in trigonal groups, for example).

Example:
```python
positions = wyckoff_positions("148-hexagonal")  # Space group 148 with hexagonal cell
print(positions)
```

## Data Source

This implementation is inspierd by a utility fuction in [doped](https://github.com/SMTG-Bham/doped/tree/main) project. That version used a non-standard datafile for parsing the Wyckoff positions from [bilbao crystallographic server](https://www.cryst.ehu.es/). This implementation uses a standard JSON file for parsing the Wyckoff positions, add additional checks and validations to ensure data integrity, remove a bug that produces duplicate Wyckoff positions
and custom wyckoff dataclass, etc,.

## License

MIT
