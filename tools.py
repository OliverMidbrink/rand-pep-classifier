import pandas as pd
import torch

standard_amino_acid_codes = [
    'A', 'R', 'N', 'D', 'B', 'C', 'E', 'Q', 'Z', 'G', 'H', 'I', 'L', 'K', 
    'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V'
]

def filtered(item): # This will take in an amino acid sequece and filter it. 
    modded_item = str(item)
    for char in str(item):
        if char not in standard_amino_acid_codes:
            modded_item = modded_item.replace(char, "X")
            if char == 'U':
                print(item)
                print(modded_item)
        if char.islower():
            return ""
    return str(modded_item).replace("\n", "").replace("*", "").strip().replace(" ", "") + "|"


def get_filtered_seq_list():
    # Read the data from the xlsx file
    df = pd.read_excel('Luzeena_sORF_Database_2024.xlsx')

    list_ = df["ORF sequence"].values

    filtered_ = [filtered(item) for item in list_ if filtered(item) != ""]

    filtered_ = list(set(filtered_))

    return filtered_


with open("filtered.txt", "r") as f:
    seqs = f.readlines()

unique_chars = set()
num = 0
max_len = 0

for seq in seqs:
    if len(seq) > max_len:
        max_len = len(seq)
    for char in seq:
        # if char is lowercase
        if char.islower():
            num += 1
        if char != "\n":
            unique_chars.add(char)


unique_chars.add('+')

unique_chars = sorted(list(unique_chars))

# Make the chars into one hot encodings
char_to_int = dict((c, i) for i, c in enumerate(unique_chars))
int_to_char = dict((i, c) for i, c in enumerate(unique_chars))

# Use torch to convert a sequence to a matrix of one hot encodings
def seq_to_one_hot(seq, char_to_int):
    # integer encode input data
    integer_encoded = [char_to_int[char] for char in seq]
    # one hot encode
    onehot_encoded = list()
    for value in integer_encoded:
        letter = [0 for _ in range(len(char_to_int))]
        letter[value] = 1
        onehot_encoded.append(letter)
    return torch.tensor(onehot_encoded, dtype=torch.float32)


def argmax_one_hot_to_seq(one_hot, int_to_char):
    seq = ""
    for one_hot_vec in one_hot:
        seq += int_to_char[torch.argmax(one_hot_vec).item()]
    return seq


def run_test():
    # Test the function
    seq = "++++CHKSE|"
    print("Original sequence: ", seq)
    one_hot = seq_to_one_hot(seq, char_to_int)
    print(one_hot)

    print("len(unique_chars): ", len(unique_chars))

    # Test the function
    seq = argmax_one_hot_to_seq(one_hot / 2 + 0.1, int_to_char)
    print("Reconstructed sequence: ", seq)


run_test()