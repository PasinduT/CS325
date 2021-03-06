import heapq
import json
# Implement the UPGMA algorithm here

# This function implements the UPGMA algorithm, however, we didn't use it in 
# our final submission. Therefore, it is not commented
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
                break

    if len(dist_dict.keys()) == 1:
        return list(dist_dict.keys())[0]

    raise Exception("More than one tree was created: {}".format(dist_dict))


# This function makes a nxn distance matrix that is stored in the form of a 
# dictionary 
# seqs: a dictionary with the sequence names and their distances
# d_func: the distance function that will be used to calculate the distance 
#         between each sequence
# filename: (Default: None) if a filename is supplied, then a JSON version
#           of the resulting dictionary object will be stored in the given 
#           filename
# Returns: the distance matrix between all the sequences in FORMAT_2
def make_dist_dict (seqs, d_func, filename=None): 
    # Make an empty dictionary to hold the distance matrix
    dist_dict = {}

    keys = list(seqs.keys())

    # Add all the keys to the distance matrix and initialize them with empty
    # dictionaries.
    for i in range(len(seqs)):
        dist_dict[keys[i]] = {}

    # Calculate the distance between each sequence and every other sequence
    # and store the appropriate locations in the dictionary.
    for i in range(len(seqs) - 1):
        for j in range(i + 1, len(seqs)):
            d = d_func(seqs[keys[i]], seqs[keys[j]])
            dist_dict[keys[i]][keys[j]] = d
            dist_dict[keys[j]][keys[i]] = d

    # If a filename is give, then output the the distance matrix to the file
    # in JSON format.
    if filename:
        with open(filename, 'w') as file:
            json.dump(dist_dict, file)


    return dist_dict

# A smalll test method to test the UPGMA algorithm with the Jukes-Cantor 
# distance model
def test():
    from distance import dJC

    t = {
        'A': "ATATAT",
        'B': "ATTTTT",
        'C': "ATATAA",
        'D': "TTTTTT"
    }
    
    some = make_dist_dict(t, dJC)

    print(some)

    res = make_cladogram(some)

    print(res)

if __name__ == "__main__":
    test()
        

