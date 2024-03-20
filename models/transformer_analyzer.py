from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class TransformerAnalyzer:

    def __init__(self):
        model_name = "microsoft/codebert-base"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        num_categories = 3
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=num_categories)

        self.classifier = pipeline("text-classification", model=self.model, tokenizer=self.tokenizer)

    def classify_commits(self, commit_messages):
        """
        Classifies each commit message using the fine-tuned model.
        """
        classifications = self.classifier(commit_messages)
        return classifications

    def generate_summary(self, author, classifications, files_involved):
        """
        Generates a summary for an author based on commit message classifications.
        """
        summary_counts = {category['label']: 0 for category in classifications}
        label_mapping = {0: 'Bug Fix', 1: 'Feature Addition', 27: 'hej'}  # Based on training labels

        for classification in classifications:
            label_index = int(classification['label'].split('_')[-1])  # Extract index from LABEL_X
            classification['label'] = label_mapping.get(label_index, 'Unknown')  # Map index to actual labe

        summary = f"{author} did a lot of "
        summary += ", ".join([f"{count} {label}" for label, count in summary_counts.items() if count > 0])
        summary += f". They worked on files such as: {', '.join(files_involved[:3])}."  # Example: top 3 files
        if len(files_involved) > 3:
            summary += " And more."
        return summary

    def analyze_commits(self, authors_commits_files):
        """
        Analyzes commits by classifying them and generating summaries.
        """
        summaries_per_user = {}

        print(type(authors_commits_files))

        for author, data in authors_commits_files.items():
            commit_messages = [commit_message for commit_message, _ in data]
            classifications = self.classify_commits(commit_messages)
            files_involved = list(set([file for _, files in data for file in files]))
            summary = self.generate_summary(author, classifications, files_involved)
            summaries_per_user[author] = summary

        for author, summary in summaries_per_user.items():
            print(summary)
