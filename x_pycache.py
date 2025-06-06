import shutil
import os

for root, dirs, _ in os.walk("."):
    for dir_name in dirs:
        if dir_name == "__pycache__":
            shutil.rmtree(os.path.join(root, dir_name))
            print(f"Deleted: {os.path.join(root, dir_name)}")
