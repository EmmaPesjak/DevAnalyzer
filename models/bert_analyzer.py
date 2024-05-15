from pathlib import Path
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification, \
    BertForSequenceClassification, BertTokenizerFast
from itertools import cycle

class BertAnalyzer:

    def __init__(self):
        # commit_message_model_path = Path(__file__).parent.parent / "transformers_model/results/messages/split_11"
        # filepath_model_path = Path(__file__).parent.parent / "transformers_model/results/filepaths/split_14"

        # Load models and tokenizers
        # self.commit_message_model = AutoModelForSequenceClassification.from_pretrained(commit_message_model_path)
        # self.commit_message_tokenizer = AutoTokenizer.from_pretrained(commit_message_model_path)
        self.commit_message_tokenizer = AutoTokenizer.from_pretrained("dev-analyzer/commit-message-model")
        self.commit_message_model = AutoModelForSequenceClassification.from_pretrained(
            "dev-analyzer/commit-message-model")
        self.filepath_model = BertForSequenceClassification.from_pretrained("dev-analyzer/file_path_model")
        self.filepath_tokenizer = BertTokenizerFast.from_pretrained("dev-analyzer/file_path_model")

        # self.filepath_model = BertForSequenceClassification.from_pretrained(filepath_model_path)
        # self.filepath_tokenizer = BertTokenizerFast.from_pretrained(filepath_model_path)

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

        # Initialize commit and file types lists
        self.all_commit_types = list(self.commit_message_model.config.id2label.values())
        self.all_file_types = list(self.filepath_model.config.id2label.values())

    def reset_for_new_repository(self):
        # self.commit_types_per_user = {}
        # self.commit_types_in_project = {}
        # self.file_types_per_user = {}
        # self.file_types_in_project = {}
        # self.detailed_contributions = {}
        # self.detailed_contributions_in_project = {}

        # for commit_type in self.all_commit_types:
        #     self.commit_types_in_project[commit_type] = 0
        #     self.detailed_contributions_in_project[commit_type] = {}
        #     for file_type in self.all_file_types:
        #         self.file_types_in_project[file_type] = 0

        self.commit_types_per_user = {}
        self.commit_types_in_project = {}
        self.file_types_per_user = {}
        self.file_types_in_project = {}
        self.detailed_contributions = {}
        self.detailed_contributions_in_project = {}

        self.commit_types_in_project = {ct: 0 for ct in self.all_commit_types}
        self.file_types_in_project = {ft: 0 for ft in self.all_file_types}
        self.detailed_contributions_in_project = {
            ct: {ft: 0 for ft in self.all_file_types} for ct in self.all_commit_types
        }

    def analyze_commits(self, commits_dict):
        self.reset_for_new_repository()  # Reset counts before processing new data
        print(f"Commits_dict: {commits_dict}")

        for author, commits in commits_dict.items():
            print(f"Author: {author}, commits: {commits}")
            if author not in self.commit_types_per_user:

                # Prepopulate with zero counts for all commit types
                self.commit_types_per_user[author] = {ct: 0 for ct in self.all_commit_types}
                # Prepopulate with zero counts for all file types
                self.file_types_per_user[author] = {ft: 0 for ft in self.all_file_types}
                # Prepare detailed contributions with nested dictionaries
                self.detailed_contributions[author] = {ct: {ft: 0 for ft in self.all_file_types} for ct in
                                                       self.all_commit_types}

            for commit_message, file_paths in commits:
                # Classify the commit message
                commit_prediction = self.commit_message_nlp(commit_message)
                commit_type = commit_prediction[0]['label']

                # Update commit label counts
                self.commit_types_per_user[author][commit_type] += 1
                self.commit_types_in_project[commit_type] += 1

                # Classify each file path modified in this commit
                for file_path in file_paths:
                    file_prediction = self.filepath_nlp(file_path)
                    file_type = file_prediction[0]['label']

                    # Update commit label counts
                    self.file_types_per_user[author][file_type] += 1
                    self.file_types_in_project[file_type] += 1
                    self.detailed_contributions_in_project[commit_type][file_type] += 1

                    # # Update detailed contribution summary
                    self.detailed_contributions[author][commit_type][file_type] += 1
        print(f'Detailed contribution for authors: {self.detailed_contributions}')
        print(f'Detailed contribution for project: {self.detailed_contributions_in_project}')

        # Generate personal summaries from detailed contributions
        self.personal_summaries = self.generate_personal_summaries(self.commit_types_per_user, self.detailed_contributions)
        self.project_summaries = self.generate_project_summaries(self.commit_types_in_project, self.detailed_contributions_in_project)
        #self.print_summary(self.personal_summaries, self.project_summaries)

    def prepare_summary_matrix(self, commit_types, file_types, detailed_contributions):
        # Initialize the matrix with zeros
        summary_matrix = {ctype: {ftype: 0 for ftype in file_types} for ctype in commit_types}

        # Fill the matrix with actual counts
        for author, contributions in detailed_contributions.items():
            # print(f'{author}: {contributions}')
            #print(f'Contribution items: {contributions.items()}')
            for commit_type, file_stats in contributions.items():
                # print(f'\t{commit_type}, file stats: {file_stats}')
                for file_type, count in file_stats.items():
                    # print(f'\t\t{file_type}, count: {count}')
                    if commit_type in summary_matrix and file_type in summary_matrix[commit_type]:
                        summary_matrix[commit_type][file_type] += count
                        # print(f'summary matrix: {summary_matrix}')

        return summary_matrix

    def generate_personal_summaries(self, commit_types_per_user, detailed_contributions):

        personal_summaries = {}

        for author, contributions in detailed_contributions.items():
            summary_parts = []
            # Sort the commit types by frequency for this user
            sorted_contributions = sorted(commit_types_per_user[author].items(), key=lambda x: x[1], reverse=True)
            zero_commit_types = []
            first = True  # Flag for the first item
            second = True  # Flag for the second item

            # Create an iterator to cycle through synonyms
            emphasis_words = cycle(["primarily", "mostly", "mainly"])

            # Determine the number of non-zero commit types for formatting
            num_non_zero = sum(1 for _, count in sorted_contributions if count > 0)
            count_non_zero = 0

            for ctype, count in sorted_contributions:
                commit_word = "commit" if count == 1 else "commits"
                commit_has_have = "has" if count == 1 else "have"
                commit_these_this = "This" if count == 1 else "These"

                if count == 0:
                    zero_commit_types.append(ctype.lower())  # Collect zero commit types
                    continue
                else:
                    count_non_zero += 1  # Increment the counter of non-zero types

                    # Get the file type with the highest count for this commit type from detailed_contributions
                    file_changes = contributions[ctype]
                    most_common_file, most_common_count = max(file_changes.items(),
                                                              key=lambda item: item[1]) if file_changes else ("", 0)

                    next_emphasis_word = next(emphasis_words)  # Get the next word from the cycle

                    # Determine the conjunction for formatting
                    conjunction = "and" if count_non_zero == num_non_zero else ""
                    end_of_sentence = "." if conjunction == "and" else ""

                    if first:
                        # Special formatting for the most common commit type
                        summary_part = f"{author.capitalize()} has mostly done {ctype.lower()} commits, with {count} {commit_word}."
                        if most_common_count > 0:
                            summary_part += f" {commit_these_this} {commit_has_have} {next_emphasis_word} been done in {most_common_file.lower()} files."
                        else:
                            summary_part += " However, in 0 files."
                        first = False

                    else:
                        if second:
                            # Formatting for other commit types
                            if most_common_count > 0:
                                summary_part = f" Then, {count} {ctype.lower()} {commit_word} {commit_has_have} {next_emphasis_word} been done in {most_common_file.lower()} files{end_of_sentence}"
                            else:
                                summary_part = f" Then, there {commit_has_have} been {count} {ctype.lower()} {commit_word} in 0 files{end_of_sentence}"
                            second = False
                        else:
                            if most_common_count > 0:
                                summary_part = f", {conjunction} {count} {ctype.lower()} {commit_word} {commit_has_have} {next_emphasis_word} been done in {most_common_file.lower()} files{end_of_sentence}{end_of_sentence}"
                            else:
                                summary_part = f", {conjunction} {count} {ctype.lower()} {commit_word}, but in 0 files{end_of_sentence}{end_of_sentence}"
                summary_parts.append(summary_part)

            if zero_commit_types:
                if summary_parts[-1][-1] != '.':
                    summary_parts[-1] += '.'
                zero_commits_sentence = f" However, {author.capitalize()} has not done any {', '.join(zero_commit_types)} commits"
                summary_parts.append(zero_commits_sentence)

            # Ensure the entire summary ends with a period
            if not summary_parts[-1].endswith('.'):
                summary_parts[-1] += "."
            personal_summaries[author] = "".join(summary_parts)

        return personal_summaries

    def generate_project_summaries(self, commit_types_in_project, detailed_contributions_in_project):
        # Summarize the most common types of commits
        sorted_commits = sorted(commit_types_in_project.items(), key=lambda x: x[1], reverse=True)
        summary_parts = []
        zero_commit_types = []
        first = True  # Flag to check if it's the first item
        second = True

        # Create an iterator to cycle through synonyms
        emphasis_words = cycle(["primarily", "mostly", "mainly"])

        # Determine the number of non-zero commit types for formatting
        num_non_zero = sum(1 for _, count in sorted_commits if count > 0)
        count_non_zero = 0

        for ctype, count in sorted_commits:
            commit_word = "commit" if count == 1 else "commits"
            commit_has_have = "has" if count == 1 else "have"
            commit_these_this = "This" if count == 1 else "These"

            if count == 0:
                zero_commit_types.append(ctype.lower())  # Add to zero count list
                continue  # Skip further processing for zero count types
            else:
                count_non_zero += 1  # Increment the counter of non-zero types
                # Get the file type with the highest count for this commit type
                file_changes = detailed_contributions_in_project[ctype]
                most_common_file, most_common_count = max(file_changes.items(),
                                                          key=lambda item: item[1]) if file_changes else ("", 0)
                next_emphasis_word = next(emphasis_words)  # Get the next word from the cycle

                # Determine the conjunction for formatting
                conjunction = "and" if count_non_zero == num_non_zero else ""
                end_of_sentence = "." if conjunction == "and" else ""

                if first:
                    # Special formatting for the most common commit type
                    summary_part = f"In this project, {ctype.lower()} {commit_word} have been the most frequent, with {count} commits."
                    if most_common_count > 0:
                        summary_part += f" {commit_these_this} {commit_has_have} {next_emphasis_word} been done in {most_common_file.lower()} files."
                    else:
                        summary_part += " However, in 0 files."
                    first = False
                else:
                    if second:
                        # Formatting for other commit types
                        if most_common_count > 0:
                            summary_part = f" Then, {count} {ctype.lower()} {commit_word} {commit_has_have} {next_emphasis_word} been done in {most_common_file.lower()} files{end_of_sentence}"
                        else:
                            summary_part = f" Then, there {commit_has_have} been {count} {ctype.lower()} {commit_word} in 0 files{end_of_sentence}"
                        second = False
                    else:
                        if most_common_count > 0:
                            summary_part = f", {conjunction} {count} {ctype.lower()} {commit_word} {commit_has_have} {next_emphasis_word} been done in {most_common_file.lower()} files{end_of_sentence}"
                        else:
                            summary_part = f", {conjunction} {count} {ctype.lower()} {commit_word}, but in 0 files{end_of_sentence}"

            summary_parts.append(summary_part)

        if zero_commit_types:
            if summary_parts[-1][-1] != '.':
                summary_parts[-1] += '.'
            # Format the zero count types into a readable string
            zero_commits_sentence = f" However, no {', '.join(zero_commit_types)} commits have been done in this project"
            summary_parts.append(zero_commits_sentence)

        #summary_parts.append(f".")

        return "".join(summary_parts)

    def get_matrix(self):
        return self.prepare_summary_matrix(self.commit_types_in_project.keys(), self.file_types_in_project.keys(), self.detailed_contributions)

    def get_detailed_contributions(self):
        return self.detailed_contributions
    def get_total_what_per_user(self):
        """
        Returns a dictionary mapping each author to their total counts of each commit type.
        """
        return self.commit_types_per_user

    def get_total_where_per_user(self):
        return self.file_types_per_user

    def get_total_what(self):
        return self.commit_types_in_project

    def get_total_where(self):
        return self.file_types_in_project

    def get_personal_summary(self):
        return self.personal_summaries

    def get_overall_summary(self):
        return self.project_summaries

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

