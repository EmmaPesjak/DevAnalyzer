import pandas as pd

def get_label_list_from_csv(csv_file_path, label_column_name):
    df = pd.read_csv(csv_file_path)
    unique_labels = df[label_column_name].unique()
    label_list = sorted(unique_labels)  # Sorting is optional but helps in consistent ordering
    return label_list


# Example usage
csv_file_path = 'labeled_dataset.csv'
label_column_name = 'label'
label_list = get_label_list_from_csv(csv_file_path, label_column_name)
print(label_list)
