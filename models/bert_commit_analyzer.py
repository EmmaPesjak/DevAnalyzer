from collections import defaultdict

from transformers import BertTokenizerFast, BertForSequenceClassification, pipeline
import torch
from pathlib import Path

class BertCommitAnalyzer:

    def __init__(self):
        model_path = Path(__file__).parent.parent / "transformers_model/results/trained_model"

        self.model = BertForSequenceClassification.from_pretrained(model_path)
        self.tokenizer = BertTokenizerFast.from_pretrained(model_path)
        self.nlp = pipeline("sentiment-analysis", model=self.model, tokenizer=self.tokenizer)

    def analyze_commits(self, commits_dict):
        types_per_user = {}
        types_of_commits = {}

        print("Innan")

        for author, commits in commits_dict.items():
            for commit_message in commits:
                prediction = self.nlp(commit_message)
                predicted_label = prediction[0]['label']
                print(f'Predicted label: {predicted_label}, msg: \"{commit_message}\"')

                # Update counts for each author
                if author not in types_per_user:
                    types_per_user[author] = {}

                # Initialize count for this label for the author if not present
                if predicted_label not in types_per_user[author]:
                    types_per_user[author][predicted_label] = 0

                # Initialize count for this label in total counts if not present
                if predicted_label not in types_of_commits:
                    types_of_commits[predicted_label] = 0

                # Update counts for the author
                types_per_user[author][predicted_label] += 1

                # Update total counts for the project
                types_of_commits[predicted_label] += 1

            self.print_results(types_per_user, types_of_commits)

    def print_results(self, types_per_user, types_of_commits):
        # Print author-specific counts
        for author, label_counts in types_per_user.items():
            print(f'Author: {author}')
            for label, count in label_counts.items():
                print(f'  {label}: {count}')
            print()

        # Print total counts for the project
        print('Total label counts for the project:')
        for label, count in types_of_commits.items():
            print(f'  {label}: {count}')


        # for message in messages:
        #     prediction = self.nlp(message)
        #     predicted_label = prediction[0]['label']
        #     print(f'Commit message: \"{message}\", \nPrediction: {predicted_label}\n')