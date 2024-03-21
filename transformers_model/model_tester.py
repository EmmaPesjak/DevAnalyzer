import torch
from pydriller import Repository
from transformers import RobertaTokenizer, RobertaForSequenceClassification

model_path = "results/model"
tokenizer = RobertaTokenizer.from_pretrained(model_path)
model = RobertaForSequenceClassification.from_pretrained(model_path)

def fetch_commit_messages(repo_url):
    commit_messages = []
    for commit in Repository(repo_url).traverse_commits():
        commit_messages.append(commit.msg)
    return commit_messages

def preprocess_messages(messages, tokenizer):
    tokenized_messages = tokenizer(messages, padding=True, truncation=True, return_tensors="pt")
    return tokenized_messages

def classify_messages(model, tokenized_messages):
    model.eval()  # Put the model in evaluation mode
    with torch.no_grad():  # Disable gradient calculation
        outputs = model(**tokenized_messages)
        predictions = torch.argmax(outputs.logits, dim=-1)
    return predictions

repo_url = input("Enter your repository URL: ")
commit_messages = fetch_commit_messages(repo_url)
tokenized_messages = preprocess_messages(commit_messages, tokenizer)
predictions = classify_messages(model, tokenized_messages)

# Map numerical predictions back to labels
labels = {
    0: "Bug Fix", 1: "Feature Addition", 2: "Documentation", 3: "Refactoring", 4: "Performance",
    5: "Cleanup", 6: "Security", 7: "Styling/Front-End", 8: "Update", 9: "Setup", 10: "Testing",
    11: "Git operations"
}
predicted_labels = [labels[prediction] for prediction in predictions.tolist()]

for message, label in zip(commit_messages, predicted_labels):
    print(f"Message: {message}\nPrediction: {label}\n")
