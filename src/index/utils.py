from functools import reduce

from index.document import IndexDocument

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

def generate_pairs(rank: [IndexDocument]) -> [(int, int)]:
    pairs = []
    for i in range(0, len(rank)-1):
        for j in range(i+1, len(rank)):
            pairs.append((rank[i].id, rank[j].id))

    return pairs

def kendal_tau(rank1: [IndexDocument], rank2: [IndexDocument]) -> float:
    if len(rank1) != len(rank2):
        raise ValueError("Rank1 has different size than Rank2: {} - {}.".format(str(len(rank1)), str(len(rank2))))

    rank_size = len(rank1)
    num_pairs = float(rank_size)*float(rank_size-1)/2.0

    p1 = generate_pairs(rank1)
    p2 = generate_pairs(rank2)

    p1_not_in_p2 = reduce(lambda acc, p: acc if p in p2 else acc+1, p1, 0)
    p2_not_in_p1 = reduce(lambda acc, p: acc if p in p1 else acc+1, p2, 0)

    disagreeing_pairs = p1_not_in_p2 + p2_not_in_p1

    return (1.0 - disagreeing_pairs/num_pairs)
