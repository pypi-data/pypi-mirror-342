"""Line reader."""

from collections import defaultdict
from wordly.status_codes import Status


class DictParser:
    def __init__(self, delimiter: bytes = b"\r\n"):
        self.line = bytearray()
        self.mapping = defaultdict(bytearray)
        self.DELIMITER = delimiter

    def _process_line(self, ending: bytes = b""):
        code = self.line[:3]
        status = Status.by_value(bytes(code))

        if status:
            data = self.line[4:]
            self.part = status.name
        else:
            data = self.line

        buf = self.mapping[self.part]
        buf.extend(data)
        buf.extend(ending)

    def feed(self, stream: bytes):
        split = stream.split(self.DELIMITER, 1)
        while len(split) > 1:
            old, new = split
            self.line += old
            self._process_line(b"\n")
            self.line = b""
            split = new.split(self.DELIMITER, 1)

        if line := split[0]:
            self.line += line
            self._process_line()
            self.line = b""
