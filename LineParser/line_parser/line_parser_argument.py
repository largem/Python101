class LineParserArgument:

    DEFAULT_CONFIG = {"override_match": False, "split_delimiter": None}

    @staticmethod
    def builder(keyword: str) -> "LineParserArgumentBuilder":
        return LineParserArgumentBuilder(keyword)

    def __init__(
        self,
        keyword: str,
        args: dict,
        config: dict = dict(DEFAULT_CONFIG),
        extra_match: callable = None,
        preprocess: callable = None,
    ) -> None:
        self.keyword = keyword
        self.extract_args = args
        self.config = config
        self.extra_match = extra_match
        self.preprocess = preprocess

    def override_match(self) -> bool:
        return self.config["override_match"]

    def get_split_delimiter(self) -> str:
        return self.config["split_delimiter"]


class LineParserArgumentBuilder:
    def __init__(self, keyword: str) -> None:
        self.keyword = keyword
        self.extract_args = {}
        self.extra_match = None
        self.preprocess = None
        self.config = dict(LineParserArgument.DEFAULT_CONFIG)

    def with_extra_match(self, extra_match: callable) -> "LineParserArgumentBuilder":
        self.extra_match = extra_match
        self.config["override_match"] = False
        return self

    def with_match(self, match_override: callable) -> "LineParserArgumentBuilder":
        self.extra_match = match_override
        self.config["override_match"] = True
        return self

    def with_preprocess(self, preprocess: callable) -> "LineParserArgumentBuilder":
        self.preprocess = preprocess
        return self

    def add_key_position(self, key: str, pos: int) -> "LineParserArgumentBuilder":
        self.extract_args[key] = pos
        return self

    def add_key_regex(self, key: str, regex: str) -> "LineParserArgumentBuilder":
        self.extract_args[key] = regex
        return self

    def with_split_delimiter(self, delimiter: str) -> "LineParserArgumentBuilder":
        self.config["split_delimiter"] = delimiter
        return self

    def build(self) -> LineParserArgument:
        return LineParserArgument(
            self.keyword,
            self.extract_args,
            self.config,
            self.extra_match,
            self.preprocess,
        )
