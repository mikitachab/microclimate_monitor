#!/bin/bash
cd ..
pyflakes .
pycodestyle --max-line-length=120 .
vulture --min-confidence=100 .
python3 -m pytest test/



