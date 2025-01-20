#!/bin/bash
python -m venv venv
./venv/bin/python -m pip install ".[dev,gui,release]"
./venv/bin/python -m PyQt6.uic.pyuic -o src/assets assets/
./venv/bin/python -m PyInstaller --noconsole --onefile src/app.py
echo "exe is in /dist"