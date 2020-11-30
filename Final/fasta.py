
# Reads RNA, DNA or Protien sequences in FASTA format from a file
# Parameter filename: A string containing the relative path of the file from
# where this program is stored
# Parameter genes: A dictionary object which should hold the genes read from
# the FASTA file. Therefore this function does not have a return value
def readFASTAFile(filename, genes, limit=10):
    # Open the file and initialize the dictionary
    file = open(filename, "r")
    for line in file:
        # Remove the newline characters and spaces at the end
        line = line.strip()

        # If the line starts with the '>' character
        # then we can start reading the RNA sequence that starts
        # from the next line
        if line.startswith('>'):

            # The FASTA format allows spaces, numbers and newlines
            # between the sequences

            # List to hold the gene lines
            gene = []

            # Read the first line of the sequence
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

                # Read the next line of sequence
                gene_line = (file.readline()).strip()

            # Add a new gene to the dictionary where
            # Key:   The line that starts with '>'
            #        ('>' character removed)
            # Value: The RNA sequence of the gene
            genes[line[1:limit+1]] = ''.join(gene)

    # Close the file and return the dictionary object
    file.close()