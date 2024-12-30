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


class AbstractLineParser(LineParser):
    def __init__(
        self, keyword: str, extra_match: callable = None, preprocess: callable = None
    ) -> None:
        self.keyword = keyword
        self.extra_match = extra_match
        self.preprocess = preprocess

    def matched(self, line: str) -> bool:
        matched = self.keyword in line
        if self.extra_match:
            return matched and self.extra_match(line)
        return matched

    @abstractmethod
    def extract(self, line: str) -> dict:
        pass

    def _preprocess(self, line: str) -> str:
        if self.preprocess:
            line = self.preprocess(line)
        return line

    def parse(self, line: str) -> dict:
        line = self._preprocess(line)
        return self.extract(line)


class PositionBasedLineParser(AbstractLineParser):
    def __init__(
        self,
        keyword: str,
        pos_args: dict | int,
        extra_match: callable = None,
        preprocess: callable = None,
    ) -> None:
        super().__init__(keyword, extra_match, preprocess)
        if isinstance(pos_args, int):
            self.pos_args = {
                keyword: pos_args
            }  # single position and use  keyword as key
        else:
            self.pos_args = pos_args

    def extract(self, line: str) -> dict:
        parts = line.split()
        result = {}
        for key, pos in self.pos_args.items():
            result[key] = parts[pos]
        return result


class RegexBasedLineParser(AbstractLineParser):
    def __init__(
        self,
        keyword: str,
        regex_args: dict | str,
        extra_match: callable = None,
        preprocess: callable = None,
    ) -> None:
        super().__init__(keyword, extra_match, preprocess)
        if isinstance(regex_args, str):
            self.regex = {keyword: regex_args}  # single regex and use keyword as key
        else:
            self.regex = regex_args

    def extract(self, line: str) -> dict:
        result = {}
        for key, regex in self.regex.items():
            result[key] = re.search(regex, line).group()
        return result


class GenericLineParser(LineParser):
    def __init__(
        self,
        args: LineParserArgument,
    ) -> None:
        self.args = args

    def matched(self, line: str) -> bool:
        matched = self.args.keyword in line
        if matched and self.args.extra_match:
            return self.args.extra_match(line)
        return matched

    def parse(self, line: str) -> dict:
        line = self.args.preprocess(line) if self.args.preprocess else line
        result = {}
        for key, option in self.args.extract_options.items():
            if isinstance(option, int):
                result[key] = line.split()[option]
            elif isinstance(option, str):
                match: re.Match = re.search(option, line)
                if match:
                    if len(match.groups()) > 0:
                        # we only support extract one value
                        result[key] = match.group(1)
                    else:
                        result[key] = match.group()
            else:
                raise ValueError(f"Invalid argument type: {type(option)}")
        return result


class LineParserFactory:
    @staticmethod
    def get_parser(
        parser_type: str,
        keyword: str,
        args: dict | int | str,
        extra_match: callable = None,
        preprocess: callable = None,
    ) -> LineParser:
        if parser_type == "position":
            return PositionBasedLineParser(keyword, args, extra_match, preprocess)
        elif parser_type == "regex":
            return RegexBasedLineParser(keyword, args, extra_match, preprocess)
        else:
            raise ValueError(f"Invalid parser type: {parser_type}")
