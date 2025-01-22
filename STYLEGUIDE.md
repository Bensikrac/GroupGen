# Styleguide

<sup><sup>Do **not** approve pull-requests when any of these are not fulfilled</sup></sup>

## Python
### Version
- Python 3.12.7

### Format
- always use tabs
- `black` formatter on default settings ([vscode-extension](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter))
- **every** code file should end with a newline

### Naming
- PascalCase for classes
- snake_case for functions
- snake_case for member variables
- `__` prefix for private member variables/functions
- member variables public when getter and setter exist and trivial
- **never** abbreviate identifiers (except proper names)

### Style
- **always** add TypeHints (exception: `self` parameters must omit `Self` typehints)
- no more than 4 indentation levels inside any function (code complexity and readability; first instruction inside a function is considered to be on indent level 0)
- remember that Python is not purely object-oriented

### Docstrings
- **every** function and **every** class needs a [docstring](https://peps.python.org/pep-0257/) except dunder-methods (`__*__`) which should only have a docstring if the implementation may behave unexpected. a special mention is `__init__` the parameters of which should be documented in the class' docstring and unexpected behaviour (e.g. global side-effects) inside the class' extended description
- **must** be in [`sphinx` compatible format](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html)
- `self` parameters without typehint **must not** be documented
- Summaries and extended descriptions **always** end with a dot (`.`). normal descriptions (like parameter descriptions) **must not** end with a dot
- the order for documenting a function (with a double newline between each non-empty bullet-point group; an empty line in-between)
  - Summary (always imperative)
  - Optional extended description
  - parameter description in order of appearance
  - `yield` then `return` value description
  - possible errors raised in order of appearance
- the order for documenting a class (with a double newline after each bullet-point group)
  - Summary (Description of what it represents, or in case of interfaces/abstract classes what it provides an interface for)
  - TODO: documentation of type-parameters

#### Example (Functions)
```py
"""[Summary]

[Extended Description (optional)]

:param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
...

:yield: [YieldDescription]
:return: [ReturnDescription]

:raises [ErrorType]: [ErrorDescription]
...

:Examples:
>>> line 1 of example
>>> line 2 of example

>>> line 1 of second example
...

.. seealso:: text
.. note:: text
.. warning:: text
.. todo:: text
"""
```

#### Example (Classes)
```py
"""[Summary]

[Extended Description (optional)]

TODO: type-parameters (is this even possible with sphinx? is a `TypeVar` needed?)

:param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
...

:Examples:
>>> line 1 of example
>>> line 2 of example

>>> line 1 of second example
...

.. seealso:: text
.. note:: text
.. warning:: text
.. todo:: text
"""
```


## Project structure
- source files into `src`
- no subfolders for single-file components
- snake_case for filenames

