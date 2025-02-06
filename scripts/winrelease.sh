#!/bin/bash
python -m venv venv
./venv/bin/python -m pip install -e ".[dev,gui,release]"
./venv/bin/python -m PyQt6.uic.pyuic -o src/assets assets/
./venv/bin/python -m PyInstaller --noconsole --onefile src/app.py --add-data "assets/groupgen_logo3_icon.ico:." -i assets/groupgen_logo3_icon.ico
echo "exe is in /dist"