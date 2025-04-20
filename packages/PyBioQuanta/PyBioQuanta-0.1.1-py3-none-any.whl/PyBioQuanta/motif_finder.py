def find_motif(seq, motif):
    positions = []
    seq = seq.upper()
    motif = motif.upper()
    for i in range(len(seq) - len(motif) + 1):
        if seq[i:i+len(motif)] == motif:
            positions.append(i + 1)  
    return positions