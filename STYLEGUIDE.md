# Styleguide

<sup><sup>Do **not** approve pull-requests when any of these are not fulfilled</sup></sup>

## Python
### Version
- Python 3.12.7

### Format
- always use tabs
- `black` formatter on default settings (https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter on vscode)

### Naming
- PascalCase for classes
- snake_case for functions
- snake_case for member variables
- `__` prefix for private member variables
- member variables public when getter and setter exist and trivial
- **never** abbreviate identifiers (except proper names)

### Other
- **always** add TypeHints
- **every** function and **every** class needs a docstring

