# How to use a pretrained model:
1. Go to the use_model.py file and name the output file name at the start to your desired output name. 
2. Run use_model.py, this will append to the output file. If the program crashes, just restart. 

# How to train a model on a custom peptide dataset:
1. Put your custom dataset in the filtered.txt file, only standard amino acids are allowed. Others should be marked as X. All lines should end with "|", to mark that a line is finished. 
2. use the train_model.py script to train the model.