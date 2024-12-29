
import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))    
from line_parser.line_parser import LineParserFactory, LineParser

def test_position_based_parser():
    parser: LineParser = LineParserFactory.get_parser('position', 'test', 1)
    line = "some test value"
    assert parser.matched(line) == True
    assert parser.parse(line) == {'test': 'test'}

def test_position_based_parser_multiple_positions():
    parser = LineParserFactory.get_parser('position', 'key', {'first': 0, 'second': 2})
    line = "value1 key value2"
    assert parser.matched(line) == True
    assert parser.parse(line) == {'first': 'value1', 'second': 'value2'}

def test_regex_based_parser():
    parser = LineParserFactory.get_parser('regex', 'number', r'\d+')
    line = "test number 123 string"
    assert parser.matched(line) == True
    assert parser.parse(line) == {'number': '123'}

def test_regex_based_parser_multiple_patterns():
    parser = LineParserFactory.get_parser('regex', 'key', {
        'digits': r'\d+',
        'word': r'[a-zA-Z]+'
    })
    line = "test123key"
    assert parser.matched(line) == True
    assert parser.parse(line) == {'digits': '123', 'word': 'test'}

def test_parser_with_preprocess():
    def preprocess(line):
        return line.upper()
    
    parser = LineParserFactory.get_parser('position', 'test', 2, preprocess)
    line = "some test value"
    assert parser.matched(line) == True
    assert parser.parse(line) == {'test': 'VALUE'}

def test_invalid_parser_type():
    with pytest.raises(ValueError):
        LineParserFactory.get_parser('invalid', 'test', 1)