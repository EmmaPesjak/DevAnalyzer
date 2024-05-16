import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification, \
    BertForSequenceClassification, BertTokenizerFast
from itertools import cycle


def generate_personal_summaries(commit_types_per_user, detailed_contributions):
    """
    Generates summary for each author.
    :param commit_types_per_user: A dictionary containing commit types per user.
    :param detailed_contributions: A dictionary containing detailed contributions for each author for project.
    :return: Dictionary containing a personal summary for each author
    """
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
                zero_commit_types.append(ctype)  # Collect zero commit types
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
                    summary_part = f"{author} has mostly done {ctype} commits, with {count} {commit_word}."
                    if most_common_count > 0:
                        summary_part += f" {commit_these_this} {commit_has_have} {next_emphasis_word} been done " \
                                        f"in {most_common_file} files."
                    else:
                        summary_part += " However, in 0 files."
                    first = False

                else:
                    if second:
                        # Formatting for other commit types
                        if most_common_count > 0:
                            summary_part = f" Then, {count} {ctype} {commit_word} {commit_has_have} " \
                                           f"{next_emphasis_word} been done in {most_common_file} " \
                                           f"files{end_of_sentence}"
                        else:
                            summary_part = f" Then, there {commit_has_have} been {count} {ctype} {commit_word} " \
                                           f"in 0 files{end_of_sentence}"
                        second = False
                    else:
                        if most_common_count > 0:
                            summary_part = f", {conjunction} {count} {ctype} {commit_word} {commit_has_have} " \
                                           f"{next_emphasis_word} been done in {most_common_file} " \
                                           f"files{end_of_sentence}"
                        else:
                            summary_part = f", {conjunction} {count} {ctype} {commit_word}, but in 0 files" \
                                           f"{end_of_sentence}{end_of_sentence}"
            summary_parts.append(summary_part)

        # Include zero commit types.
        if zero_commit_types:
            if summary_parts[-1][-1] != '.':
                summary_parts[-1] += '.'
            zero_commits_sentence = f" However, {author} has not done any {', '.join(zero_commit_types)} commits"
            summary_parts.append(zero_commits_sentence)

        # Ensure the entire summary ends with a period
        if not summary_parts[-1].endswith('.'):
            summary_parts[-1] += "."
        personal_summaries[author] = "".join(summary_parts)

    return personal_summaries


def generate_project_summaries(commit_types_in_project, detailed_contributions_in_project):
    """
    Generates an overall summary for the project.
    :param commit_types_in_project: A dictionary containing the commit types with their respective counters.
    :param detailed_contributions_in_project: A dictionary containing contributions for project.
    :return: A summary of project.
    """
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
            zero_commit_types.append(ctype)  # Add to zero count list
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
                summary_part = f"In this project, {ctype} {commit_word} have been the most frequent, with " \
                               f"{count} commits."
                if most_common_count > 0:
                    summary_part += f" {commit_these_this} {commit_has_have} {next_emphasis_word} been done " \
                                    f"in {most_common_file} files."
                else:
                    summary_part += " However, in 0 files."
                first = False
            else:
                if second:
                    # Formatting for other commit types
                    if most_common_count > 0:
                        summary_part = f" Then, {count} {ctype} {commit_word} {commit_has_have} " \
                                       f"{next_emphasis_word} been done in {most_common_file} " \
                                       f"files{end_of_sentence}"
                    else:
                        summary_part = f" Then, there {commit_has_have} been {count} {ctype} {commit_word} in " \
                                       f"0 files{end_of_sentence}"
                    second = False
                else:
                    if most_common_count > 0:
                        summary_part = f", {conjunction} {count} {ctype} {commit_word} {commit_has_have} " \
                                       f"{next_emphasis_word} been done in {most_common_file} files{end_of_sentence}"
                    else:
                        summary_part = f", {conjunction} {count} {ctype} {commit_word}, but in 0 files{end_of_sentence}"

        summary_parts.append(summary_part)

    if zero_commit_types:
        if summary_parts[-1][-1] != '.':
            summary_parts[-1] += '.'
        # Format the zero count types into a readable string
        zero_commits_sentence = f" However, no {', '.join(zero_commit_types)} commits have been done in this project"
        summary_parts.append(zero_commits_sentence)

    return "".join(summary_parts)


class BertAnalyzer:
    """
    Class to analyze commits with BERT models.
    """

    def __init__(self):
        """
        Initialize the BertAnalyzer with data structures, pre-trained models and configurations.
        """
        self.project_summaries = None
        self.personal_summaries = None
        self.detailed_contributions_in_project = None
        self.file_types_in_project = None
        self.commit_types_in_project = None
        self.detailed_contributions = None
        self.file_types_per_user = None
        self.commit_types_per_user = None
        self.commit_message_tokenizer = AutoTokenizer.from_pretrained("dev-analyzer/commit-message-model")
        self.commit_message_model = AutoModelForSequenceClassification.from_pretrained(
            "dev-analyzer/commit-message-model")
        self.filepath_model = BertForSequenceClassification.from_pretrained("dev-analyzer/file_path_model")
        self.filepath_tokenizer = BertTokenizerFast.from_pretrained("dev-analyzer/file_path_model")

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
        """
        Reset all analytical metrics for analyzing a new repository.
        """
        self.commit_types_per_user = {}
        self.commit_types_in_project = {}
        self.file_types_per_user = {}
        self.file_types_in_project = {}
        self.detailed_contributions = {}
        self.detailed_contributions_in_project = {}

        # Populate dictionaries with predefined labels.
        self.commit_types_in_project = {ct: 0 for ct in self.all_commit_types}
        self.file_types_in_project = {ft: 0 for ft in self.all_file_types}
        self.detailed_contributions_in_project = {
            ct: {ft: 0 for ft in self.all_file_types} for ct in self.all_commit_types
        }

    def analyze_commits(self, commits_dict):
        """
        Analyze commits from a given dictionary of commits.

        Args:
            commits_dict (Dict[str, List[Tuple[str, List[str]]]]): A dictionary where the key is the author and
            the value is a list of tuples containing commit messages and lists of file paths.
        """
        self.reset_for_new_repository()  # Ensure a clean state before starting analysis.

        for author, commits in commits_dict.items():
            if author not in self.commit_types_per_user:
                # Repopulate with zero counts for all commit types
                self.commit_types_per_user[author] = {ct: 0 for ct in self.all_commit_types}
                # Repopulate with zero counts for all file types
                self.file_types_per_user[author] = {ft: 0 for ft in self.all_file_types}
                # Prepare detailed contributions with nested dictionaries
                self.detailed_contributions[author] = {ct: {ft: 0 for ft in self.all_file_types} for ct in
                                                       self.all_commit_types}

            for commit_message, file_paths in commits:
                # Truncate and tokenize the commit message before classification
                # commit_inputs = self.commit_message_tokenizer(commit_message, return_tensors="pt", truncation=True,
                #                                        max_length=128)
                #
                # # Classify the commit message using the model
                # with torch.no_grad():  # Ensure no gradients are computed during inference
                #     commit_prediction = self.commit_message_model(**commit_inputs)
                #     predicted_label_index = commit_prediction.logits.argmax(-1).item()
                #     commit_type = self.commit_message_model.config.id2label[predicted_label_index]
                commit_prediction = self.commit_message_nlp(commit_message, truncation=True, max_length=128)
                commit_type = commit_prediction[0]['label']

                # Update commit label counts
                self.commit_types_per_user[author][commit_type] += 1
                self.commit_types_in_project[commit_type] += 1

                # Classify each file path modified in this commit
                for file_path in file_paths:
                    # Truncate and tokenize the file path before classification
                    # file_inputs = self.filepath_tokenizer(file_path, return_tensors="pt", truncation=True,
                    #                                        max_length=128)
                    #
                    # # Classify the commit message using the model
                    # with torch.no_grad():  # Ensure no gradients are computed during inference
                    #     file_prediction = self.filepath_model(**file_inputs)
                    #     predicted_label_index = file_prediction.logits.argmax(-1).item()
                    #     file_type = self.filepath_model.config.id2label[predicted_label_index]

                    file_prediction = self.filepath_nlp(file_path, truncation=True, max_length=128)
                    file_type = file_prediction[0]['label']

                    # Update commit label counts
                    self.file_types_per_user[author][file_type] += 1
                    self.file_types_in_project[file_type] += 1
                    self.detailed_contributions_in_project[commit_type][file_type] += 1

                    # Update detailed contribution summary
                    self.detailed_contributions[author][commit_type][file_type] += 1

        # Generate personal summaries from detailed contributions
        self.personal_summaries = generate_personal_summaries(self.commit_types_per_user,
                                                              self.detailed_contributions)
        self.project_summaries = generate_project_summaries(self.commit_types_in_project,
                                                            self.detailed_contributions_in_project)

    def get_total_what_per_user(self):
        """
        Returns a dictionary mapping each author to their total counts of each commit type.
        """
        return self.commit_types_per_user

    def get_total_where_per_user(self):
        """
        Returns a dictionary mapping each author to their total counts of changed files.
        """
        return self.file_types_per_user

    def get_total_what(self):
        """
        Returns a dictionary mapping for total commit types in project.
        """
        return self.commit_types_in_project

    def get_total_where(self):
        """
        Returns a dictionary mapping for total changed file-types in project.
        """
        return self.file_types_in_project

    def get_personal_summary(self):
        """
        Returns a dictionary of summaries for each author.
        """
        return self.personal_summaries

    def get_overall_summary(self):
        """
        Returns the project summary.
        """
        return self.project_summaries
