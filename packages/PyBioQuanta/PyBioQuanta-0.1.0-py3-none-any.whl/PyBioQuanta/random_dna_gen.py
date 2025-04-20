import random

def generate_random_dna(length):
    return ''.join(random.choices('ATCG', k=length))
