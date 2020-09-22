#A possible new solution based on https://academic.oup.com/peds/article/12/7/557/1575362

#Reads RNA in FASTA format from a file
#Parameter filename: A string containing the relative path of the file from where
#this program is stored
#Return: The RNA sequences contained in the file in list format
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

#Sets up a dictionary that matches 3 RNA nucleotides to their corresponding
#amino acid or to Stop
#Return: The dictionary after being set up
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

conforms = {
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

    '*': 0
    }

def convertToAAs(RNA, table, single_letter = False):

    # Initialize the sequence to an empyt list 

    # and the index pointer to 0

    

    seq = []

    current = 0

    

    # Loop over the RNA string length in multiples of 3

    while current + 2 < len(RNA):

        # Convert the RNA condones to amino acids using the

        # look up table

        if single_letter:

            seq.append(triple_letter_to_single_letter[table[RNA[current:current + 3]]])

        else:

            seq.append(table[RNA[current:current + 3]])

            

        current += 3

    

    return seq

hw_hydrophobicity = {   

    'Ala': -0.5,

    'Arg': 3.0,

    'Asn': 0.2,

    'Asp': 3.0,

    'Cys': -1.0,

    'Gln': 0.2,

    'Glu': 3.0,

    'Gly': 0.0,

    'His': -0.5,

    'Ile': -0.8,

    'Leu': -1.8,

    'Lys': -1.3,

    'Met': 3.0,

    'Phe': -2.5,

    'Pro': 0.0,

    'Ser': 0.3,

    'Thr': -0.4,

    'Trp': -3.4,

    'Tyr': -2.3,

    'Val': -1.5,

    '*': 0

}

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

    'Val': 'V'
,
    '*':'*'
}

def ranges(nums):
    nums = sorted(set(nums))
    gaps = [[s, e] for s, e in zip(nums, nums[1:]) if s+1 < e]
    edges = iter(nums[:1] + sum(gaps, []) + nums[-1:])
    return list(zip(edges, edges))

#Main
genes = readFile("Assignment1Sequences.txt")
table = setUpTable()
AASeqs = []
for gene in genes:
    AASeqs.append(convertToAAs(genes[gene], table, single_letter=False))
for seq in AASeqs:
    conform_vals = [conforms[aa] for aa in seq]



    window_length = 20
    some = [0 for i in conform_vals]

    val = 0



    for i in range(window_length):

        if (conform_vals[i] >= 0.8):

            val += 1

        

    some[0] = val



    for i in range(1, len(conform_vals) - window_length + 1):

        val -= 1 if conform_vals[i-1] >= 0.8 else 0

        val += 1 if conform_vals[i + 20 -1] >= 0.8 else 0

        some[i] = val

    high_vals = []
    for i in range(len(some)):
        if some[i] >= 18:
            high_vals.append(i)
    aves = []
    for group in ranges(high_vals):
        aves.append(round(sum(group) / len(group)))
    good_vals = []
    for ave in aves:
        if len(good_vals) == 0 or ave > good_vals[-1] + 20:
            good_vals.append(ave)
    print(aves)
    print(good_vals)

