import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../"))
from line_parser.line_parser import LineParserFactory, LineParser, GenericLineParser
import line_parser.line_parser_factory as factory
from line_parser.line_parser_argument import (
    LineParserArgument,
    LineParserArgumentBuilder,
)


def test_position_based_parser():
    parser: LineParser = LineParserFactory.get_parser("position", "test", 1)
    line = "some test value"
    assert parser.matched(line) == True
    assert parser.parse(line) == {"test": "test"}


def test_position_based_parser_multiple_positions():
    parser = LineParserFactory.get_parser("position", "key", {"first": 0, "second": 2})
    line = "value1 key value2"
    assert parser.matched(line) == True
    assert parser.parse(line) == {"first": "value1", "second": "value2"}


def test_regex_based_parser():
    parser = LineParserFactory.get_parser("regex", "number", r"\d+")
    line = "test number 123 string"
    assert parser.matched(line) == True
    assert parser.parse(line) == {"number": "123"}


def test_regex_based_parser_multiple_patterns():
    parser = LineParserFactory.get_parser(
        "regex", "key", {"digits": r"\d+", "word": r"[a-zA-Z]+"}
    )
    line = "test123key"
    assert parser.matched(line) == True
    assert parser.parse(line) == {"digits": "123", "word": "test"}


def test_parser_with_preprocess():
    def preprocess(line):
        return line.upper()

    parser = LineParserFactory.get_parser("position", "test", 2, preprocess=preprocess)
    line = "some test value"
    assert parser.matched(line) == True
    assert parser.parse(line) == {"test": "VALUE"}


def test_invalid_parser_type():
    with pytest.raises(ValueError):
        LineParserFactory.get_parser("invalid", "test", 1)


def test_generic_line_parser():
    test_line1 = "Type Call on CAD 1,234.56"
    test_line2 = "Type Down & Out Put on USD 2,345.67"

    put_builder: LineParserArgumentBuilder = LineParserArgument.builder("Put on")
    put_builder.add_key_regex("Put_Currency", r"Put on\s+([A-Z]{3})")
    put_builder.add_key_regex("Put_Amount", r"\s+([\d,]+\.?\d*)")
    put_builder.add_key_regex("Sub_Type", r"Type\s+(.*)\sPut")
    put_parser = GenericLineParser(put_builder.build())

    call_builder: LineParserArgumentBuilder = LineParserArgument.builder("Call on")
    call_builder.add_key_regex("Call_Currency", r"Call on\s+([A-Z]{3}) ")
    call_builder.add_key_regex("Call_Amount", r"\s+([\d,]+\.?\d*)")
    call_builder.add_key_regex("Sub_Type", r"Type\s+(.*)\sCall")
    call_builder.add_key_position("Type", 0)
    call_parser = GenericLineParser(call_builder.build())

    assert put_parser.matched(test_line1) == False
    assert put_parser.matched(test_line2) == True
    print(put_parser.parse(test_line2))

    assert call_parser.matched(test_line2) == False
    assert call_parser.matched(test_line1) == True
    print(call_parser.parse(test_line1))
