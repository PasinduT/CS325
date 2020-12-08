# Implement the neighbor joining algorithm here
import pprint
pp = pprint.PrettyPrinter(indent = 4)

# This function will make a cladogram using the neighbor joining algorithm. The
# output will be in FORMAT_1
# dist_dict: the distance matrix in FORMAT_2
# Return: the resulting tree in FORMAT_1
def make_cladogram (dist_dict):
    # As long as there are more than two disconnected nodes in the tree,
    # calculate the minimum value from the Q matrix and then combine those nodes
    # together in the final tree.
    while (len(dist_dict) > 2): 

        # Get the minimum distance in the Q matrix
        mini = calculate_min_Q(dist_dict)

        # Get the distance, and the two nodes (a, b)
        d, a, b = mini

        # Calculate the distance between the two nodes to the new node
        # da is the distance from 'a' to the new node and db is the distance 
        # from 'b' to the new node 
        da, db = calculate_distance_to_pair(dist_dict, a, b)

        # Make the new node with the distance from the child nodes to it,
        # spliced in between
        new_node = (a, da, b, db)

        # Get the distances from node 'a', and 'b' to every other node, and
        # delete that entry from the distance matrix
        dista = dist_dict[a]
        distb = dist_dict[b]
        del dist_dict[a]
        del dist_dict[b]

        # Store a list of the nodes that remain to be joined together as keys
        keys = list(dist_dict.keys())

        # Add the new node to the distance matrix
        dist_dict[new_node] = {}

        # Calculate the distance between the new node and every other node and
        # store it in the correct positions in the distance matrix
        for c in keys:
            nd = (dista[c] + distb[c] - dista[b]) / 2
            dist_dict[new_node][c] = nd
            dist_dict[c][new_node] = nd

    # Get the last two nodes remaining as 'a', and 'b'.
    a, b = tuple(dist_dict.keys())

    # Get the distance between 'a' and 'b'
    d = dist_dict[a][b]

    # Return the topmost node as 'a', the distance between 'a' and 'b', and 'b'
    # as a tuple (in accordance with FORMAT_1)
    return (a, d, b)

# TODO: rename this function and its variables
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
# TODO: rename this function and its variables
def calculateAverageD (first, second, some):
    tot = 0
    for c in some:
        if c != first or c == second:
            tot += some[first][c]
        
        if c != second:
            tot += some[second][c]
        # tot += some[first][c] + some[c][second]
    return tot 

# This function calculates the Q matrix from the neighbor joining algorithm 
# and then returns the minimum entry within it
# dist_dict: the distance matrix in FORMAT_2
# Return: the minimum entry in the Q matrix generated for the given distance
#         matrix
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

# This function tests the above algorithm using the example given at
# https://en.wikipedia.org/wiki/Neighbor_joining
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