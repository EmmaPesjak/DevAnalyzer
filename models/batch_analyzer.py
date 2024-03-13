import pickle
import spacy
from gensim.corpora import Dictionary
from gensim.models import LdaModel


class BatchAnalyzer:
    """
    Class to analyze batch data of commit messages.
    """
    def __init__(self):
        """
        Initialize the BatchAnalyzer class.
        """

        # Load the trained LDA model
        self.lda_model = LdaModel.load('TopicModeling/lda_model.gensim')

        # Load the dictionary
        self.dictionary = Dictionary.load('TopicModeling/dictionary.gensim')

        # Load the topic-to-category mappings
        with open('TopicModeling/topic_to_category_mapping.pkl', 'rb') as f:
            self.topic_category_mapping = pickle.load(f)

        # Load the categories
        with open('TopicModeling/categories.pkl', 'rb') as f:
            self.categories = pickle.load(f)

    def analyze_commits(self, authors_commits):
        """
        Analyze the commits by preprocessing the commits, creating a bag-of-words, and using the
        lda-model to find the best-matching categories.
        :param authors_commits: commit-messages.
        :return:
        """

        types_per_user = {}
        types_of_commits = {}

        # Loop through each commit message related to the author.
        for author, commits in authors_commits.items():

            # Pre-process all commits.
            preprocessed_commits = self.preprocess_commits(commits)

            # Create a bag of words, using the dictionary.
            bow_corpus = [self.dictionary.doc2bow(commit) for commit in preprocessed_commits]

            # Find the topic distributions from the lda-model.
            topic_distributions = [self.lda_model.get_document_topics(bow) for bow in bow_corpus]

            # For each topic distribution, find the dominant topic and map it to a category.
            for distribution in topic_distributions:
                dominant_topic = max(distribution, key=lambda x: x[1])[0]

                category = self.topic_category_mapping[dominant_topic][1]

                # Update counts for each author
                if author not in types_per_user:
                    types_per_user[author] = {}
                types_per_user[author][category] = types_per_user[author].get(category, 0) + 1

                # Update global counts
                types_of_commits[category] = types_of_commits.get(category, 0) + 1

        # Summarize the results.
        self.summarize_results(types_per_user, types_of_commits)

    @staticmethod
    def preprocess_commits(commit_messages):
        """
        Preprocesses the commit messages by applying stop words, lemmatizing, and filter out only
        alphabetic characters.
        :param commit_messages: Commit messages.
        :return: Preprocessed commit messages
        """
        nlp = spacy.load("en_core_web_sm")

        # Define custom stopwords
        custom_stop_words = ["\n\n", "a", "the", "and", "etc", "<", ">", "\n", "=", "zip", "use", "instead", "easy",
                             "\r\n\r\n", " ", "\t", "non", "no", "ensure", "minor", "example", "null", "call", "method",
                             "prepare", "support", "set", "snapshot", "class", "close", "code", "extract", "available",
                             "object", "fix", "type", "follow", "expect", "flag", "src", "main", "master", "sdk"]

        for stop_word in custom_stop_words:
            nlp.vocab[stop_word].is_stop = True

        preprocessed_commits = []

        # Process each commit message individually within the batch
        for commit_message in commit_messages:
            # Tokenize and preprocess each commit message
            doc = nlp(commit_message.lower())
            tokens = [token.lemma_ for token in doc if
                      not token.is_stop and
                      not token.is_punct and
                      not token.like_num and
                      not token.like_url
                      and token.is_alpha  # Ensure token is fully alphabetic
                      ]
            preprocessed_commits.append(tokens)

        return preprocessed_commits

    @staticmethod
    def summarize_results(types_per_user, types_of_commits):
        """
        Summarize the results and write to file.
        :param types_per_user: Type of commits per user.
        :param types_of_commits: Type of commits for entire project.
        :return:
        """

        # Format the content string with global commit types and types per user
        content = (f"types_of_commits = {types_of_commits}\n"
                   f"types_per_user = {types_per_user}\n")

        file_path = 'support/repo_stats.py'

        # Open the file and append the content
        with open(file_path, 'a', encoding="utf-8") as file:
            file.write(content)
