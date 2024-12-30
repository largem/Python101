from line_parser.line_parser import LineParser, GenericLineParser
from line_parser.line_parser_argument import (
    LineParserArgumentBuilder,
    LineParserArgument,
)


def get_option_line_parser(option_type: str) -> LineParser:
    keyword = f"{option_type} on"
    builder: LineParserArgumentBuilder = LineParserArgument.builder(keyword)
    builder.add_key_regex(f"{option_type}_Currency", rf"{keyword}\s+([A-Z]{3})")
    builder.add_key_regex(f"{option_type}_Amount", r"\s+([\d,]+\.?\d*)")
    builder.add_key_regex("Sub_Type", rf"Type\s+(.*)\s{option_type}")
    return GenericLineParser(builder.build())
