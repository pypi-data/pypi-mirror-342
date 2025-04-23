raise ModuleNotFoundError('This moudle is not completed.')
from pathlib import Path
from sys import prefix

folder_path = Path(prefix, "Lib")
all_entries = [entry.name for entry in folder_path.iterdir()]
files = [entry.name for entry in folder_path.iterdir() if entry.is_file()]
dirs = [entry.name for entry in folder_path.iterdir() if entry.is_dir()]

filter_list = ["site-packages", "this.py", "antigravity.py"]

filtered_list = [item for item in files + dirs if item not in filter_list]
filtered_list = [item for item in files + dirs]

for i in filtered_list:
    try:
        __import__(i.split(".py")[0])
    except (ImportError,ModuleNotFoundError):
        pass
