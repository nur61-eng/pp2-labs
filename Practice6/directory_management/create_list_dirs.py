from pathlib import Path

# create nested dirs
Path("a/b/c").mkdir(parents=True, exist_ok=True)

# list files
for item in Path(".").iterdir():
    print(item)