

<h1 align="center">uncle-nelson</h1>
<p align="center">A small library to calculate mixes for the game Schedule 1.</p>

<p align="center">
    <a href="https://pypi.org/project/uncle-nelson/"><img alt="PyPi version" src="https://img.shields.io/pypi/v/uncle-nelson?style=flat-square&color=016dad"></a>
    <a href="https://pypi.org/project/uncle-nelson/"><img alt="Python version" src="https://img.shields.io/pypi/pyversions/uncle-nelson?style=flat-square&color=016dad"></a>
    <a href="https://github.com/codeofandrin/uncle-nelson/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/codeofandrin/uncle-nelson?style=flat-square"></a>
</p>


## Installing

**Python 3.9 or higher is required**

To install the latest stable version, use
```cmd
pip install -U uncle-nelson
```

To install the development version (**may be unstable**), use
```cmd
pip install -U git+https://github.com/codeofandrin/uncle-nelson
```


## Example

```python
from uncle_nelson import calculate_mix, DrugType, IngredientType

def main():
    mix = calculate_mix(DrugType.meth, [IngredientType.cuke, IngredientType.banana])
    effects = ", ".join(e.value for e in mix.effects)
    
    print(f"Your custom mix has following effects: {effects}")

if __name__ == "__main__":
    main()
```


## Links
* [Documentation][1] <br>


[1]: https://uncle-nelson.readthedocs.io/latest/
