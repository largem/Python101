class LineParserArgument:
    @staticmethod
    def builder(keyword: str) -> "LineParserArgumentBuilder":
        return LineParserArgumentBuilder(keyword)

    def __init__(
        self,
        keyword: str,
        args: dict,
        extra_match: callable = None,
        preprocess: callable = None,
    ) -> None:
        self.keyword = keyword
        self.extract_options = args
        self.extra_match = extra_match
        self.preprocess = preprocess


class LineParserArgumentBuilder:
    def __init__(self, keyword: str) -> None:
        self.keyword = keyword
        self.extract_args = {}
        self.extra_match = None
        self.preprocess = None

    def with_extra_match(self, extra_match: callable) -> "LineParserArgumentBuilder":
        self.extra_match = extra_match
        return self

    def with_preprocess(self, preprocess: callable) -> "LineParserArgumentBuilder":
        self.preprocess = preprocess
        return self

    def add_key_position(self, key: str, pos: int) -> "LineParserArgumentBuilder":
        self.extract_args[key] = pos
        return self

    def set_position(self, pos: int) -> "LineParserArgumentBuilder":
        self.extract_args[self.keyword] = pos
        return self

    def add_key_regex(self, key: str, regex: str) -> "LineParserArgumentBuilder":
        self.extract_args[key] = regex
        return self

    def set_regex(self, regex: str) -> "LineParserArgumentBuilder":
        self.extract_args[self.keyword] = regex
        return self

    def build(self) -> LineParserArgument:
        return LineParserArgument(
            self.keyword, self.extract_args, self.extra_match, self.preprocess
        )
