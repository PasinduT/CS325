# Implement the neighbor joining algorithm here

def make_cladogram (dist_dict):
    pq = []

    for a, v in dist_dict.items():
        for b, d in v.items():
            heapq.heappush(pq, (d, a, b))

    while (len(pq) > 0):
        d, a, b = heapq.heappop(pq)

        if (a not in dist_dict) or (b not in dist_dict):
            continue

        new_item = (a, b)

        dista = dist_dict[a]
        distb = dist_dict[b]

        del dist_dict[a]
        del dist_dict[b]

        store = list(dist_dict.keys())

        dist_dict[new_item] = {}

        for c in store: 
            d = (dista[c] + distb[c]) / 2
            dist_dict[new_item][c] = d
            dist_dict[c][new_item] = d
            heapq.heappush(pq, (d, c, new_item))

    if len(dist_dict.keys()) == 1:
        return list(dist_dict.keys())[0]

    raise Exception("More than one tree was created: {}".format(dist_dict))