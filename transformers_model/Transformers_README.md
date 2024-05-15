This directory contains various scripts, datasets, and sub-directories:

- **Directories:**
  - `commit_messages/` - Contains the mined commit messages with and without labels used when fine-tuning the commit message BERT model.
  - `file_paths/` - Contains the mined commit file paths with and without labels used when fine-tuning the file path BERT model.
  - `model_results/` - Contains CSV files with fine-tuning data from both models.
  - `readmes/` - Contains the mined README.mds for summarization.

- **Scripts and Files:**
  - `bert_filepath_model.py` - Code for fine-tuning the file path BERT model. *Note: Running this script requires significant computational power, time, and storage space.*
  - `bert_message_model.py` - Code for fine-tuning the commit message BERT model. *Note: Running this script requires significant computational power, time, and storage space.*
  - `commit_mining.py` - Helper script for mining label data.
  - `data_loader.py` - Helper class for handling tokenized text data and corresponding labels.
  - `eval_loss_diagram.py` - Helper script for displaying evaluation data for trained models.
  - `get_labels.py` - Helper script for getting all labels from a dataset.

- **Datasets:**
  - `labeled_filepath_dataset.csv` - The complete dataset used for the fine-tuning of the file path BERT model.
  - `labeled_message_dataset.csv` - The complete, labeled dataset used for the fine-tuning of the commit message BERT model.