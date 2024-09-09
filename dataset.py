import tools
import random 

dataset = tools.get_filtered_seq_list()

n_data = len(dataset)
n_CV_splits = 5

seed = 42

random.seed(seed)
random.shuffle(dataset)

# Split the data into 5 folds
split_indexes = [int(n_data * i / n_CV_splits) for i in range(n_CV_splits + 1)]

split_parts = [dataset[split_indexes[i]:split_indexes[i + 1]] for i in range(n_CV_splits)]

def get_train_test(cv_index): # The CV index will be the test set
    test = split_parts[cv_index]
    train = []
    for i, part in enumerate(split_parts):
        if i != cv_index:
            train += part
    return train, test



