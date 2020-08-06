from datetime import datetime

class Logger:

    def __init__(self, log_to_file=True, log_filename=None):
        self.log_file = None
        if log_to_file:
            if log_filename is None:
                log_filename = datetime.now().strftime("%Y-%m-%d_%H:%M:%S_%f") + "_safecopy.log"
            self.log_file = open(log_filename, "w")

    def _print(self, line):
        print(line)
        if self.log_file is not None:
            self.log_file.write(line)

    def log(self, msg, tag=None):
        line = "[" + str(datetime.now()) + "] "
        if tag is not None:
            line = line + "[" + tag + "] "
        line = line + msg
        self._print(line)

    def log_handler(self, handler, msg):
        self.log(msg, handler.handler_tag)


logger = Logger(log_to_file=False)