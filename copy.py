import pathutil
import logging
from logging import logger, Logger
from pathlib import Path
from handler import Handler, SkipHandler

valid_handlers = ["mag", "s", "c"]

def parse_spec(spec):
    spec_parts = spec.split(":")
    if len(spec_parts) <= 1:
        return None
    ext = spec_parts[0]
    task = spec_parts[1]
    task_parts = task.split("#")
    handler = task_parts[0]
    if handler not in valid_handlers:
        print("Invalid handler: " + handler + " ('" + spec + "'), aborting")
        exit(1)
    handler_args = task_parts[1] if len(task_parts) > 1 else ""
    return {
        "ext": ext,
        "handler": handler,
        "handler_args": handler_args
    }
    
def main():
    # TODO: Read from command line args.
    extensions_filename = "extensions.txt"
    input_root = Path("fixures").absolute()
    output_root = Path("out").absolute()

    logging.logger = Logger(log_to_file=False)

    if not input_root.is_dir():
        logger.log("ERROR: No such input root directory: " + str(input_root.name))
        exit(1)

    if output_root.exists():
        logger.log("ERROR: Output root '" + str(output_root.name) + "' already exists, refusing to overwrite")
        exit(1)

    copy_specs = []
    with open(extensions_filename, "r") as infile:
        copy_specs_strings = infile.read()
        for spec_str in copy_specs_strings.split("\n"):
            spec = parse_spec(spec_str)
            if spec is not None:
                copy_specs.append(spec)

    file_paths = [f.absolute() for f in input_root.rglob("*.*") if f.is_file()]

if __name__ == "__main__":
    main()