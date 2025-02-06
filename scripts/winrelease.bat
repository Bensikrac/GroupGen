python -m venv venv
.\venv\Scripts\python.exe -m pip install -e ".[dev,gui,release]"
.\venv\Scripts\python.exe -m PyQt6.uic.pyuic -o src/assets assets/
.\venv\Scripts\python.exe -m PyInstaller --noconsole --onefile src/app.py --add-data "assets/groupgen_logo3_icon.ico:." -i assets/groupgen_logo3_icon.ico
rem "Exe is in dist/"
pause