# Reads RNA in FASTA format from a file
# Parameter filename: A string containing the relative path of the file from
# where this program is stored
# Return: The RNA sequences contained in the file in a dictionary format
def readFile(filename):
    # Open the file and initialize the dictionary
    file = open(filename, "r")
    genes = {}
    for line in file:
        # Remove the newline characters and spaces at the end
        line = line.strip()

        # If the line starts with the '>' character
        # then we can start reading the RNA sequence that starts
        # from the next line
        if line.startswith('>'):

            # The FASTA format allows spaces, numbers and newlines
            # between the RNA sequences

            # List to hold the gene lines
            gene = []

            # Read the first line of the RNA string
            gene_line = file.readline()

            # While the gene_line is not empty
            while (gene_line):
                # Clean the line
                # - Remove the numbers
                for i in range(10):
                    gene_line = gene_line.replace(str(i), '')

                # - Remove whitespace
                gene_line = gene_line.replace(' ', '')
                gene_line = gene_line.replace('\n', '')

                # If the resulting line is not empty, add it to
                # the list of gene_lines
                if gene_line:
                    gene.append(gene_line)

                # Read the next line of RNA string
                gene_line = (file.readline()).strip()

            # Add a new gene to the dictionary where
            # Key:   The line that starts with '>'
            #        ('>' character removed)
            # Value: The RNA sequence of the gene
            genes[line[1:]] = ''.join(gene)

    # Close the file and return the dictionary object
    file.close()
    return genes


# Sets up a dictionary that matches 3 RNA nucleotides to their corresponding
# amino acid or to Stop
# Return: The dictionary after being set up
def setUpTable():
    table = {}
    for key in ["UUU", "UUC"]:
        table[key] = "Phe"
    for key in ["UUA", "UUG", "CUU", "CUC", "CUA", "CUG"]:
        table[key] = "Leu"
    for key in ["AUU", "AUC", "AUA"]:
        table[key] = "Ile"
    for key in ["AUG"]:
        table[key] = "Met"
    for key in ["GUU", "GUC", "GUA", "GUG"]:
        table[key] = "Val"
    for key in ["UCU", "UCC", "UCA", "UCG", "AGU", "AGC"]:
        table[key] = "Ser"
    for key in ["CCU", "CCC", "CCA", "CCG"]:
        table[key] = "Pro"
    for key in ["ACU", "ACC", "ACA", "ACG"]:
        table[key] = "Thr"
    for key in ["GCU", "GCC", "GCA", "GCG"]:
        table[key] = "Ala"
    for key in ["UAU", "UAC"]:
        table[key] = "Tyr"
    for key in ["CAU", "CAC"]:
        table[key] = "His"
    for key in ["CAA", "CAG"]:
        table[key] = "Gln"
    for key in ["AAU", "AAC"]:
        table[key] = "Asn"
    for key in ["AAA", "AAG"]:
        table[key] = "Lys"
    for key in ["GAU", "GAC"]:
        table[key] = "Asp"
    for key in ["GAA", "GAG"]:
        table[key] = "Glu"
    for key in ["UGU", "UGC"]:
        table[key] = "Cys"
    for key in ["UGG"]:
        table[key] = "Trp"
    for key in ["CGU", "CGC", "CGA", "CGG", "AGA", "AGG"]:
        table[key] = "Arg"
    for key in ["GGU", "GGC", "GGA", "GGG"]:
        table[key] = "Gly"
    for key in ["UAA", "UAG", "UGA"]:
        table[key] = "*"
    return table

# A dictionary to hold the conformational parameters
conformational_parameters = {
    'Ala': 1.334,
    'Arg': 0.169,
    'Asn': 0.494,
    'Asp': 0.171,
    'Cys': 1.062,
    'Gln': 0.343,
    'Glu': 0.168,
    'Gly': 0.998,
    'His': 0.530,
    'Ile': 1.803,
    'Leu': 1.623,
    'Lys': 0.115,
    'Met': 1.413,
    'Phe': 1.707,
    'Pro': 0.563,
    'Ser': 0.817,
    'Thr': 0.838,
    'Trp': 1.274,
    'Tyr': 1.146,
    'Val': 1.599,
    '*'  : 0
}

# Converts an RNA sequence into the corresponding amino acid sequence.
# Stop codones are denoted by '*'
# Parameter RNA: The RNA sequence in string format
# Parameter table: The dictionary that pairs RNA to amino acids
# Parameter single_letter: AA are in single character IUPAC codes (True)
#                          AA are in 3 character codes (False)
# Return: A list containing the amino acid sequence
def convertToAAs(RNA, table, single_letter=False):
    # Initialize the sequence to an empyt list
    # and the index pointer to 0
    seq = []
    current = 0

    # Loop over the RNA string length in multiples of 3
    while current + 2 < len(RNA):

        # Convert the RNA condons to amino acids using the
        # look up table
        if single_letter:
            seq.append(
                triple_letter_to_single_letter[table[RNA[current:current + 3]]]
            )
        else:
            seq.append(table[RNA[current:current + 3]])

        current += 3

    return seq

# This a lookup table that converts 3 character amino acids codes to
# single character IUPAC codes
triple_letter_to_single_letter = {
    'Ala': 'A',
    'Arg': 'R',
    'Asn': 'N',
    'Asp': 'D',
    'Asx': 'B',
    'Cys': 'C',
    'Gln': 'Q',
    'Glu': 'E',
    'Glx': 'Z',
    'Gly': 'G',
    'His': 'H',
    'Ile': 'I',
    'Leu': 'L',
    'Lys': 'K',
    'Met': 'M',
    'Phe': 'F',
    'Pro': 'P',
    'Ser': 'S',
    'Thr': 'T',
    'Trp': 'W',
    'Tyr': 'Y',
    'Val': 'V',
    '*': '*'
}

# Finds sequences of numbers in a sorted set
# ex. [1, 2, 3, 4, 6, 7, 9] -> [(1,4), (6,7), (9, 9)]
# Parameter nums: the sorted set to find the ranges in
# Return: Returns a list of the ranges found
def ranges(nums):
    # creates ranges of the gaps in between sequences
    gaps = [[s, e] for s, e in zip(nums, nums[1:]) if s+1 < e]
    # adds the first and last elements of the list to the beggining and ends of
    # the gaps, and makes an iterator over the new set
    edges = iter(nums[:1] + sum(gaps, []) + nums[-1:])
    # returns a list of pairs generated using zip
    # because edges is an iterator, the first element is pair with the second, 
    # then the third with the fourth and so on
    return list(zip(edges, edges))


# This method formats the output in a nice way
# Parameter good_indexes: the list of the predicted transmembrane domains
# Parameter gene: the name of the gene
# Parameter sequence: the full amino acid sequence (using three letter codes)
def format_output(good_indexes, gene, sequence):
    print('{}: {}\n'.format(gene, good_indexes))

    for start, end in good_indexes:
        # Make sure to include the last element
        end = end + 1
        # Convert the sequence to single letter codes
        seq = [triple_letter_to_single_letter[aa] for aa in sequence[start:end]]
        # Convert to string
        seq = ''.join(seq)
        # Add spaces inbetween the string
        seq = ' '.join([seq[i:i+5] for i in range(0, len(seq), 5)])
        print('{} {}'.format(start, seq))

    print()

# The main function
def main():
    # Read the RNA sequences
    genes = readFile("Assignment1Sequences.txt")

    # Set up the look up table
    table = setUpTable()

    # Calculate convert the RNA sequences to amino acid sequences and store
    # them in a dictionary
    AASeqs = {}
    for gene in genes:
        AASeqs[gene] = convertToAAs(genes[gene], table, single_letter=False)

    # Loop through every converted gene
    for gene in AASeqs:
        # Get the amino acid sequence for this gene
        aa_sequence = AASeqs[gene]

        # Convert the amino acid sequence to a conformational parameters list
        conform_vals = [conformational_parameters[aa] for aa in aa_sequence]

        # Use a sliding window of length 20
        window_length = 20

        # A list to hold the indexes of windows which have 18 or more
        # conformational parameters greater than or equal to 0.8
        high_indexes = []

        # Initialize the counter to 0
        count = 0
        for i in range(window_length):
            if (conform_vals[i] >= 0.8):
                count += 1

        # If more than 18 conformational parameters with values greater than 
        # or equal to 0.8 are found then add the index of the start of the 
        # window to the high_indexes list
        if (count >= 18):
            high_indexes.append(0)

        # Keep sliding the window over until the last sliding position
        for i in range(1, len(conform_vals) - window_length + 1):
            # At each new position remove the conformational parameter at the 
            # beginning of the previous window and add the conformational 
            # parameter at the end of the current window
            count -= 1 if conform_vals[i-1] >= 0.8 else 0
            count += 1 if conform_vals[i + 20 - 1] >= 0.8 else 0


            # If more than 18 conformational parameters with values greater than 
            # or equal to 0.8 are found then add the index of the start of the 
            # window to the high_indexes list
            if count >= 18:
                high_indexes.append(i)

        # Finds the average of each range of indices and sets it as a potential
        # start location
        potential_indexes = []
        for group in ranges(high_indexes):
            potential_indexes.append(round(sum(group) / len(group)))
            
        good_indexes = []
        # Filter the potential indexes so that we don't have any overlapping
        # transmembrane domains (TMD)
        for start_position in potential_indexes:
            # Check if the transmembrane domain is spaced at least 20 amino
            # acids from the previous one
            if len(good_indexes) == 0 or \
                start_position > good_indexes[-1][0] + 20:

                # Calculate the ending position of the TMD
                end_position = start_position + window_length - 1
                good_indexes.append((start_position, end_position))

        # Print the output
        format_output(good_indexes, gene, aa_sequence)



if __name__ == '__main__':
    main()
