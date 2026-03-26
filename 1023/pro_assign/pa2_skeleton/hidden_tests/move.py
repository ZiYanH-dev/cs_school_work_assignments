import os
from pathlib import Path
import shutil

p=Path('hidden_tests')
move_dir=os.getcwd()
for f in p.iterdir():
    abs=f.absolute()
    shutil.copy()

print(move_dir)