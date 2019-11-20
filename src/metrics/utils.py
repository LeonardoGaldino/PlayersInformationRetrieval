from math import sqrt

def avg_sd(data: [int]) -> (float, float):
    n = float(len(data))
    if n == 1:
        raise ValueError("Single value does not have defined standard deviation.")
    
    avg = float(sum(data))/n

    _sum = 0.0
    for data_point in data:
        _sum += (data_point - avg)*(data_point - avg)

    return (avg, sqrt(_sum/(n-1)))
