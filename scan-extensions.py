import sys

from pathlib import Path

if len(sys.argv) != 2:
  print("Invalid number of arguments: " + str(len(sys.argv)))
  print("Usage: python3 scan-extension.py <root_dir>")
  exit(1)

root_path = Path(sys.argv[1])
if not root_path.is_dir():
  print("Specified root is not a directory: " + str(root_path))
  exit(1)

for ext in set([f.name.split(".")[-1] for f in root_path.rglob("*.*") if f.is_file()]):
  print(ext)