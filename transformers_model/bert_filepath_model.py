import sys
import pandas as pd
from transformers import BertForSequenceClassification, BertTokenizerFast
from transformers import TrainingArguments, Trainer
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from torch import cuda
from transformers_model.data_loader import DataLoader
from sklearn.model_selection import train_test_split
import numpy as np
import shutil
import os


def clear_directory(path):
    """
    Removes old training data.
    :param path: is the path to the specific split.
    """
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


# Ask user whether to clear BERT model and continue or terminate the script.
user_input = input("Do you want to clear BERT and continue? (yes/no): ")
if user_input.lower() != 'yes':
    print("Terminating the program.")
    sys.exit()

# Check if a CUDA-compatible GPU is available to enable GPU acceleration and optimize
# the training session. Training on a GPU is usually significantly faster than on a CPU.
device = 'cuda' if cuda.is_available() else 'cpu'

# Load the dataset using Pandas DataFrame, contains the data that will be used for training the model.
df_org = pd.read_csv("labeled_filepath_dataset.csv")
# Shuffle the dataset to ensure that the training process doesn't get biased by the order of the data.
# The random_state is set to a fixed value to ensure that the shuffling is reproducible.
df_org = df_org.sample(frac=1.0, random_state=42)

# Get the label names from the training set. This list of labels represents the different
# categories that the model will learn to distinguish.
labels = df_org['label'].unique().tolist()
labels = [s.strip() for s in labels]
# print(f"Labels:\n{labels}")   Can print this to verify labels.

# Count the number of unique labels, which will be used to specify the
# number of output neurons in the model (one for each label).
NUM_LABELS = len(labels)

# Create two dictionaries for mapping. These mappings are essential for converting between the
# numerical outputs of the model and the human-readable labels.
id2label = {idx: label for idx, label in enumerate(labels)}
label2id = {label: idx for idx, label in enumerate(labels)}
# print(label2id)  Can print this to verify the mappings.
# print(id2label)

# Creates a new column in the DataFrame ("labels") that contains the numerical ID for each label.
# This step is crucial for training the model, as machine learning models work with numerical data rather
# than text labels.
df_org["labels"] = df_org.label.map(lambda x: label2id[x.strip()])
# print(df_org.head())   Can print to verify.

# Print out the label distribution in percentages.
print(f"Label Distribution in Percentages:\n{df_org.label.value_counts(normalize=True) * 100}")

# The tokenizer converts text into tokens that the BERT model can understand.
tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased", max_length=512)
# A BERT model specifically for sequence classification is initialized with the same bert-base-uncased
# pre-trained weights. It's configured for the number of unique labels in our dataset and is informed
# about the label mappings (id2label and label2id). This allows the model to output predictions
# corresponding to the classes of our dataset.
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=NUM_LABELS, id2label=id2label,
                                                      label2id=label2id)

# Update the configuration with label2id and id2label.
model.config.label2id = label2id
model.config.id2label = id2label

# Ensure the model utilizes the GPU if available, falling back on the CPU otherwise.
model.to(device)

# Constants for the experiment.
num_splits = 15
test_size = 0.2
seed_values = [19, 42, 123, 2023, 777, 101, 333, 888, 999, 444, 246, 555, 666, 777, 222]

# Lists to store loss scores from each split.
loss_scores = []
results = []


def compute_metrics(pred):
    """
    Computes accuracy, F1, precision, and recall for a given set of predictions.

    Args:
        pred (obj): An object containing label_ids and predictions attributes.
            - label_ids (array-like): A 1D array of true class labels.
            - predictions (array-like): A 2D array where each row represents
              an observation, and each column represents the probability of
              that observation belonging to a certain class.

    Returns:
        dict: A dictionary containing the following metrics:
            - Accuracy (float): The proportion of correctly classified instances.
            - F1 (float): The macro F1 score, which is the harmonic mean of precision
              and recall. Macro averaging calculates the metric independently for
              each class and then takes the average.
            - Precision (float): The macro precision, which is the number of true
              positives divided by the sum of true positives and false positives.
            - Recall (float): The macro recall, which is the number of true positives
              divided by the sum of true positives and false negatives.
    """
    # Extract true labels from the input object.
    true_labels = pred.label_ids

    # Obtain predicted class labels by finding the column index with the maximum probability.
    preds = pred.predictions.argmax(-1)

    # Compute macro precision, recall, F1 score, and accuracy using sklearn.
    precision, recall, f1, _ = precision_recall_fscore_support(true_labels, preds, average='macro')
    acc = accuracy_score(true_labels, preds)
    return {
        'Accuracy': acc,
        'F1': f1,
        'Precision': precision,
        'Recall': recall
    }


# Loop through multiple splits and train the model.
for i, seed_value in enumerate(seed_values):
    # Define output directory for each split.
    output_dir = f'./results/filepaths/split_{i}'
    clear_directory(output_dir)

    # Split the data.
    train_texts, test_texts, train_labels, test_labels = train_test_split(df_org['message'], df_org['labels'],
                                                                          test_size=test_size, random_state=seed_value)

    # Tokenize data.
    train_encodings = tokenizer(list(train_texts), truncation=True, padding=True)
    test_encodings = tokenizer(list(test_texts), truncation=True, padding=True)

    # Create data loaders.
    train_dataloader = DataLoader(train_encodings, list(train_labels))
    test_dataset = DataLoader(test_encodings, list(test_labels))

    # Define training arguments and create Trainer.
    training_args = TrainingArguments(
        output_dir=output_dir,
        do_train=True,
        num_train_epochs=3,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=32,
        learning_rate=2e-5,
        warmup_steps=21,
        weight_decay=0.01,
        evaluation_strategy="steps",
        eval_steps=50,
        save_strategy="steps",
        fp16=False,  # Remove this line if training on a GPU.
        load_best_model_at_end=True
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataloader,
        eval_dataset=test_dataset,
        compute_metrics=compute_metrics
    )

    # Train and evaluate the model.
    trainer.train()

    # Manually save the model and tokenizer.
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)

    eval_results = trainer.evaluate()

    # Store results along with identifying information.
    results.append({
        'split_index': i,
        'seed_value': seed_value,
        'loss': eval_results['eval_loss'],
        'accuracy': eval_results.get('eval_Accuracy'),
        'f1': eval_results.get('eval_F1'),
        'precision': eval_results.get('eval_Precision'),
        'recall': eval_results.get('eval_Recall')
    })
    print(f"Results for split {i}: {eval_results}")

    # Store and print the loss score
    loss_score = eval_results['eval_loss']
    loss_scores.append(loss_score)

# Calculate the average loss score and standard deviation.
average_loss_score = np.mean(loss_scores)
std_deviation = np.std(loss_scores)
print("Average Loss Score:", average_loss_score)
print("Standard Deviation:", std_deviation)

# Convert list of results to a DataFrame for easier analysis.
df_results = pd.DataFrame(results)

# Compute average metrics.
if 'accuracy' in df_results.columns and df_results['accuracy'].notna().any():
    average_accuracy = df_results['accuracy'].mean()
    print("Average Accuracy:", average_accuracy)
else:
    print("Accuracy data unavailable.")

if 'f1' in df_results.columns and df_results['f1'].notna().any():
    average_f1 = df_results['f1'].mean()
    print("Average F1 Score:", average_f1)
else:
    print("F1 Score data unavailable.")

if 'precision' in df_results.columns and df_results['precision'].notna().any():
    average_precision = df_results['precision'].mean()
    print("Average Precision:", average_precision)
else:
    print("Precision data unavailable.")

if 'recall' in df_results.columns and df_results['recall'].notna().any():
    average_recall = df_results['recall'].mean()
    print("Average Recall:", average_recall)
else:
    print("Recall data unavailable.")

print("-------------------------")

best_by_loss = df_results.loc[df_results['loss'].idxmin()]
print("Best split by loss:", best_by_loss)
