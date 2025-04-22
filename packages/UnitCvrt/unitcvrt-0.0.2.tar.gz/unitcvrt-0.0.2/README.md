# UnitCvrt
Unit Conversion System

## Author
Shinsuke Sakai
Yokohama National University

## Installation
You can install the package via pip:

```bash
pip install UnitCvrt
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Usage
First, create an instance and check the registered unit names.
```python
from UnitCvrt import UnitConv as uc
conv=uc.Conv()
conv.Registered()
```
Select a unit name from the list of registered units, then convert it using the following steps.
The example below demonstrates how to convert 1 meter to inch for the case of length.
```python
conv.SetUnit('Length')
conv.Eval('m','in',1)
```
You can output the unit conversion table using the following command. You can check the unit names from this output.
```python
conv.ShowDict()
```
Finally, you need to destroy the created instance using the following command.
```python
conv.DelUnit()
```
