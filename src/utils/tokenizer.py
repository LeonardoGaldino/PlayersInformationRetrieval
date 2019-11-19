import re

numeric_regex = r'[-+]?(\d)*.?(\d)*'
reg = re.compile(numeric_regex)

def tokenize(_input: str, accept_nums: bool = False) -> [str]:
    if _input is None:
        return []

    _input = str(_input)

    separators = ['.', ',', '!', '?', '"', '\n', '\t', 
                '(', ')', '|', ';', '>', '<', '[', ']', '\'', ':', 
                '@', '*', '/', '=', '+']

    for separator in separators: 
        _input = _input.replace(separator, ' ')
    
    words = [word for word in _input.split(' ') if len(word) > 0 and (accept_nums or not reg.fullmatch(word))]
    return words