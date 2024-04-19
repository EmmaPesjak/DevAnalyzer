import torch
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from transformers import BertForSequenceClassification, BertTokenizerFast
from tqdm import tqdm
import numpy as np
from sklearn.metrics import classification_report, f1_score


class CustomDataset(Dataset):
    """Custom Dataset for loading data"""

    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx], dtype=torch.long)
        return item

    def __len__(self):
        return len(self.labels)


def load_model(model_path):
    model = BertForSequenceClassification.from_pretrained(model_path)
    tokenizer = BertTokenizerFast.from_pretrained(model_path)
    return model, tokenizer


def create_data_loader(test_data_path, tokenizer, label_dict, batch_size=16):
    df = pd.read_csv(test_data_path)
    labels = [label_dict.get(label, 0) for label in df['label']]  # default to 0 if label not found
    encodings = tokenizer(df['message'].tolist(), truncation=True, padding=True, max_length=512)
    dataset = CustomDataset(encodings, labels)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=False)
    return loader


def validate_model(model, testing_loader, device):
    model.eval()
    eval_loss = 0
    predictions = []
    true_labels = []

    with tqdm(total=len(testing_loader), desc="Validating") as pbar:
        with torch.no_grad():
            for data in testing_loader:
                inputs = {k: v.to(device) for k, v in data.items() if k != 'labels'}
                labels = data['labels'].to(device)

                outputs = model(**inputs)
                logits = outputs.logits if hasattr(outputs, 'logits') else outputs[0]

                logits = logits.detach().cpu().numpy()
                labels = labels.cpu().numpy()

                preds = np.argmax(logits, axis=1)
                predictions.extend(preds.tolist())
                true_labels.extend(labels.tolist())

                # Calculate loss for validation (optional, requires labels)
                # Uncomment if you need to calculate validation loss
                # loss = criterion(logits, labels)
                # eval_loss += loss.item()

                pbar.update(1)

    # Optionally calculate average loss
    # eval_loss /= len(testing_loader)

    print(f"Validation Loss: {eval_loss}")  # Comment if not calculating loss
    print("F1-Score:", f1_score(true_labels, predictions, average='weighted'))
    print("Classification Report:\n", classification_report(true_labels, predictions))

if __name__ == "__main__":
    model_path = './results/trained_label_model'
    test_data_path = 'labeled_file_dataset.csv'
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    label_list = ['Configuration', 'Documentation', 'Resources', 'Source Code', 'Tests']
    label_dict = {label: i for i, label in enumerate(label_list)}

    model, tokenizer = load_model(model_path)
    test_loader = create_data_loader(test_data_path, tokenizer, label_dict)
    validate_model(model, test_loader, device)