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
            logging.logger.log("ERROR: No such input root directory: " + str(self.input_root.name))
            exit(1)

        if self.output_root.exists():
            logging.logger.log("ERROR: Output root '" + str(self.output_root.name) + "' already exists, refusing to overwrite")
            exit(1)

        # Initialize handler factory.
        self.handler_factory = HandlerFactory(self.input_root, self.output_root)

        # Parse copy specs
        self.copy_specs = {}
        with open(str(spec_file), "r") as infile:
            copy_specs_strings = infile.read()
            for spec_str in copy_specs_strings.split("\n"):
                spec = self.parse_spec(spec_str)
                if spec is not None:
                    self.copy_specs[spec["ext"]] = spec

    def parse_spec(self, spec):
        spec_parts = spec.split(":")
        if len(spec_parts) <= 1:
            return None
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

    def run(self):
        logging.logger.log("Starting copy process", tag="MAIN")
        file_paths = [f.absolute() for f in self.input_root.rglob("*.*") if f.is_file()]
        for fp in file_paths:
            ext = fp.name.split(".")[-1]
            spec = None
            if ext not in self.copy_specs:
                logging.logger.log("No handler specified for extension '" + ext + "', skipping by default", tag="MAIN")
                spec = self.copy_specs["s"]
            else:
                spec = self.copy_specs[ext]
            handler = self.handler_factory.create(spec["handler"])
            handler.handle(fp, spec["handler_args"])
        logging.logger.log("Copy process completed successfully", tag="MAIN")

    
if __name__ == "__main__":
    logging.logger = logging.Logger(log_to_file=True)

    try:
        optlist, args = getopt.getopt(sys.argv[1:], "", ["in=", "out=", "spec=", "help"])
    except getopt.GetoptError as err:
        logging.logger.log("ERROR:" + err, tag="MAIN")

    optdict = {}
    for opt in optlist:
        optdict[opt[0]] = opt[1]
    required_opts = ["--in", "--out", "--spec"]
    for ro in required_opts:
        if ro not in optdict.keys():
            logging.logger.log("ERROR: Missing required option: " + ro, tag="MAIN")
            exit(2)

    Safecopy(optdict["--in"], optdict["--out"], optdict["--spec"]).run()
