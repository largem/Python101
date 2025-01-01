import pytest
import sys
import os

# start from project root
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../"))
from line_parser.line_parser import LineParser, GenericLineParser
import line_parser.line_parser_factory as factory
from line_parser.line_parser_argument import (
    LineParserArgument,
    LineParserArgumentBuilder,
)


def test_position_based_parser_with_different_delimiter():
    line = "key:value"
    builder: LineParserArgumentBuilder = LineParserArgument.builder("key")
    builder.add_key_position("key", 1).with_split_delimiter(":")
    parser: LineParser = GenericLineParser(builder.build())

    assert parser.matched(line) == True
    assert parser.parse(line) == {"key": "value"}


def test_position_based_parser():
    parser: LineParser = factory.get_simple_line_parser("key")
    line = "key value"
    assert parser.matched(line) == True
    assert parser.parse(line) == {"key": "value"}


def test_position_based_parser_multiple_positions():
    parser = factory.get_multi_value_line_parser("key", {"first": 1, "second": 2})
    line = "key value1 value2"
    assert parser.matched(line) == True
    assert parser.parse(line) == {"first": "value1", "second": "value2"}


def test_option_line_parser():
    test_line1 = "Type Call   on CAD 1,234.56"
    test_line2 = "Type Down & Out Put     on USD 2,345.67"

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
    test_line4 = "Premium    0.00114 USD   Payment date: 2024/12/10"
    test_line5 = "Counterparty Premium    0.0334  CAD Payment date: 2024/12/11"
    test_line6 = "Settlement Premium     0.0  JPN Payment date: 2024/12/12"

    premium_parser = factory.get_premium_line_parser(factory.PremiumType.Native)
    assert premium_parser.matched(test_line1) == True
    assert premium_parser.matched(test_line2) == False
    assert premium_parser.matched(test_line3) == False
    assert premium_parser.matched(test_line4) == True
    assert premium_parser.matched(test_line5) == False
    assert premium_parser.matched(test_line6) == False
    assert premium_parser.parse(test_line1) == {
        "Premium_Amount": "0.00114",
        "Premium_Currency": "USD",
    }
    assert premium_parser.parse(test_line4) == {
        "Premium_Amount": "0.00114",
        "Premium_Currency": "USD",
        "Payment_Date": "2024/12/10",
    }

    counterparty_premium_parser = factory.get_premium_line_parser(factory.PremiumType.Counterparty)
    assert counterparty_premium_parser.matched(test_line1) == False
    assert counterparty_premium_parser.matched(test_line2) == True
    assert counterparty_premium_parser.matched(test_line3) == False
    assert counterparty_premium_parser.matched(test_line4) == False
    assert counterparty_premium_parser.matched(test_line5) == True
    assert counterparty_premium_parser.matched(test_line6) == False
    assert counterparty_premium_parser.parse(test_line2) == {
        "Counterparty_Premium_Amount": "0.0334",
        "Counterparty_Premium_Currency": "CAD",
    }
    assert counterparty_premium_parser.parse(test_line5) == {
        "Counterparty_Premium_Amount": "0.0334",
        "Counterparty_Premium_Currency": "CAD",
        "Payment_Date": "2024/12/11",
    }

    settlement_premium_parser = factory.get_premium_line_parser(factory.PremiumType.Settlement)
    assert settlement_premium_parser.matched(test_line1) == False
    assert settlement_premium_parser.matched(test_line2) == False
    assert settlement_premium_parser.matched(test_line3) == True
    assert settlement_premium_parser.matched(test_line4) == False
    assert settlement_premium_parser.matched(test_line5) == False
    assert settlement_premium_parser.matched(test_line6) == True
    assert settlement_premium_parser.parse(test_line3) == {
        "Settlement_Premium_Amount": "0.0",
        "Settlement_Premium_Currency": "JPN",
    }
    assert settlement_premium_parser.parse(test_line6) == {
        "Settlement_Premium_Amount": "0.0",
        "Settlement_Premium_Currency": "JPN",
        "Payment_Date": "2024/12/12",
    }


def test_direction_line_parser():
    test_line1 = "  We   Buy"
    test_line2 = "We pay you at"

    line_parser = factory.get_direction_line_parser()
    assert line_parser.matched(test_line1) == True
    assert line_parser.parse(test_line1) == {"TD_Direction": "Buy"}

    assert line_parser.matched(test_line2) == False


def test_ticket_line_parser():
    test_line1 = "AVERAGE OPTION TICKET       123456789 ABC"
    test_line2 = "AVERAGE OPTION TICKET - DTD      123456789 ABC"

    line_parser = factory.get_ticket_line_parser()
    assert line_parser.matched(test_line1) == True
    assert line_parser.parse(test_line1) == {
        "Option_Ticket": "AVERAGE OPTION TICKET",
        "TradeId": "123456789",
    }

    assert line_parser.matched(test_line2) == True
    assert line_parser.parse(test_line2) == {
        "Option_Ticket": "AVERAGE OPTION TICKET - DTD",
        "TradeId": "123456789",
    }


def test_regex_line_parser():
    test_line1 = "Average Type Extract All of this"

    line_parser = factory.get_regex_line_parser("Average Type", r"Average Type (.*)")
    assert line_parser.matched(test_line1) == True
    assert line_parser.parse(test_line1) == {"Average_Type": "Extract All of this"}
