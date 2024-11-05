import dataset
import tools
import model
import torch
from tqdm import tqdm
import json

seed = dataset.seed
n_CV_splits = dataset.n_CV_splits

training_results = {}
device = torch.device("cpu")

model_name = "micro"

for split_idx in tqdm(range(n_CV_splits), desc="Splits"):
    
    train, test = dataset.get_train_test(split_idx)

    # Create the model
    # Input format: 100 context size (padding + data) * 23 chars
    # Architecture: whatever you want
    # Output format: probability of each next token

    model_ = model.SimpleAutoregressiveModel().to(device)

    # Loss function
    criterion = torch.nn.CrossEntropyLoss()

    # Optimizer
    optimizer = torch.optim.Adam(model_.parameters(), lr=1e-3)
    print("LR: ", optimizer.param_groups[0]['lr'])

    # Training loop
    n_epochs = 100

    for epoch in tqdm(range(n_epochs), desc="Epochs"):

        train_loss = 0
        model_.train()
        train_tqdm_bar = tqdm(train, desc="Train")
        for seq in train_tqdm_bar:

            #print("seq: ", seq)

            for char_idx in range(len(seq)):
                sub_seq = seq[:char_idx]
                #print("sub_seq: ", sub_seq)
                # Pad the sequence with "+" to make it 100 characters long
                if len(sub_seq) > 100:
                    sub_seq = sub_seq[-100:]
                input_seq = "+" * (100 - len(sub_seq)) + sub_seq

                # Convert the sequence to one hot
                one_hot = tools.seq_to_one_hot(input_seq, tools.char_to_int)

                # Flatten the one hot encoding
                one_hot = one_hot.flatten().to(device)

                #print("one_hot: ", one_hot.shape)

                # Forward pass
                output = model_(one_hot)

                #print("OUTPUT: ", output)  

                next_char = seq[char_idx] 
                #print("next_char: ", next_char)

                next_char_one_hot = tools.seq_to_one_hot(next_char, tools.char_to_int).squeeze(0).to(device)
                #print("next_char_one_hot: ", next_char_one_hot)

                # Compute the loss
                loss = criterion(output, next_char_one_hot)
                train_loss += loss.item()
                #print("loss: ", loss)
                # Show loss on train bar
                #train_tqdm_bar.set_postfix({"loss": loss.item()})

                # Backward pass
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

        training_results["train" + "_" + str(epoch) + "_" + str(split_idx)] = train_loss
        
        with open("training_results.json", "w") as f:
            json.dump(training_results, f)

        # Get the validation loss
        val_loss = 0
        model_.eval()

        for seq in tqdm(test, desc="Test"):
            for char_idx in range(len(seq)):
                sub_seq = seq[:char_idx]
                # Pad the sequence with "+" to make it 100 characters long
                if len(sub_seq) > 100:
                    sub_seq = sub_seq[-100:]
                input_seq = "+" * (100 - len(sub_seq)) + sub_seq

                # Convert the sequence to one hot
                one_hot = tools.seq_to_one_hot(input_seq, tools.char_to_int)

                # Flatten the one hot encoding
                one_hot = one_hot.flatten().to(device)

                # Forward pass
                output = model_(one_hot)

                next_char = seq[char_idx] 

                next_char_one_hot = tools.seq_to_one_hot(next_char, tools.char_to_int).squeeze(0).to(device)

                # Compute the loss
                loss = criterion(output, next_char_one_hot)

                val_loss += loss.item()

        training_results["val" + "_" + str(epoch) + "_" + str(split_idx)] = val_loss

        with open("training_results.json", "w") as f:
            json.dump(training_results, f)

        # Save the model
        torch.save(model_, model_name + "_ep_" + str(epoch) + ".pt")