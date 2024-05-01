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
        commit_types_per_user = {}
        commit_types_in_project = {}
        file_types_per_user = {}
        file_types_in_project = {}
        detailed_contributions = {}

        for author, commits in commits_dict.items():
            if author not in commit_types_per_user:
                #print(f"Author: {author}")
                commit_types_per_user[author] = {}
                file_types_per_user[author] = {}
                detailed_contributions[author] = {}

            for commit_message, file_paths in commits:
                #print(f"Commit message: {commit_message}")
                #print(f"File paths: {len(file_paths)}")
                # Classify the commit message
                commit_prediction = self.commit_message_nlp(commit_message)
                commit_type = commit_prediction[0]['label']

                #print(f"Commit type: {commit_type}")

                # Initialize commit label counts
                commit_types_per_user[author].setdefault(commit_type, 0)
                commit_types_in_project.setdefault(commit_type, 0)

                # Update commit label counts
                commit_types_per_user[author][commit_type] += 1
                commit_types_in_project[commit_type] += 1

                if commit_type not in detailed_contributions[author]:
                    detailed_contributions[author][commit_type] = {}

                # Classify each file path modified in this commit
                for file_path in file_paths:
                    #print(f"File path: {file_path}")
                    file_prediction = self.filepath_nlp(file_path)
                    file_type = file_prediction[0]['label']

                    #print(f"File type: {file_type}")

                    # Update commit label counts
                    if file_type not in file_types_per_user[author]:
                        file_types_per_user[author][file_type] = 0
                    file_types_per_user[author][file_type] += 1

                    if file_type not in file_types_in_project:
                        file_types_in_project[file_type] = 0
                    file_types_in_project[file_type] += 1

                    # Update detailed contribution summary
                    if file_type not in detailed_contributions[author][commit_type]:
                        detailed_contributions[author][commit_type][file_type] = 0
                    detailed_contributions[author][commit_type][file_type] += 1
        #print(f'Detailed contribution: {detailed_contributions}')

        #self.print_results(commit_types_per_user, commit_types_in_project, file_types_per_user, file_types_in_project)

        # Generate personal summaries from detailed contributions
        personal_summaries = self.generate_personal_summaries(detailed_contributions)
        project_summaries = self.generate_project_summaries(commit_types_in_project, file_types_in_project)
        self.print_summary(personal_summaries, project_summaries)

    def generate_personal_summaries(self, detailed_contributions):
        personal_summaries = {}

        for author, contributions in detailed_contributions.items():
            summary_parts = []
            for commit_type, file_types in contributions.items():
                # Find the file type with the highest count for each commit type
                if len(file_types) > 0:
                    most_common_file_type, highest_count = max(file_types.items(), key=lambda item: item[1])
                    summary_part = f"{commit_type} in {most_common_file_type} ({highest_count} times)"
                else:
                    summary_part = f"{commit_type} changes"
                summary_parts.append(summary_part)

            # Combine all parts into one summary for each author
            personal_summary = f"{author} has worked mostly on " + "; ".join(summary_parts) + "."
            personal_summaries[author] = personal_summary

        return personal_summaries

    def generate_project_summaries(self, commit_types_in_project, file_types_in_project):
        # Summarize the most common types of commits
        sorted_commits = sorted(commit_types_in_project.items(), key=lambda x: x[1], reverse=True)
        commit_summary = "In this project, the most frequent types of commits have been: "
        commit_summary += ", ".join([f"{ctype} ({count} times)" for ctype, count in sorted_commits])

        # Summarize the most common types of file changes
        sorted_file_types = sorted(file_types_in_project.items(), key=lambda x: x[1], reverse=True)
        file_type_summary = "The types of files most changed have been: "
        file_type_summary += ", ".join([f"{ftype} ({count} times)" for ftype, count in sorted_file_types])

        return commit_summary + ". " + file_type_summary


    def print_summary(self, personal_summaries, project_summary):
        # Print the personal summaries
        for author, summary in personal_summaries.items():
            print(f'Author: {author}')
            print(f'  Summary: {summary}')
            print()

        print(f'Project Summary: \n{project_summary}')

    def print_results(self, commit_types_per_user, commit_types_in_project, file_types_per_user, file_types_in_project):
        # Print author-specific counts
        for author, label_counts in commit_types_per_user.items():
            print(f'Author: {author}')
            for label, count in label_counts.items():
                print(f'  {label}: {count}')
            print('  File types:')
            for file_type_label, count in file_types_per_user[author].items():
                print(f'    {file_type_label}: {count}')
            print()

        # Print total counts for the project
        print('Total label commit message counts for the project:')
        for label, count in commit_types_in_project.items():
            print(f'  {label}: {count}')

        print('Total label filepath counts for the project:')
        for label, count in file_types_in_project.items():
            print(f'  {label}: {count}')

        # author_summaries = self.generate_author_summaries(types_per_user, file_type_predictions_per_user)
        # for summary in author_summaries:
        #     print(summary)

    # def generate_author_summaries(self, types_per_user, file_type_predictions_per_user):
    #     summaries = []
    #
    #     for author, label_counts in types_per_user.items():
    #         # Sort the labels by count, descending
    #         sorted_labels = sorted(label_counts.items(), key=lambda item: item[1], reverse=True)
    #
    #         # Build the summary string for commit types
    #         summary_parts = [f"{label}: {count}" for label, count in sorted_labels]
    #         commit_summary = f"{author} has mainly been working with {summary_parts[0]}"
    #
    #         # If there are more labels, add them as secondary mentions
    #         if len(summary_parts) > 1:
    #             secondary_activities = ", ".join(summary_parts[1:])
    #             commit_summary += f", but also contributed to {secondary_activities}"
    #
    #         # Include file type information
    #         file_types = file_type_predictions_per_user[author]
    #         sorted_file_types = sorted(file_types.items(), key=lambda item: item[1], reverse=True)
    #         file_type_summary = ", ".join([f"{ftype}: {count}" for ftype, count in sorted_file_types])
    #
    #         # Combine commit and file type summaries
    #         summary = f"{commit_summary}. In terms of file types, {author} modified {file_type_summary}"
    #         summaries.append(summary)
    #
    #     return summaries
    # def generate_author_summaries(self, types_per_user):
    #     summaries = []
    #
    #     for author, label_counts in types_per_user.items():
    #         # Sort the labels by count, descending
    #         sorted_labels = sorted(label_counts.items(), key=lambda item: item[1], reverse=True)
    #
    #         # Build the summary string
    #         summary_parts = [f"{label}: {count}" for label, count in sorted_labels]
    #         summary = f"{author} has mainly been working with {summary_parts[0]}"
    #
    #         # If there are more labels, add them as secondary mentions
    #         if len(summary_parts) > 1:
    #             secondary_activities = ", ".join(summary_parts[1:])
    #             summary += f", but also contributed to {secondary_activities}"
    #
    #         summaries.append(summary)
    #
    #     return summaries
