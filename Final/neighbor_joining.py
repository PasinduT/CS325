# Implement the neighbor joining algorithm here

# This function will make a cladogram using the neighbor joining algorithm. The
# output will be in the form of tuples
# dist_dict: a nxn distance matrix stored in the form of nested dictionaries.
#            ex: {
#                   "A": {"B": 3},
#                   "B": {"A": 3},
#                }
def make_cladogram (dist_dict):
    dist_dict, mini = calculate_dist_dict(dist_dict)

    while (len(dist_dict) > 1): 
        d, a, b = mini
        
        new_node = (a, b)

        dista = dist_dict[a]
        distb = dist_dict[b]
        del dist_dict[a]
        del dist_dict[b]
        store = list(dist_dict.keys())
        dist_dict[new_node] = {}

        for c in store:
            nd = (dista[c] + distb[c] - d) / 2
            dist_dict[new_node][c] = nd
            dist_dict[c][new_node] = nd
        dist_dict, mini = calculate_dist_dict(dist_dict)

    return list(dist_dict.keys())[0]

# This function calculates the distance between two nodes in the neighbor 
# joining algorithm
def calculateAverageD (first, second, some):
    if len(some) < 3:
        return 0
    tot = 0
    for c in some:
        if c == first or c == second:
            continue
        tot += some[first][c] + some[c][second]
    return tot / (len(some) - 2)

def calculate_dist_dict (dist_dict):
    res = {}
    for i in dist_dict:
        res[i] = {}

    # Just a large value with random data to start off (terrible I know) 
    # TODO: fix it to get the first/random distance
    mini = (10000000, dist_dict[list(dist_dict.keys())[0]], 
            dist_dict[list(dist_dict.keys())[0]])

    keys = list(dist_dict.keys())
    for i in range(len(dist_dict) - 1):
        for j in range(i + 1, len(dist_dict)):
            a, b = keys[i], keys[j]
            d = dist_dict[a][b] - calculateAverageD(a, b, dist_dict)
            res[a][b] = d
            res[b][a] = d
            if d < mini[0]:
                mini = (d, a, b)
    
    return res, mini

# This function tests the above algorithm
def test ():
    from distance import dJC
    import upgma

    t = {
        'A': "ATATAT",
        'B': "ATTTTT",
        'C': "ATATAA",
        'D': "TTTTTT"
    }
    
    some = upgma.make_dist_dict(t, dJC)

    print(some)

    res = make_cladogram(some)

    print(res)

    import output_tree
    output_tree.output_tree(res, "testing", "mytree.png")

if __name__ == '__main__':
    test()