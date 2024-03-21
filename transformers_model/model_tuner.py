from transformers import RobertaTokenizer, RobertaForSequenceClassification, Trainer, TrainingArguments
import pandas as pd
from datasets import Dataset
from pydriller import Repository

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('./logs/training.log')


""" This section is for loading the example dataset to be trained on, preparing the data for training, 
setting up the training arguments, fine-tuning the model, and evaluating the model. """

""" Preprocess (load and tokenize the dataset) """

# Load the dataset using Pandas DataFrame (df).
df = pd.read_csv("customized_dataset.csv")
# Map human-readable labels for numeric values.
label_dict = {
    "Bug Fix": 0, "Feature Addition": 1, "Documentation": 2, "Refactoring": 3, "Performance": 4,
    "Cleanup": 5, "Security": 6, "Styling/Front-End": 7, "Update": 8, "Setup": 9, "Testing": 10,
    "Git operations": 11
}
# Replace the text labels in the df with their corresponding numeric values.
df['label'] = df['label'].apply(lambda x: label_dict[x])
# Convert the Pandas DataFrame into Dataset object from dataset library, to be compatible with Hugging Face
# transformers library
dataset = Dataset.from_pandas(df)
print(f"Dataset from pandas: {dataset}")

# Load the tokenizer. It breaks down the text into tokens, adding special tokens like [CLS] and [SEP], and converting
# these tokens into numerical IDs that the model can process. It is loaded from the pre_trained tokenizer from codebert.
model_name = "microsoft/codebert-base"
tokenizer = RobertaTokenizer.from_pretrained(model_name)

def tokenize_function(examples):
    """
    Tokenize the message from examples dataset. It calls the tokenizer on the list of text messages, converts them into
    a format suitable for the model (converting words to token IDs).
    The padding ensures all tokenized outputs are padded to the same length.
    Truncates the texts to the model's maximum input size if they are too long.
    :param examples: dataset with text messages to be tokenized.
    :return: the processed (tokenized) version of the input batch, which replaces the original batch in the dataset.
    """
    return tokenizer(examples["message"], padding="max_length", truncation=True)

# Tokenize the dataset. The .map() iterates over the dataset, applying the method to each example/batch of examples.
# The examples argument is a dictionary where each key corresponds to a column in the dataset.
tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Split the dataset into two parts; training set and test set. 0.2 means that 20% of the data should be used for
# the test set, and remaining 80% will be for the training set.
train_test_split = tokenized_datasets.train_test_split(test_size=0.2)
# Extract the training set.
train_dataset = train_test_split['train']
# Extract the test set.
test_dataset = train_test_split['test']

print(f"Train Dataset: {train_dataset}")
print(f"Test Dataset: {test_dataset}")

""" Setting up and training the model. """

# Define training arguments. This will be adjusted later when the dataset is larger (now it is only 60).

# Warmup steps: Gradually increases learning rate to stabilize early training, useful for adapting pre-trained models.
# Weight decay: Penalizes large weights to prevent overfitting, encouraging simpler models.
# Per device batch size: Number of examples processed at once on each device, balances speed and model accuracy.
training_args = TrainingArguments(
    output_dir="./results",          # Output directory for model checkpoints
    num_train_epochs=5,             # Number of training epochs TODO lower when batch is larger (for example 3).
    per_device_train_batch_size=4,   # Batch size for training TODO increase when batch is larger (for example 16).
    per_device_eval_batch_size=4,    # Batch size for evaluation TODO increase when batch is larger (for example 64).
    warmup_steps=50,                 # Number of warmup steps for learning rate scheduler TODO increase when batch is larger (for example 500).
    weight_decay=0.01,               # Strength of weight decay
    logging_dir="./logs",            # Directory for storing logs
    logging_steps=5,                # Log metrics every 10 steps
    evaluation_strategy="epoch",     # Evaluate each `logging_steps`
    learning_rate=2e-5,
)

# Load the model
model = RobertaForSequenceClassification.from_pretrained(model_name, num_labels=len(label_dict))

# Initialize the Trainer
trainer = Trainer(
    model=model,                         # The instantiated 🤗 Transformers model to be trained
    args=training_args,                  # Training arguments, defined above
    train_dataset=train_dataset,         # Training dataset
    eval_dataset=test_dataset,           # Evaluation dataset
)

# Train the model
trainer.train()

# Evaluate the model
print("Starting evaluation...")
results = trainer.evaluate(test_dataset)
print("Evaluation completed.")
print(results)

# Save the model and tokenizer
model.save_pretrained('./results/model')
tokenizer.save_pretrained('./results/model')

# In the output console:
# [it/s]: Iterations per second
# eval_loss: Show's the models performance on the evaluation set at different points during training. Lower means that it's
# improving in predicting the correct labels for the input data
# epochs: each epoch processes the entire training dataset once, the model is evaluated after each epoch.



