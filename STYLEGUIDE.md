# Styleguide

<sup><sup>Do **not** approve pull-requests when any of these are not fulfilled</sup></sup>

## Python
### Version
- Python 3.12.7

### Format
- always use tabs
- `black` formatter on default settings (https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter on vscode)
- **every** code file should end with a newline

### Naming
- PascalCase for classes
- snake_case for functions
- snake_case for member variables
- `__` prefix for private member variables
- member variables public when getter and setter exist and trivial
- **never** abbreviate identifiers (except proper names)

### Style
- **always** add TypeHints (exception: `self` parameters must omit `Self` typehints)
- no more than 4 indentation levels inside any function (readability; first instruction inside a function is considered to be on indent level 0)

### Docstrings
- **every** function and **every** class needs a docstring (PEP 257 - https://peps.python.org/pep-0257/)
- **must** be in `sphinx` compatible format (https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html)
- `self` parameters without typehint **must not** be documented
- Summaries and extended descriptions **always** end with a dot (`.`). normal descriptions (like parameter descriptions) **must not** end with a dot
- the order for documenting a function (with a double newline after each bullet-point group) (note that `__init__` is to be documented separate to the class itself)
  - Summary (always imperative)
  - Optional extended description
  - parameter description in order of appearance
  - `yield` then `return` value description
  - possible errors raised in order of appearance
  - privacy meta tag
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

:meta (public|private):

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

TODO: type-parameters
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

