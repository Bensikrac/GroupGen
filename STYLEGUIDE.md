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

### Other
- **always** add TypeHints
- **every** function and **every** class needs a docstring (PEP 257 - https://peps.python.org/pep-0257/)


## Project structure
- source files into `src`
- no subfolders for single-file components
- snake_case for filenames

