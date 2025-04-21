import os, sys
from pathlib import Path

PARENT_DIR = Path(__file__).parents[1].resolve()
DATA_DIR = PARENT_DIR / 'data'
RAW_DATA_DIR =DATA_DIR / 'raw'
TRANSFORMED_DATA_DIR = DATA_DIR / 'transformed'

if not DATA_DIR.is_dir():
    DATA_DIR.mkdir()

if not RAW_DATA_DIR.is_dir():
    RAW_DATA_DIR.mkdir()

if not TRANSFORMED_DATA_DIR.is_dir():
    TRANSFORMED_DATA_DIR.mkdir()



