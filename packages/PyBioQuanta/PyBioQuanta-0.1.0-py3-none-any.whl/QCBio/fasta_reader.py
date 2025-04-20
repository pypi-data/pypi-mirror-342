def read_fasta(file_path):
    sequences = {}
    with open(file_path, 'r') as f:
        header = None
        seq = ''
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if header:
                    sequences[header] = seq
                header = line[1:]
                seq = ''
            else:
                seq += line
        if header:
            sequences[header] = seq
    return sequences
