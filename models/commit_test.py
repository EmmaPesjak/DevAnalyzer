import pickle

import spacy
from gensim.models.ldamodel import LdaModel
from gensim.corpora.dictionary import Dictionary

class CommitTest:
    def __init__(self):
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


    def analyze_commits(self, commit_messages):
        for commit in commit_messages:
            #print("Commit: " + commit)
            self.categorize_commit_message(commit)
        # # Preprocess commit messages
        # preprocessed_commits = self.preprocess_commit(commit_messages)
        #
        # # Vectorize messages
        # corpus = [self.dictionary.doc2bow(commit) for commit in preprocessed_commits]
        #
        # # Analyze and categorize each commit
        # commit_categories = []
        # for commit in corpus:
        #     topics = self.lda_model[commit]
        #     category = self.map_topics_to_category(topics)
        #     commit_categories.append(category)

        #return commit_categories

    def categorize_commit_message(self, commit_message):
        # Preprocess the commit message
        preprocessed_message = self.preprocess_commit(commit_message)  # Ensure this is a list
        #print("Preprocessed: " + str(preprocessed_message))
        # Vectorize the commit message
        bow_vector = self.dictionary.doc2bow(preprocessed_message)  # Convert to BoW format

        # Infer the topic(s) for the commit message
        #topic_distribution = self.lda_model[bow_vector]
        # Infer the topic(s) for the commit message
        topic_distribution = self.lda_model.get_document_topics(bow_vector)
        #print("Topics: " + str(topic_distribution))

        # Find the dominant topic
        dominant_topic = max(topic_distribution, key=lambda x: x[1])[0]
        #print("Dominant topic: " + str(dominant_topic))

        # Map the dominant topic to a category
        category = self.topic_category_mapping[dominant_topic]

        # Print the result
        #print(f"Commit Message: \"{commit_message}\"")
        #print(f"Predicted Category: {category}")
        #print('-----------------------')

    def preprocess_commit(self, commit_message):
        nlp = spacy.load("en_core_web_sm")
        # Lowercase the commit message.
        commit_message = commit_message.lower()

        # Check for merge commits and handle them as desired.
        if "merge pull request" in commit_message or "merge branch" in commit_message:
            # Option 1: Ignore merge commits by returning an empty list.
            #return []

            # Option 2: Mark merge commits distinctly.
            return ["merge_commit"]

        # Tokenize the commit
        doc = nlp(commit_message)

        # Define custom stopwords.
        custom_stop_words = ["\n\n", "a", "the", "and", "etc", "<", ">", "\n", "=", "zip", "use", "instead", "easy",
                             "\r\n\r\n", " ", "\t", "non", "no", "ensure", "minor", "example"]
        for stop_word in custom_stop_words:
            nlp.Defaults.stop_words.add(stop_word)

        # Filtering out stopwords, punctuation, numbers, and urls. Also lemmatizing.
        filtered_tokens = [
            token.lemma_ for token in doc if
            not token.is_stop and not token.is_punct and not token.like_num and not token.like_url
        ]

        return filtered_tokens

    # def map_topics_to_category(self, topics):
    #     # Map topics to categories using self.topic_category_mappings
    #     # This is a simplified example. You'll need to adapt it based on your mapping logic.
    #     category = max(topics, key=lambda x: self.topic_category_mappings.get(x[0], 'Other'))
    #     return category

