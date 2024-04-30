from pathlib import Path
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification, \
    BertForSequenceClassification, BertTokenizerFast


class BertAnalyzer:

    def __init__(self):
        commit_message_model_path = Path(__file__).parent.parent / "transformers_model/results/messages/split_14"
        filepath_model_path = Path(__file__).parent.parent / "transformers_model/results/filepaths/split_14"

        # Load models and tokenizers
        self.commit_message_model = AutoModelForSequenceClassification.from_pretrained(commit_message_model_path)
        self.commit_message_tokenizer = AutoTokenizer.from_pretrained(commit_message_model_path)
        self.filepath_model = BertForSequenceClassification.from_pretrained(filepath_model_path)
        self.filepath_tokenizer = BertTokenizerFast.from_pretrained(filepath_model_path)

        # Check and set id2label if it wasn't loaded properly
        if not hasattr(self.commit_message_model.config, 'id2label'):
            self.commit_message_model.config.id2label = {int(k): v for k, v in
                                                         self.commit_message_model.config.id2label.items()}
            self.commit_message_model.config.label2id = {v: int(k) for k, v in
                                                         self.commit_message_model.config.label2id.items()}
            self.filepath_model.config.id2label = {int(k): v for k, v in
                                                   self.filepath_model.config.id2label.items()}
            self.filepath_model.config.label2id = {v: int(k) for k, v in
                                                   self.filepath_model.config.label2id.items()}

        # Create pipelines
        self.commit_message_nlp = pipeline("text-classification", model=self.commit_message_model,
                                           tokenizer=self.commit_message_tokenizer)
        self.filepath_nlp = pipeline("text-classification", model=self.filepath_model,
                                     tokenizer=self.filepath_tokenizer)

    def analyze_commits(self, commits_dict):
        types_per_user = {}
        types_of_commits = {}
        file_type_predictions_per_user = {}

        for author, commits in commits_dict.items():
            if author not in types_per_user:
                types_per_user[author] = {}
                file_type_predictions_per_user[author] = {}

            for commit_message, file_paths in commits:
                # Classify the commit message
                prediction = self.commit_message_nlp(commit_message)
                predicted_label = prediction[0]['label']

                # Initialize commit label counts
                types_per_user[author].setdefault(predicted_label, 0)
                types_of_commits.setdefault(predicted_label, 0)

                # Update commit label counts
                types_per_user[author][predicted_label] += 1
                types_of_commits[predicted_label] += 1

                # Classify each file path modified in this commit
                for file_path in file_paths:
                    file_prediction = self.filepath_nlp(file_path)
                    file_type_label = file_prediction[0]['label']

                    # Initialize file type counts
                    file_type_predictions_per_user[author].setdefault(file_type_label, 0)

                    # Update file type counts
                    file_type_predictions_per_user[author][file_type_label] += 1

        self.print_results(types_per_user, types_of_commits, file_type_predictions_per_user)

    def print_results(self, types_per_user, types_of_commits, file_type_predictions_per_user):
        # Print author-specific counts
        for author, label_counts in types_per_user.items():
            print(f'Author: {author}')
            for label, count in label_counts.items():
                print(f'  {label}: {count}')
            print('  File types:')
            for file_type_label, count in file_type_predictions_per_user[author].items():
                print(f'    {file_type_label}: {count}')
            print()

        # Print total counts for the project
        print('Total label commit message counts for the project:')
        for label, count in types_of_commits.items():
            print(f'  {label}: {count}')

        print('Total label filepath counts for the project:')
        for label, count in file_type_predictions_per_user.items():
            print(f'  {label}: {count}')

        author_summaries = self.generate_author_summaries(types_per_user)
        for summary in author_summaries:
            print(summary)

    def generate_author_summaries(self, types_per_user):
        summaries = []

        for author, label_counts in types_per_user.items():
            # Sort the labels by count, descending
            sorted_labels = sorted(label_counts.items(), key=lambda item: item[1], reverse=True)

            # Build the summary string
            summary_parts = [f"{label}: {count}" for label, count in sorted_labels]
            summary = f"{author} has mainly been working with {summary_parts[0]}"

            # If there are more labels, add them as secondary mentions
            if len(summary_parts) > 1:
                secondary_activities = ", ".join(summary_parts[1:])
                summary += f", but also contributed to {secondary_activities}"

            summaries.append(summary)

        return summaries
