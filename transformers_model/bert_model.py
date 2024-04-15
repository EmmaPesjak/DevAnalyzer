import pandas as pd
from transformers import pipeline, BertForSequenceClassification, BertTokenizerFast
from transformers import TrainingArguments, Trainer
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from torch import cuda
from transformers_model.data_loader import DataLoader

# Check if a CUDA-compatible GPU is available to enable GPU acceleration and optimize
# the training session. Training on a GPU is significantly faster than on a CPU.
device = 'cuda' if cuda.is_available() else 'cpu'

# Load the dataset using Pandas DataFrame, contains the data that will be used for training the model.
df_org = pd.read_csv("labeled_dataset.csv")
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

# Print out the label distribution in percentages
print(f"Label Distribution in Percentages:\n{df_org.label.value_counts(normalize=True) * 100}")

# The tokenizer converts text into tokens that the BERT model can understand.
tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased", max_length=512)
# A BERT model specifically for sequence classification is initialized with the same bert-base-uncased
# pre-trained weights. It's configured for the number of unique labels in our dataset and is informed
# about the label mappings (id2label and label2id). This allows the model to output predictions
# corresponding to the classes of our dataset.
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=NUM_LABELS, id2label=id2label,
                                                      label2id=label2id)
# Ensure the model utilizes the GPU if available, falling back on the CPU otherwise.
# This is critical for efficient training, especially with large models like BERT.
model.to(device)

# Dataset splitting. The dataset is divided into training (50%), validation (25%), and testing (25%)
# sets based on the message column.
SIZE = df_org.shape[0]
train_texts = list(df_org.message[:SIZE // 2])
val_texts = list(df_org.message[SIZE // 2:(3 * SIZE) // 4])
test_texts = list(df_org.message[(3 * SIZE) // 4:])
train_labels = list(df_org.labels[:SIZE // 2])
val_labels = list(df_org.labels[SIZE // 2:(3 * SIZE) // 4])
test_labels = list(df_org.labels[(3 * SIZE) // 4:])

# The training, validation, and test text data are tokenized using the previously initialized tokenizer.
# truncation=True ensures texts longer than the maximum allowed sequence length are truncated,
# and padding=True pads shorter sequences to the maximum length. This standardizes the input size for BERT.
train_encodings = tokenizer(train_texts, truncation=True, padding=True)
val_encodings = tokenizer(val_texts, truncation=True, padding=True)
test_encodings = tokenizer(test_texts, truncation=True, padding=True)

# Custom DataLoader objects are created for each dataset split. These DataLoaders are responsible for
# batching the data and making it iterable for the training loop.
train_dataloader = DataLoader(train_encodings, train_labels)
val_dataloader = DataLoader(val_encodings, val_labels)
test_dataset = DataLoader(test_encodings, test_labels)


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


# This portion of code configures and initiates the training process for the machine learning model
# using the Hugging Face Transformers library, specifically using the Trainer class. The process involves
# setting training arguments, initializing the Trainer, training the model, and then evaluating the
# model's performance on the training, validation, and test datasets.
training_args = TrainingArguments(
    # The output directory where the model predictions and checkpoints will be written.
    output_dir='./results',
    do_train=True,
    do_eval=True,
    #  The number of epochs, defaults to 3.0
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=32,
    # Number of steps used for a linear warmup
    warmup_steps=100,
    weight_decay=0.01,
    logging_strategy='steps',
    # TensorBoard log directory
    logging_dir='./multi-class-logs',
    logging_steps=50,
    evaluation_strategy="steps",
    eval_steps=50,
    save_strategy="steps",
    fp16=False,
    load_best_model_at_end=True
)

# The Trainer class encapsulates the training loop, automatically handling the training,
# evaluation, and prediction loops.
trainer = Trainer(
    # The pre-trained model that will be fine-tuned.
    model=model,
    # The training arguments that we defined above.
    args=training_args,
    train_dataset=train_dataloader,
    eval_dataset=val_dataloader,
    compute_metrics=compute_metrics
)

# Start the training process.
trainer.train()

# Evaluate the model on the training dataset.
train_results = trainer.evaluate(eval_dataset=train_dataloader)
print("Training Set Results:", train_results)

# Evaluate the model on the validation dataset.
val_results = trainer.evaluate(eval_dataset=val_dataloader)
print("Validation Set Results:", val_results)

# Optionally, evaluate the model on the test dataset.
test_results = trainer.evaluate(eval_dataset=test_dataset)
print("Test Set Results:", test_results)

# Print eval results.
q = [train_results, val_results, test_results]
print(pd.DataFrame(q, index=["train", "val", "test"]).iloc[:, :5])

# Save the model and tokenizer.
model_path = "./results/trained_model"
trainer.save_model(model_path)
tokenizer.save_pretrained(model_path)
