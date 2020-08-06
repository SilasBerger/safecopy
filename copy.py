import pathutil
import logging
from pathlib import Path
from handler import HandlerFactory

class Safecopy:

    def __init__(self):
        logging.logger.log("Setting up...", tag="MAIN")
        # TODO: Read from command line args.
        extensions_filename = "extensions.txt"
        self.input_root = Path("fixtures").absolute()
        self.output_root = Path("out").absolute()

        logging.logger = logging.Logger(log_to_file=True)

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
        with open(extensions_filename, "r") as infile:
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
    Safecopy().run()
