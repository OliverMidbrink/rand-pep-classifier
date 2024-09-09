import random
import tools
import dataset


seqs = tools.get_filtered_seq_list()

for seq in seqs:
    # Gen a reandom seq of equal length

    rand_seq = ""

    for x in range(len(seq) - 1):
        next_char = random.choice(tools.unique_chars)
        while next_char == "|" or next_char == "+":
            next_char = random.choice(tools.unique_chars)
        rand_seq += next_char

    rand_seq += "|"
    
    with open("rand_seqs.txt", "a") as f:
        f.write(rand_seq + "\n")