import pickle
import time

import spacy
from gensim.models.ldamodel import LdaModel
from gensim.corpora.dictionary import Dictionary

# TODO: vad händer med alla merge kommits?

# TODO: namnet på denna låter som att vi testar något, borde inte denna heta commitAnalyzer?
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

        self.categories_counts = {}

        self.types_per_user = {}
        self.types_of_commits = {}

    # def analyze_commits(self, commit_messages):
    #     for commit in commit_messages:
    #         #print("Commit: " + commit)
    #         self.categorize_commit_message(commit)
    #
    #     self.summarize_results()

    def analyze_commits(self, authors_commits):
        # Start timer
        start_time = time.time()

        for author, commits in authors_commits.items():
            if author not in self.types_per_user:
                self.types_per_user[author] = {}

            for commit in commits:
                category_name = self.categorize_commit_message(commit)

                # Update per user
                self.types_per_user[author][category_name] = self.types_per_user[author].get(category_name, 0) + 1

                # Update global
                self.types_of_commits[category_name] = self.types_of_commits.get(category_name, 0) + 1
        # End timer and print the elapsed time
        end_time = time.time()
        print(f"Commit analysis took {end_time - start_time:.2f} seconds.")

        self.summarize_results()
        

    def categorize_commit_message(self, commit_message):
        # Preprocess the commit message
        preprocessed_message = self.preprocess_commit(commit_message)
        #print("Preprocessed: " + str(preprocessed_message))
        # Vectorize the commit message
        bow_vector = self.dictionary.doc2bow(preprocessed_message)  # Convert to BoW format

        #topic_distribution = self.lda_model[bow_vector]
        # Infer the topic(s) for the commit message
        topic_distribution = self.lda_model.get_document_topics(bow_vector)
        #print("Topics: " + str(topic_distribution))

        # Find the dominant topic
        dominant_topic = max(topic_distribution, key=lambda x: x[1])[0]
        #print("Dominant topic: " + str(dominant_topic))

        # # Map the dominant topic to a category
        # category = self.topic_category_mapping[dominant_topic]
        # # Increment the count for the determined category
        # #self.category_counts[category] += 1
        #
        # # After determining the category, update the counts
        # # Assuming topic_category_mapping is a mapping from topic numbers to categories
        # category_info = self.topic_category_mapping[dominant_topic]  # This retrieves the category info tuple
        # category_name = category_info[1]  # Assuming the second element is the category name
        #
        # # Aggregate counts by category name
        # self.category_counts[category_name] += 1

        category_name = self.topic_category_mapping[dominant_topic][1]

        # Update the counts in the dictionary
        if category_name in self.categories_counts:
            self.categories_counts[category_name] += 1
        else:
            self.categories_counts[category_name] = 1

        return category_name

        # Print the result
        #print(f"Commit Message: \"{commit_message}\"")
        #print(f"Predicted Category: {category}")
        #print('-----------------------')

    def preprocess_commit(self, commit_message):
        nlp = spacy.load("en_core_web_sm")
        # Lowercase the commit message.
        commit_message = commit_message.lower()

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

    def summarize_results(self):
        # Format the content string with global commit types and types per user
        content = (f"types_of_commits = {self.types_of_commits}\n"
                   f"types_per_user = {self.types_per_user}\n")

        # Specify the file path where you want to append the results
        file_path = 'support/repo_stats.py'

        # Open the file and append the content
        with open(file_path, 'a', encoding="utf-8") as file:
            file.write(content)

        # types_per_user = {'Emma Pesjak': {'REFACTORING': 27, 'FEATURE_ADDITIONS': 7, 'UPDATE': 7, 'DATABASE': 6, 'SETUP': 6}, 'EmmaPesjak': {'REFACTORING': 1}, 'ebbanimer': {'REFACTORING': 22, 'FEATURE_ADDITIONS': 21, 'UPDATE': 10, 'DATABASE': 10, 'SETUP': 9}}
        #
        # content = (f"type_of_commits = {self.categories_counts}\n"
        #            f"types_per_user = {types_per_user}\n")
        #
        # # Append the string to the file
        # with open('support/repo_stats.py', 'a', encoding="utf-8") as file:
        #     file.write(content)
        # print(f"Global Commit Types: {self.types_of_commits}")
        # print("Commit Types Per User:")
        # for user, categories in self.types_per_user.items():
        #     print(f"{user}: {categories}")


        # for category, count in self.category_counts.items():
        #     print(f"{category}: {count}")

    # def map_topics_to_category(self, topics):
    #     # Map topics to categories using self.topic_category_mappings
    #     # This is a simplified example. You'll need to adapt it based on your mapping logic.
    #     category = max(topics, key=lambda x: self.topic_category_mappings.get(x[0], 'Other'))
    #     return category

