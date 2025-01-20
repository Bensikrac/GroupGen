python -m venv venv
.\venv\Scripts\python.exe -m pip install ".[dev,gui,release]"
.\venv\Scripts\python.exe -m PyQt6.uic.pyuic -o src/assets assets/
.\venv\Scripts\python.exe -m PyInstaller --noconsole --onefile src/app.py
rem "Exe is in dist/"
pause