from enum import Enum

from line_parser.line_parser import LineParser, GenericLineParser
from line_parser.line_parser_argument import (
    LineParserArgumentBuilder,
    LineParserArgument,
)
from utils import string_utils as su

# A regular expression pattern that matches a numeric amount, including optional commas and decimal places.
REGEX_AMOUNT = r"[\d,]+\.?\d*"
REGEX_CURR = r"[A-Z]{3}"


class OptionType(Enum):
    Call = 0
    Put = 1


class PremiumType(Enum):
    Native = 0
    Counterparty = 1
    Settlement = 2


# define some quick functions
def exclude_word(*words: str):
    def _inner_func_(builder: LineParserArgumentBuilder, *words: str) -> None:
        builder.with_extra_match(lambda line: not su.contains_any(line, words))

    return lambda builder: _inner_func_(builder, *words)


# key-value pair style, but can be flexible to handle value in different positions
def get_simple_line_parser(
    keyword: str, key: str = None, pos: int = 1, extra_build: callable = None
) -> LineParser:
    builder: LineParserArgumentBuilder = LineParserArgument.builder(keyword)
    key = keyword if not key else key
    builder.add_key_position(key, pos)
    if extra_build:
        extra_build(builder)
    return GenericLineParser(builder.build())


# extract multiple values from a line
def get_multi_value_line_parser(
    keyword: str, key_pos: dict, extra_build: callable = None
) -> LineParser:
    builder: LineParserArgumentBuilder = LineParserArgument.builder(keyword)

    for key, pos in key_pos.items():
        builder.add_key_position(key, pos)

    if extra_build:
        extra_build(builder)

    return GenericLineParser(builder.build())


def get_regex_based_line_parser(
    keyword: str, key: str = None, regex: str = None, extra_build: callable = None
) -> LineParser:
    key = su.combine_camel_words(keyword) if not key else key
    regex = regex if regex else rf"{keyword}\s+(.+)"
    builder: LineParserArgumentBuilder = LineParserArgument.builder(keyword)
    builder.add_key_regex(key, regex)

    if extra_build:
        extra_build(builder)

    return GenericLineParser(builder.build())


def get_option_line_parser(option_type: OptionType) -> LineParser:
    keyword = f"{option_type.name}on"
    builder: LineParserArgumentBuilder = LineParserArgument.builder(keyword)
    builder.with_match(lambda line: keyword in line.replace(" ", ""))
    builder.add_key_regex(
        f"{option_type.name}_Currency", rf"{option_type.name}\s+on\s+({REGEX_CURR})"
    )
    builder.add_key_regex(f"{option_type.name}_Amount", rf"\s+({REGEX_AMOUNT})")
    builder.add_key_regex("Sub_Type", rf"Type\s+(.+)\s+{option_type.name}")
    return GenericLineParser(builder.build())


def get_strike_line_parser() -> LineParser:
    keyword = "Strike"
    builder: LineParserArgumentBuilder = LineParserArgument.builder(keyword)
    builder.add_key_regex(keyword, REGEX_AMOUNT)
    return GenericLineParser(builder.build())


def get_premium_line_parser(premium_type: PremiumType) -> LineParser:
    keyword = f"{premium_type.name} Premium" if premium_type != PremiumType.Native else "Premium"
    builder: LineParserArgumentBuilder = LineParserArgument.builder(keyword)
    amount_key = "Premium_Amount"
    currency_key = "Premium_Currency"
    if premium_type != PremiumType.Native:
        amount_key = f"{premium_type.name}_{amount_key}"
        currency_key = f"{premium_type.name}_{currency_key}"
    builder.add_key_regex(amount_key, REGEX_AMOUNT)
    builder.add_key_regex(currency_key, rf"{REGEX_AMOUNT}\s+({REGEX_CURR})")
    # TODO, Payment Date should have its own parser
    builder.add_key_regex("Payment_Date", r"Payment date:\s+(.*)")
    if premium_type == PremiumType.Native:
        # "Seller" is a special case
        exclude_word(PremiumType.Counterparty.name, PremiumType.Settlement.name, "Seller")(builder)

    return GenericLineParser(builder.build())


def get_direction_line_parser() -> LineParser:
    keyword = "We"
    builder: LineParserArgumentBuilder = LineParserArgument.builder(keyword)
    # Being lazy here, just use number of words to distinguish
    builder.with_extra_match(lambda line: len(line.split()) == 2)
    builder.add_key_position("TD_Direction", 1)
    return GenericLineParser(builder.build())


def get_ticket_line_parser() -> LineParser:
    keyword = "TICKET"
    builder: LineParserArgumentBuilder = LineParserArgument.builder(keyword)
    builder.add_key_regex("Option_Ticket", r"(.*?)\d+")
    builder.add_key_regex("TradeId", r"\d+")

    return GenericLineParser(builder.build())
