import pathutil
import logging
import subprocess
from pathlib import Path

class HandlerFactory:

    def __init__(self, input_root, output_root):
        self._handler_names = ["mag", "c", "s"]
        self._handler_meta = _HandlerMeta(input_root, output_root)

    def has_handler(self, handler_name):
        return handler_name in self._handler_names

    def create(self, handler_name):
        if handler_name not in self._handler_names:
            # Invalid handler name, bail
            logging.logger.log("ERROR: Invalid handler '" + handler_name + "', aborting", tag="HFAC")
            exit(1)

        # Dispatch handler
        if handler_name == "s":
            return SkipHandler(self._handler_meta)
        if handler_name == "c":
            return CopyHandler(self._handler_meta)
        if handler_name == "mag":
            return ImageMagickHandler(self._handler_meta)


class _HandlerMeta:

    def __init__(self, input_root, output_root):
        self.input_root = input_root
        self.output_root = output_root


class Handler:

    def __init__(self, handler_tag, handler_meta):
        self._handler_meta = handler_meta
        self.handler_tag = handler_tag

    def handle(self, input_file_path, args):
        raise NotImplementedError()


class SkipHandler(Handler):

    def __init__(self, handler_meta):
        super().__init__("SKIP", handler_meta)

    def handle(self, input_file_path, args):
        logging.logger.log_handler(self, str(input_file_path))


class CopyHandler(Handler):

    def __init__(self, handler_meta):
        super().__init__("COPY", handler_meta)

    def handle(self, input_file_path, args):
        if not input_file_path.is_file():
            # Should not reach here - log and exit.
            logging.logger.log_handler(self, "ERROR: '" + str(input_file_path) + "' is does not exist or is not a file.")
            exit(1)
        dst_file_path = pathutil.calculate_path_substitution(self._handler_meta.input_root, self._handler_meta.output_root, input_file_path)
        pathutil.ensure_output_path(dst_file_path)

        # Copy file (-r and -f flags not specified to avoid unexpected behavior)
        result = subprocess.run(["cp", str(input_file_path), str(dst_file_path)], capture_output=True)
        if result.returncode != 0:
            # Shell command returned non-zero, bail
            logging.logger.log_handler(self, "cp command returned with exit code " + str(result.returncode) + ": " + result.stderr.decode("utf-8"))
            exit(1)
        logging.logger.log_handler(self, str(input_file_path) + " -> " + str(dst_file_path))
        

class ImageMagickHandler(Handler):

    def __init__(self, handler_meta):
        super().__init__("IMAG", handler_meta)

    def handle(self, input_file_path, args):
        if not input_file_path.is_file():
            # Should not reach here - log and exit.
            logging.logger.log_handler(self, "ERROR: '" + str(input_file_path) + "' is does not exist or is not a file.")
            exit(1)

        if args == "":
            logging.logger.log_handler(self, "ERROR: missing dst file extension for 'mag' job")
            exit(1)

        dst_file_path = pathutil.calculate_path_substitution(self._handler_meta.input_root, self._handler_meta.output_root, input_file_path)
        dst_file_path = Path(".".join(str(dst_file_path).split(".")[:-1]) + "." + args)
        pathutil.ensure_output_path(dst_file_path)

        # Copy file (-r and -f flags not specified to avoid unexpected behavior)
        result = subprocess.run(["magick", str(input_file_path), str(dst_file_path)], capture_output=True)
        if result.returncode != 0:
            # Shell command returned non-zero, bail
            logging.logger.log_handler(self, "cp command returned with exit code " + str(result.returncode) + ": " + result.stderr.decode("utf-8"))
            exit(1)
        logging.logger.log_handler(self, str(input_file_path) + " -> " + str(dst_file_path))