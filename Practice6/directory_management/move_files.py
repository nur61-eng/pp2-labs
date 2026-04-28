import shutil
from pathlib import Path

# create folder
Path("folder").mkdir(exist_ok=True)

# create file
file = Path("test.txt")
file.write_text("Hello")

# move file
shutil.move("test.txt", "folder/test.txt")