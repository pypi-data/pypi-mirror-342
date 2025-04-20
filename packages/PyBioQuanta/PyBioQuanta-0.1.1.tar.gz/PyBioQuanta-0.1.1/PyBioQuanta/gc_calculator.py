def gc_content(seq):
    gc_count = sum(1 for base in seq.upper() if base in "GC")
    return (gc_count / len(seq)) * 100 if seq else 0
