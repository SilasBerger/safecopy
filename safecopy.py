import sys
import pathutil
import logging
import getopt
from pathlib import Path
from handler import HandlerFactory

class Safecopy:

    def __init__(self, in_root, out_root, spec_file):
        logging.logger.log("Setting up...", tag="MAIN")
        
        # Get args and convert to paths
        spec_file = Path(spec_file).absolute()
        self.input_root = Path(in_root).absolute()
        self.output_root = Path(out_root).absolute()

        if not self.input_root.is_dir():
            logging.logger.log("ERROR: No such input root directory: " + str(self.input_root.absolute()))
            exit(1)

        if self.output_root.exists():
            logging.logger.log("ERROR: Output root '" + str(self.output_root.absolute()) + "' already exists, refusing to overwrite")
            exit(1)

        # Initialize handler factory.
        self.handler_factory = HandlerFactory(self.input_root, self.output_root)

        # Parse copy specs
        self.copy_specs = {}
        with open(str(spec_file), "r") as infile:
            copy_specs_strings = infile.read()
            for idx, spec_str in enumerate(copy_specs_strings.split("\n")):
                if not spec_str:
                    # Skip blank line
                    continue
                spec = self.parse_spec(spec_str, idx + 1)
                if spec is not None:
                    self.copy_specs[spec["ext"]] = spec

    def parse_spec(self, spec, line_number):
        spec_parts = spec.split(":")
        if len(spec_parts) <= 1:
            logging.logger.log("ERROR: Invalid spec '" + spec + "' on line " + str(line_number) + ", aborting", tag="MAIN")
            exit(1)
        ext = spec_parts[0]
        task = spec_parts[1]
        task_parts = task.split("#")
        handler_name = task_parts[0]
        if not self.handler_factory.has_handler(handler_name):
            logging.logger.log("Invalid handler: " + handler_name + " (spec = '" + spec + "'), aborting", tag="MAIN")
            exit(1)
        handler_args = task_parts[1] if len(task_parts) > 1 else ""
        return {
            "ext": ext,
            "handler": handler_name,
            "handler_args": handler_args
        }

    def add_default_spec(self, ext):
        default_handler = "s"
        logging.logger.log("WARNING: No handler specified for extension '" + ext + "', assuming '" + default_handler + "' by default", tag="MAIN")
        self.copy_specs[ext] = {
            "ext": ext,
            "handler": default_handler,
            "handler_args": ""
        }

    def run(self):
        logging.logger.log("Starting copy process", tag="MAIN")
        file_paths = [f.absolute() for f in self.input_root.rglob("*.*") if f.is_file()]
        for fp in file_paths:
            ext = fp.name.split(".")[-1]
            if ext not in self.copy_specs:
                # No spec defined for this file extension - create default spec and add it to dictionary.
                self.add_default_spec(ext)
            spec = self.copy_specs[ext]
            handler = self.handler_factory.create(spec["handler"])
            handler.handle(fp, spec["handler_args"])
        logging.logger.log("Copy process completed successfully", tag="MAIN")


def print_usage():
    print("Usage:")
    print("\n\tpython safecopy.py --in <input_root> --out <output_root> --spec <specs_file>")
    print("\tpython safecopy.py --help (display this help text)")
    print("\nRefer to README.md for additional information.")


if __name__ == "__main__":
    logging.logger = logging.Logger(log_to_file=True)

    try:
        optlist, args = getopt.getopt(sys.argv[1:], "", ["in=", "out=", "spec=", "help"])
    except getopt.GetoptError as err:
        logging.logger.log("ERROR:" + err, tag="MAIN")
        print_usage()
        exit(2)

    optdict = {}
    for opt in optlist:
        optdict[opt[0]] = opt[1]

    if "--help" in optdict:
        print_usage()
        exit(0)

    required_opts = ["--in", "--out", "--spec"]
    for ro in required_opts:
        if ro not in optdict.keys():
            logging.logger.log("ERROR: Missing required option: " + ro, tag="MAIN")
            print_usage()
            exit(2)

    Safecopy(optdict["--in"], optdict["--out"], optdict["--spec"]).run()
