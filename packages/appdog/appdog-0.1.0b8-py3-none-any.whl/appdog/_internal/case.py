import re

from .typing import CHAR_MARK, CHAR_SEP


def to_pascal_case(string: str) -> str:
    """Convert a string to pascal case."""
    if not string:
        return string
    s = string
    s = re.sub(r'[\s\-\_]', CHAR_SEP, s)
    s = re.sub(r'(?<![^a-zA-Z\d])(?=[A-Z][a-z\d]+)', CHAR_SEP, s)
    s = re.sub(rf'^{CHAR_SEP}+|{CHAR_SEP}+$', '', s)
    s = re.sub(rf'{CHAR_SEP}+(.)', lambda m: m.group(1).upper(), s)
    s = re.sub(r'(?:^)(?=[a-zA-Z\d]+)', CHAR_MARK, s)
    s = re.sub(r'(?<=[^a-zA-Z\d])(?=[a-zA-Z\d]+)', CHAR_MARK, s)
    s = re.sub(rf'{CHAR_MARK}+(.)', lambda m: m.group(1).upper(), s)
    return s


def to_snake_case(string: str) -> str:
    """Convert a string to snake case."""
    if not string:
        return string
    s = string
    s = re.sub(r'[\s\-\_]', CHAR_SEP, s)
    s = re.sub(r'(?<![^a-zA-Z\d])(?=[A-Z][a-z\d]+)', CHAR_SEP, s)
    s = re.sub(rf'^{CHAR_SEP}+|{CHAR_SEP}+$', '', s)
    s = re.sub(rf'{CHAR_SEP}+', '_', s)
    return s.lower()


def to_title_case(string: str) -> str:
    """Convert a string to title case."""
    if not string:
        return string
    s = string
    s = re.sub(r'[\s\-\_]', CHAR_SEP, s)
    s = re.sub(r'(?<![^a-zA-Z\d])(?=[A-Z][a-z\d]+)', CHAR_SEP, s)
    s = re.sub(rf'^{CHAR_SEP}+|{CHAR_SEP}+$', '', s)
    s = re.sub(rf'{CHAR_SEP}+(.)', lambda m: ' ' + m.group(1).upper(), s)
    s = re.sub(r'(?:^)(?=[a-zA-Z\d]+)', CHAR_MARK, s)
    s = re.sub(r'(?<=[^a-zA-Z\d])(?=[a-zA-Z\d]+)', CHAR_MARK, s)
    s = re.sub(rf'{CHAR_MARK}+(.)', lambda m: m.group(1).upper(), s)
    return s


def to_name_case(string: str) -> str:
    """Convert a string to name case."""
    if not string:
        return string
    pattern_brackets = r'\{[^\{]*?\}'
    pattern_path = r'[\.\/\\]'
    # Collect all parameters
    params = []
    for match in re.finditer(pattern_brackets, string):
        content = to_snake_case(match.group(0)[1:-1])
        params.append(content)
    # Convert the string
    s = string
    s = re.sub(pattern_brackets, CHAR_SEP, s)
    s = re.sub(pattern_path, CHAR_SEP, s)
    s = to_snake_case(s)
    for count, param in enumerate(params):
        s += '_by_' if count == 0 else '_and_'
        s += param
    return s
