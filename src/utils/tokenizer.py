def tokenize(_input: str) -> [str]:
    separators = ['.', ',', '!', '?', '"', '\n', '\t', '(', ')', '|', ';', '>', '<', '[', ']', '\'', ':', '@', '*']

    for separator in separators: 
        _input = _input.replace(separator, ' ')
    
    words = [word for word in _input.split(' ') if len(word) > 0]
    return words