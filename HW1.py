
# Reads RNA in FASTA format from a file
# Parameter filename: A string containing the relative path of the file from where
# this program is stored
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
                    gene_line.replace(str(i), '')
                    
                # - Remove whitespace
                gene_line.replace(' ', '')
                gene_line.replace('\n', '')
                
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

# This a lookup table that converts 3 character amino acids to
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
    '*'  : '*'
}

# Sets up a dictionary that matches 3 RNA nucleotides to their corresponding
# amino acid or to Stop (denoted by '*')
# Return: The dictionary object that converts 3 nucleotide code to protein
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

# Converts an RNA sequence into the corresponding amino acid sequence. Does not
# yet handle stop codons besides adding stop
# Parameter RNA: The RNA sequence in string format
# Parameter table: The dictionary that pairs RNA to amino acids
# Parameter single_letter: if this value is True AA is in single character IUPAC codes 
#                          if this value is False AA is in 3 character codes
# Return: A list containing the amino acid sequence
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

# This is the main function of our translation program
def main():
    # Read the file into a dictionary of genes
    genes = readFile("Assignment1Sequences.txt")
    
    # Initialize the lookup table
    AATable = setUpTable()
    
    # Holds the resulting genes in AA format
    AASeqs = {}
    for gene in genes:
        # Convert RNA string to AA format and store in the 
        # AASeqs dictionary
        AASeqs[gene] = (convertToAAs(genes[gene], AATable, single_letter = True))
    
    # This part is for displaying the genes and their AA sequences
    for gene in AASeqs:
        print('{}:\n{}\n'.format(gene, ''.join(AASeqs[gene])))
    
if __name__ == '__main__':
    main()
