import re
from abc import ABC, abstractmethod

from line_parser.line_parser_argument import LineParserArgument

"""
    Interface for line parsers.
    
    The `LineParser` class defines the interface for parsing lines of text. Concrete
    subclasses must implement the `matched` and `parse` methods to handle the
    parsing logic for specific types of lines.
    
    The `matched` method determines whether a given line should be parsed by the
    line parser, while the `parse` method extracts relevant data from the line and
    returns it as a dictionary.
    """


class LineParser(ABC):
    @abstractmethod
    def matched(self, line: str) -> bool:
        pass

    @abstractmethod
    def parse(self, line: str) -> dict:
        pass


class GenericLineParser(LineParser):
    def __init__(
        self,
        args: LineParserArgument,
    ) -> None:
        self.args = args

    def matched(self, line: str) -> bool:
        if self.args.override_match:
            return self.args.extra_match(line)
        matched = self.args.keyword in line
        if matched and self.args.extra_match:
            return self.args.extra_match(line)
        return matched

    def parse(self, line: str) -> dict:
        line = self.args.preprocess(line) if self.args.preprocess else line
        result = {}
        for key, option in self.args.extract_options.items():
            if isinstance(option, int):
                parts = line.split()
                if option < len(parts):
                    result[key] = parts[option]                
            elif isinstance(option, str):
                match: re.Match = re.search(option, line)
                if match:
                    matched_value = ""
                    if len(match.groups()) > 0:
                        # we only support extract one value
                        matched_value = match.group(1).strip()
                    else:
                        result[key] = match.group().strip()
                    if len(matched_value) > 0:
                        result[key] = matched_value
            else:
                raise ValueError(f"Invalid argument type: {type(option)}")
        return result
