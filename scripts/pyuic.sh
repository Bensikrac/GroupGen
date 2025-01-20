#!/bin/bash
python -m venv venv
./venv/bin/python -m pip install ".[dev,gui,release]"
./venv/bin/python -m PyQt6.uic.pyuic -o src/assets assets/