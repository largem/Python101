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


def test_option_line_parser():
    test_line1 = "Type Call on CAD 1,234.56"
    test_line2 = "Type Down & Out Put on USD 2,345.67"

    put_parser = factory.get_option_line_parser(factory.OptionType.Put)
    call_parser = factory.get_option_line_parser(factory.OptionType.Call)

    assert put_parser.matched(test_line1) == False
    assert put_parser.matched(test_line2) == True
    assert put_parser.parse(test_line2) == {
        "Put_Currency": "USD",
        "Put_Amount": "2,345.67",
        "Sub_Type": "Down & Out",
    }

    assert call_parser.matched(test_line2) == False
    assert call_parser.matched(test_line1) == True
    assert call_parser.parse(test_line1) == {
        "Call_Currency": "CAD",
        "Call_Amount": "1,234.56",
    }


def test_strike_line_parser():
    test_line1 = "Strike    0.00114USD-CAD"
    test_line2 = "Strike    0.0334  USD-CAD"

    strike_parser = factory.get_strike_line_parser()

    assert strike_parser.matched(test_line1) == True
    assert strike_parser.parse(test_line1) == {"Strike": "0.00114"}

    assert strike_parser.matched(test_line2) == True
    assert strike_parser.parse(test_line2) == {"Strike": "0.0334"}


def test_premium_line_parser():
    test_line1 = "Premium    0.00114 USD"
    test_line2 = "Counterparty Premium    0.0334  CAD"
    test_line3 = "Settlement Premium     0.0  JPN"
    test_line4 = "Premium    0.00114 USD   Payment Date: 2024/12/10"
    test_line5 = "Counterparty Premium    0.0334  CAD Payment Date: 2024/12/11"
    test_line6 = "Settlement Premium     0.0  JPN Payment Date: 2024/12/12"

    premium_parser = factory.get_premium_line_parser(factory.PremiumType.Native)
    assert premium_parser.matched(test_line1) == True
    assert premium_parser.matched(test_line2) == False
    assert premium_parser.matched(test_line3) == False
    assert premium_parser.matched(test_line4) == True
    assert premium_parser.matched(test_line5) == False
    assert premium_parser.matched(test_line6) == False
    print(premium_parser.parse(test_line1))
    print(premium_parser.parse(test_line4))

    counterparty_premium_parser = factory.get_premium_line_parser(
        factory.PremiumType.Counterparty
    )
    assert counterparty_premium_parser.matched(test_line1) == False
    assert counterparty_premium_parser.matched(test_line2) == True
    assert counterparty_premium_parser.matched(test_line3) == False
    assert counterparty_premium_parser.matched(test_line4) == False
    assert counterparty_premium_parser.matched(test_line5) == True
    assert counterparty_premium_parser.matched(test_line6) == False
    print(counterparty_premium_parser.parse(test_line2))
    print(counterparty_premium_parser.parse(test_line5))

    settlement_premium_parser = factory.get_premium_line_parser(
        factory.PremiumType.Settlement
    )
    assert settlement_premium_parser.matched(test_line1) == False
    assert settlement_premium_parser.matched(test_line2) == False
    assert settlement_premium_parser.matched(test_line3) == True
    assert settlement_premium_parser.matched(test_line4) == False
    assert settlement_premium_parser.matched(test_line5) == False
    assert settlement_premium_parser.matched(test_line6) == True
    print(settlement_premium_parser.parse(test_line3))
    print(settlement_premium_parser.parse(test_line6))
