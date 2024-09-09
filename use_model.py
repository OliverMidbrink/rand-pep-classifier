import torch
import torch.nn as nn
import model
import tools
import time
import torch.nn.functional as F

model_file = "model_0.pt"

# Load the model as full model not state dict
model_ = torch.load(model_file)

original_seqs = tools.get_filtered_seq_list()

n_seqs = 9600 - 9300

for x in range(n_seqs):
    seq = ""

    while True:
        starting_seq = "+" * (100 - len(seq)) + seq

        # Convert the sequence to one hot
        one_hot = tools.seq_to_one_hot(starting_seq, tools.char_to_int)

        # Flatten the one hot encoding
        one_hot = one_hot.flatten()

        # Forward pass
        output = model_(one_hot)

        #print("output: ", output)

        temperature = 1.7
        output = F.softmax(output / temperature, dim=0)

        next_idx = torch.multinomial(output, 1)

        next_char = tools.unique_chars[next_idx.item()]

        seq += next_char

        #print("seq: ", seq)

        if next_char == "|":
            break
    
    print("Sequence: ", seq)
    if seq in original_seqs:
        print("True")
    else:
        print("False")
    print("")

    with open("synth_seqs.txt", "a") as f:
        f.write(seq + "\n")