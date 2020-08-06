import pathutil

class HandlerFactory:

    def __init__(self, input_root, output_root, logger):
        self._handler_names = ["mag", "c", "s"]
        self._handler_meta = _HandlerMeta(input_root, output_root, logger)

    def has_handler(self, handler_name):
        return handler_name in self._handler_names


class _HandlerMeta:

    def __init__(self, input_root, output_root, logger):
        self.input_root = input_root
        self.output_root = output_root
        self.logger = logger


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
        self._handler_meta.logger.log_handler(self, str(input_file_path))


class CopyHandler(Handler):

    def __init__(self, handler_meta):
        super().__init__("COPY", handler_meta)

    def handle(self, input_file_path, args):
        if not input_file_path.is_file():
            # Should not reach here - log and exit.
            self._handler_meta.logger.log_handler(self, "ERROR: '" + str(input_file_path) + "' is does not exist or is not a file.")
            exit(1)
        dst_file_path = pathutil.calculate_path_substitution(self._handler_meta.src_root, self._handler_meta.dst_root, input_file_path)
        pathutil.ensure_output_path(dst_file_path)