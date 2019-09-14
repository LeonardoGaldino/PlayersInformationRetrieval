import re

numeric_regex = r'[-+]?(\d)*.?(\d)*'
reg = re.compile(numeric_regex)

def tokenize(_input: str) -> [str]:
    separators = ['.', ',', '!', '?', '"', '\n', '\t', 
                '(', ')', '|', ';', '>', '<', '[', ']', '\'', ':', 
                '@', '*', '/', '=', '+']

    for separator in separators: 
        _input = _input.replace(separator, ' ')
    
    words = [word for word in _input.split(' ') if len(word) > 0 and not reg.fullmatch(word)]
    return words