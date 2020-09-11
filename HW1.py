#Reads RNA in FASTA format from a file
#Parameter filename: A string containing the relative path of the file from where
#this program is stored
#Return: The RNA sequences contained in the file in list format
def readFile(filename):
    f = open(filename, "r")
    genes = []
    for x in f:
        if x is not "\n":
            genes.append(f.readline())
    f.close()
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
        table[key] = "Stop"
    return table

#Converts an RNA sequence into the corresponding amino acid sequence. Does not
#yet handle stop codons besides adding stop
#Parameter RNA: The RNA sequence in string format
#Parameter table: The dictionary that pairs RNA to amino acids
#Return: A string containing the amino acid sequence
def convertToAAs(RNA, table):
    seq = ""
    current = 0
    while current + 2 < len(RNA):
        seq += table[RNA[current:current + 3]]
        current += 3
    return seq

#Main
genes = readFile("Assignment1Sequences.txt")
AATable = setUpTable()
AASeqs = []
for gene in genes:
    AASeqs.append(convertToAAs(gene, AATable))
print(AASeqs)
