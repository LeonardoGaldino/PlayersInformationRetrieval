def map_number_to_range(num: int) -> str:
    if num < 25:
        quart = "[0-24]"
    elif num > 74:
        quart = "[75-99]"
    else:
        if num < 50:
            quart = "[25-49]"
        else:
            quart = "[50-74]"
    return quart
