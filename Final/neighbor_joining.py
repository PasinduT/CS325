# Implement the neighbor joining algorithm here
import pprint
pp = pprint.PrettyPrinter(indent = 4)

# This function will make a cladogram using the neighbor joining algorithm. The
# output will be in the form of tuples
# dist_dict: a nxn distance matrix stored in the form of nested dictionaries.
#            ex: {
#                   "A": {"B": 3},
#                   "B": {"A": 3},
#                }
def make_cladogram (dist_dict):
    

    while (len(dist_dict) > 2): 
        mini = calculate_min_Q(dist_dict)
        

        d, a, b = mini
        da, db = calculate_distance_to_pair(dist_dict, a, b)

        new_node = (a, da, b, db)

        dista = dist_dict[a]
        distb = dist_dict[b]
        del dist_dict[a]
        del dist_dict[b]
        store = list(dist_dict.keys())
        dist_dict[new_node] = {}

        for c in store:
            nd = (dista[c] + distb[c] - dista[b]) / 2
            dist_dict[new_node][c] = nd
            dist_dict[c][new_node] = nd

        # print(mini)
        # pp.pprint(dist_dict)

    a, b = tuple(dist_dict.keys())
    d = dist_dict[a][b]
    return (a, d, b)

def calculate_distance_to_pair (some, a, b):
    total = 0
    
    for k in some:
        if k != a:
            total += some[a][k]
        
        if k != b:
            total -= some[b][k]
    
    total = total / (len(some) - 2)
    total = (some[a][b] + total) / 2
    return total, some[a][b] - total

# This function calculates the distance between two nodes in the neighbor 
# joining algorithm
def calculateAverageD (first, second, some):
    tot = 0
    for c in some:
        if c != first or c == second:
            tot += some[first][c]
        
        if c != second:
            tot += some[second][c]
        # tot += some[first][c] + some[c][second]
    return tot 

def calculate_min_Q (dist_dict):

    # Just a large value with random data to start off (terrible I know) 
    # TODO: fix it to get the first/random distance
    mini = (10000000, dist_dict[list(dist_dict.keys())[0]], 
            dist_dict[list(dist_dict.keys())[0]])

    keys = list(dist_dict.keys())
    for i in range(len(keys) - 1):
        for j in range(i + 1, len(keys)):
            a, b = keys[i], keys[j]
            d = (len(keys) - 2) * dist_dict[a][b] - calculateAverageD(a, b, dist_dict)
            if d < mini[0]:
                mini = (d, a, b)
    
    return mini

# This function tests the above algorithm
def test ():
    from distance import dJC
    import upgma

    t = {
        'a': {'b': 5, 'c': 9, 'd': 9, 'e': 8},
        'b': {'a': 5, 'c': 10, 'd': 10, 'e': 9},
        'c': {'a': 9, 'b': 10, 'd': 8, 'e': 7},
        'd': {'a': 9, 'b': 10, 'c': 8, 'e': 3},
        'e': {'a': 8, 'b': 9, 'c': 7, 'd': 3},
    }


    # pp.pprint(t)

    res = make_cladogram(t)

    print(res)

    import output_tree
    output_tree.output_tree(res, "testing", "mytree.png")

if __name__ == '__main__':
    test()