python -m venv venv
.\venv\Scripts\python.exe -m pip install -e ".[dev,gui,release]"
.\venv\Scripts\python.exe -m PyQt6.uic.pyuic -o src/assets assets/