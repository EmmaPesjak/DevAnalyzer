from pathlib import Path
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class BertAnalyzer:

    def __init__(self):
        commit_message_model_path = Path(__file__).parent.parent / "transformers_model/results/messages/split_14"
        self.commit_message_model = AutoModelForSequenceClassification.from_pretrained(commit_message_model_path)
        self.commit_message_tokenizer = AutoTokenizer.from_pretrained(commit_message_model_path)
        self.commit_message_nlp = pipeline("text-classification", model=self.commit_message_model, tokenizer=self.commit_message_tokenizer)

        filepath_model_path = Path(__file__).parent.parent / "transformers_model/results/filepaths/split_14"
        self.filepath_model = BertForSequenceClassification.from_pretrained(filepath_model_path)
        self.filepath_tokenizer = BertTokenizerFast.from_pretrained(filepath_model_path)
        self.filepath_nlp = pipeline("text-classification", model=self.filepath_model, tokenizer=self.filepath_tokenizer)


    def analyze_commits(self, commits_dict):
        types_per_user = {}
        types_of_commits = {}

        for author, commits in commits_dict.items():
            for commit_message in commits:
                prediction = self.commit_message_nlp(commit_message)
                predicted_label = prediction[0]['label']
                #print(f'Predicted label: {predicted_label}, msg: \"{commit_message}\"')

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

    def print_results(self, types_per_user, types_of_commits):

        # TODO include the files in the summary
        # # Convert to descriptive text
        # descriptive_texts = self.counts_to_descriptive_text(types_per_user)
        #
        # # Generate summaries
        # author_summaries = self.summarize_texts(descriptive_texts)

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

        author_summaries = self.generate_author_summaries(types_per_user)
        for summary in author_summaries:
            print(summary)

        # for author, summary in author_summaries.items():
        #     print(f"{author}: {summary}")
