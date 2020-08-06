import logging
from pathlib import Path

def calculate_path_substitution(src_root, dst_root, file):
    file_path = str(file)
    src_path = str(src_root)
    dst_path = str(dst_root)
    sub = file_path.replace(src_path, dst_path)
    return Path(sub)

def ensure_output_path(output_file):
    try:
        # Create parent dir (+ recursive parents) for output file
        output_file.parent.mkdir(parents=True)
    except FileExistsError:
        # Dir already exists, no-op
        pass