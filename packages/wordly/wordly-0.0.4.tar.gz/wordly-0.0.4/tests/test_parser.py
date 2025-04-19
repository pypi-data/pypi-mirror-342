import unittest
from wordly.parser import DictParser
from wordly.status_codes import Status
from tests.constants import HELP_OUTPUT, PROGRAMMING_DEFINITION


class TestParser(unittest.TestCase):
    def setUp(self) -> None:
        self.line_reader = DictParser()

    def test_help(self):
        self.line_reader.feed(HELP_OUTPUT)

        self.assertEqual(
            self.line_reader.mapping[Status.INITIAL_CONNECTION.name],
            bytearray(b"banner info from example.org\n"),
        )
        self.assertEqual(self.line_reader.mapping[Status.COMMAND_COMPLETE.name], bytearray(b"ok\n"))
        self.assertEqual(
            self.line_reader.mapping[Status.CLOSING_CONNECTION.name],
            bytearray(b"bye [d/m/c = 0/0/0; 0.000r 0.000u 0.000s]"),
        )

    def test_define(self):
        self.line_reader.feed(PROGRAMMING_DEFINITION)

        self.assertEqual(
            self.line_reader.mapping[Status.INITIAL_CONNECTION.name],
            bytearray(b"banner information contained here\n"),
        )
        self.assertEqual(
            self.line_reader.mapping[Status.CLOSING_CONNECTION.name],
            bytearray(b"bye [d/m/c = 0/0/0; 0.000r 0.000u 0.000s]"),
        )
