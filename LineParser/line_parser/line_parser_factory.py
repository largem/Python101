from enum import Enum

from line_parser.line_parser import LineParser, GenericLineParser
from line_parser.line_parser_argument import (
    LineParserArgumentBuilder,
    LineParserArgument,
)


# A regular expression pattern that matches a numeric amount, including optional commas and decimal places.
REGEX_AMOUNT = r"[\d,]+\.?\d*"
REGEX_CURR = r"[A-Z]{3}"


class OptionType(Enum):
    Call = 0
    Put = 1


def get_option_line_parser(option_type: OptionType) -> LineParser:
    keyword = f"{option_type.name} on"
    builder: LineParserArgumentBuilder = LineParserArgument.builder(keyword)
    builder.add_key_regex(
        f"{option_type.name}_Currency", keyword + rf"\s+({REGEX_CURR})"
    )
    builder.add_key_regex(f"{option_type.name}_Amount", rf"\s+({REGEX_AMOUNT})")
    builder.add_key_regex("Sub_Type", rf"Type\s+(.*)\s{option_type.name}")
    return GenericLineParser(builder.build())


def get_strike_line_parser():
    keyword = "Strike"
    builder: LineParserArgumentBuilder = LineParserArgument.builder(keyword)
    builder.add_key_regex(keyword, REGEX_AMOUNT)
    return GenericLineParser(builder.build())
