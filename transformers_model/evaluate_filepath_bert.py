import torch
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from transformers import BertForSequenceClassification, BertTokenizerFast
from tqdm import tqdm
import numpy as np
from sklearn.metrics import classification_report, f1_score

""" NOT WORKING NOT SURE IF NEEDED """


class CustomDataset(Dataset):
    """ Custom Dataset for loading data """

    def __init__(self, encodings, labelshej):
        self.encodings = encodings
        self.labels = labelshej

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx], dtype=torch.long)
        return item

    def __len__(self):
        return len(self.labels)


def load_model(model_path):
    """ Function to load the pre-trained model """
    model = BertForSequenceClassification.from_pretrained(model_path)
    tokenizer = BertTokenizerFast.from_pretrained(model_path)
    return model, tokenizer


def create_data_loader(csv_path, tokenizer, label_dict, batch_size=16):
    """ Create a DataLoader from the CSV dataset """
    data_frame = pd.read_csv(csv_path)
    labelshe = [label_dict.get(label, 0) for label in data_frame['label']]
    encodings = tokenizer(data_frame['message'].tolist(), truncation=True, padding=True, max_length=512)
    dataset = CustomDataset(encodings, labelshe)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=False)
    return loader

def evaluate(model, test_loader, criterion):
    model.eval()
    total_loss = 0
    total_acc = 0

    with torch.no_grad():
        for batch in test_loader:
            input_ids, attention_mask, labels = batch
            outputs = model(input_ids, attention_mask)
            loss = criterion(outputs, labels)
            total_loss += loss.item()
            predictions = torch.argmax(outputs, dim=1)
            total_acc += (predictions == labels).sum().item()

    # print(f'Test loss: {total_loss/len(test_loader)} Test acc: {total_acc/len(test_set)*100}%')


def validate_model(model, loader, device):
    """ Validate the model using the given data loader """
    model.eval()
    eval_loss = 0
    predictions = []
    true_labels = []
    criterion = torch.nn.CrossEntropyLoss()  # Define the criterion for loss computation

    with tqdm(total=len(loader), desc="Validating") as pbar:
        with torch.no_grad():
            for data in loader:
                inputs = {k: v.to(device) for k, v in data.items() if k != 'labels'}
                labelsh = data['labels'].to(device)

                outputs = model(**inputs)
                logits = outputs.logits
                loss = criterion(logits, labelsh)
                eval_loss += loss.item()

                logits = logits.detach().cpu().numpy()
                labelsh = labelsh.cpu().numpy()

                preds = np.argmax(logits, axis=1)
                preds_list = list(preds)  # Convert to list if not already
                predictions.extend(preds_list)
                true_labels.extend(labelsh.tolist())

                pbar.update(1)

    eval_loss /= len(loader)
    print(f"Validation Loss: {eval_loss}")
    print("F1-Score:", f1_score(true_labels, predictions, average='weighted'))
    print("Classification Report:\n", classification_report(true_labels, predictions))


if __name__ == "__main__":
    # path_to_model = './results/trained_label_model'
    # csv_file_path = 'labeled_filepath_dataset.csv'
    path_to_model = './results/trained_model'
    csv_file_path = 'labeled_message_dataset.csv'
    computing_device = 'cuda' if torch.cuda.is_available() else 'cpu'
    # labels = ['Configuration', 'Documentation', 'Resources', 'Source Code', 'Tests']
    labels = ['Adaptive', 'Administrative', 'Corrective', 'Other', 'Perfective']
    labels_to_index = {label: i for i, label in enumerate(labels)}

    loaded_model, loaded_tokenizer = load_model(path_to_model)
    data_loader = create_data_loader(csv_file_path, loaded_tokenizer, labels_to_index)
    validate_model(loaded_model, data_loader, computing_device)


# import torch
# import torch.nn as nn
# from torch.utils.data import DataLoader, Dataset
# from transformers import BertForSequenceClassification, BertTokenizerFast
# import pandas as pd
# from tqdm import tqdm
# import numpy as np
# from sklearn.metrics import classification_report, f1_score
#
#
# class CustomDataset(Dataset):
#     """ Custom Dataset for loading data """
#
#     def __init__(self, encodings, labels):
#         self.encodings = encodings
#         self.labels = labels
#
#     def __getitem__(self, idx):
#         item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
#         item['labels'] = torch.tensor(self.labels[idx], dtype=torch.long)
#         return item
#
#     def __len__(self):
#         return len(self.labels)
#
#
# def load_model(model_path):
#     """ Function to load the pre-trained model """
#     model = BertForSequenceClassification.from_pretrained(model_path)
#     tokenizer = BertTokenizerFast.from_pretrained(model_path)
#     return model, tokenizer
#
#
# def create_data_loader(test_data_path, tokenizer, label_dict, batch_size=16):
#     """ Create a DataLoader from the test dataset """
#     df = pd.read_csv(test_data_path)
#     labels = [label_dict.get(label, 0) for label in df['label']]
#     encodings = tokenizer(df['message'].tolist(), truncation=True, padding=True, max_length=512)
#     dataset = CustomDataset(encodings, labels)
#     loader = DataLoader(dataset, batch_size=batch_size, shuffle=False)
#     return loader
#
#
# def validate_model(model, testing_loader, device):
#     model.eval()
#     eval_loss = 0
#     predictions = []
#     true_labels = []
#     criterion = nn.CrossEntropyLoss()  # Define the criterion if you need to compute the loss
#
#     with tqdm(total=len(testing_loader), desc="Validating") as pbar:
#         with torch.no_grad():
#             for data in testing_loader:
#                 inputs = {k: v.to(device) for k, v in data.items() if k != 'labels'}
#                 labels = data['labels'].to(device)
#
#                 outputs = model(**inputs)
#                 logits = outputs.logits
#
#                 # Compute loss if labels are provided
#                 loss = criterion(logits, labels)
#                 eval_loss += loss.item()
#
#                 logits = logits.detach().cpu().numpy()
#                 label_ids = labels.cpu().numpy()
#
#                 preds = np.argmax(logits, axis=1)
#                 predictions.extend(preds.tolist())
#                 true_labels.extend(label_ids.tolist())
#
#                 pbar.update(1)
#
#     eval_loss /= len(testing_loader)
#     print(f"Validation Loss: {eval_loss}")
#     print("F1-Score:", f1_score(true_labels, predictions, average='weighted'))
#     print("Classification Report:\n", classification_report(true_labels, predictions))
#
#
# if __name__ == "__main__":
#     model_path = './results/trained_label_model'
#     test_data_path = 'labeled_filepath_dataset.csv'
#     device = 'cuda' if torch.cuda.is_available() else 'cpu'
#     label_list = ['Configuration', 'Documentation', 'Resources', 'Source Code', 'Tests']
#     label_dict = {label: i for i, label in enumerate(label_list)}
#
#     model, tokenizer = load_model(model_path)
#     test_loader = create_data_loader(test_data_path, tokenizer, label_dict)
#     validate_model(model, test_loader, device)
#
#
#
# # import torch
# # import pandas as pd
# # from torch.utils.data import Dataset, DataLoader
# # from transformers import BertForSequenceClassification, BertTokenizerFast
# # from tqdm import tqdm
# # import numpy as np
# # from sklearn.metrics import classification_report, f1_score
# #
# #
# # class CustomDataset(Dataset):
# #     """Custom Dataset for loading data"""
# #
# #     def __init__(self, encodings, labels):
# #         self.encodings = encodings
# #         self.labels = labels
# #
# #     def __getitem__(self, idx):
# #         item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
# #         item['labels'] = torch.tensor(self.labels[idx], dtype=torch.long)
# #         return item
# #
# #     def __len__(self):
# #         return len(self.labels)
# #
# #
# # def load_model(model_path):
# #     model = BertForSequenceClassification.from_pretrained(model_path)
# #     tokenizer = BertTokenizerFast.from_pretrained(model_path)
# #     return model, tokenizer
# #
# #
# # def create_data_loader(test_data_path, tokenizer, label_dict, batch_size=16):
# #     df = pd.read_csv(test_data_path)
# #     labels = [label_dict.get(label, 0) for label in df['label']]  # default to 0 if label not found
# #     encodings = tokenizer(df['message'].tolist(), truncation=True, padding=True, max_length=512)
# #     dataset = CustomDataset(encodings, labels)
# #     loader = DataLoader(dataset, batch_size=batch_size, shuffle=False)
# #     return loader
# #
# #
# # def validate_model(model, testing_loader, device):
# #     model.eval()
# #     eval_loss = 0
# #     predictions = []
# #     true_labels = []
# #
# #     with tqdm(total=len(testing_loader), desc="Validating") as pbar:
# #         with torch.no_grad():
# #             for data in testing_loader:
# #                 inputs = {k: v.to(device) for k, v in data.items() if k != 'labels'}
# #                 labels = data['labels'].to(device)
# #
# #                 outputs = model(**inputs)
# #                 logits = outputs.logits if hasattr(outputs, 'logits') else outputs[0]
# #
# #                 logits = logits.detach().cpu().numpy()
# #                 labels = labels.cpu().numpy()
# #
# #                 preds = np.argmax(logits, axis=1)
# #                 predictions.extend(preds.tolist())
# #                 true_labels.extend(labels.tolist())
# #
# #                 # Calculate loss for validation (optional, requires labels)
# #                 # Uncomment if you need to calculate validation loss
# #                 loss = criterion(logits, labels)
# #                 eval_loss += loss.item()
# #
# #                 pbar.update(1)
# #
# #     # Optionally calculate average loss
# #     eval_loss /= len(testing_loader)
# #
# #     print(f"Validation Loss: {eval_loss}")  # Comment if not calculating loss
# #     print("F1-Score:", f1_score(true_labels, predictions, average='weighted'))
# #     print("Classification Report:\n", classification_report(true_labels, predictions))
# #
# #
# # if __name__ == "__main__":
# #     model_path = './results/trained_label_model'
# #     test_data_path = 'labeled_filepath_dataset.csv'
# #     device = 'cuda' if torch.cuda.is_available() else 'cpu'
# #     label_list = ['Configuration', 'Documentation', 'Resources', 'Source Code', 'Tests']
# #     label_dict = {label: i for i, label in enumerate(label_list)}
# #
# #     model, tokenizer = load_model(model_path)
# #     test_loader = create_data_loader(test_data_path, tokenizer, label_dict)
# #     validate_model(model, test_loader, device)
