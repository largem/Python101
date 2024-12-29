import re
from abc import ABC, abstractmethod

class LineParser(ABC):
    @abstractmethod
    def matched(self, line:  str) -> bool:
        pass

    @abstractmethod
    def parse(self, line: str) -> dict:
        pass

class AbstractLineParser(LineParser):
    def __init__(self, keyword: str, preprocess: callable=None) -> None:
        self.keyword = keyword
        self.preprocess = preprocess

    def matched(self, line: str) -> bool:
        return self.keyword in line
    
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
    def __init__(self, keyword: str, pos_args: dict|int, preprocess: callable=None) -> None:
        super().__init__(keyword, preprocess)
        if isinstance(pos_args, int):
            self.pos_args = {keyword: pos_args}   # single position and use  keyword as key
        else:
            self.pos_args = pos_args
    
    def extract(self, line: str) -> dict:
        parts = line.split()
        result = {}
        for key, pos in self.pos_args.items():
            result[key] = parts[pos]
        return result
    
class RegexBasedLineParser(AbstractLineParser):
    def __init__(self, keyword: str, regex_args: dict|str, preprocess: callable=None) -> None:
        super().__init__(keyword, preprocess)
        if isinstance(regex_args, str):
            self.regex = {keyword: regex_args}  # single regex and use keyword as key
        else:
            self.regex = regex_args
    
    def extract(self, line: str) -> dict:
        result = {}
        for key, regex in self.regex.items():
            result[key] = re.search(regex, line).group()
        return result
    
class LineParserFactory:
    @staticmethod
    def get_parser(parser_type: str, keyword: str, args: dict|int|str, preprocess: callable=None) -> LineParser:
        if parser_type == 'position':
            return PositionBasedLineParser(keyword, args, preprocess)
        elif parser_type == 'regex':
            return RegexBasedLineParser(keyword, args, preprocess)
        else:
            raise ValueError(f"Invalid parser type: {parser_type}")
        