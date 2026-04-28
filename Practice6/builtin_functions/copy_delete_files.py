import shutil
import os

# copy
shutil.copy("data.txt", "backup.txt")

# delete safely
if os.path.exists("data.txt"):
    os.remove("data.txt")
    print("Deleted")
else:
    print("File not found")