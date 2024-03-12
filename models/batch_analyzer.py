import pickle
import time
import spacy
from gensim.corpora import Dictionary
from gensim.models import LdaModel


class BatchAnalyzer:
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

    def analyze_commits(self, authors_commits):
        types_per_user = {}
        types_of_commits = {}
        start_time = time.time()
        for author, commits in authors_commits.items():

            start_time_preprocessing = time.time()
            preprocessed_commits = self.preprocess_commits(commits)
            end_time_preprocessing = time.time()
            print(f"Preprocess took {end_time_preprocessing - start_time_preprocessing:.2f} seconds for {author}")

            bow_corpus = [self.dictionary.doc2bow(commit) for commit in preprocessed_commits]

            topic_distributions = [self.lda_model.get_document_topics(bow) for bow in bow_corpus]

            start_time_dist = time.time()
            for commit_message, distribution in  zip(commits, topic_distributions):
                dominant_topic = max(distribution, key=lambda x: x[1])[0]

                start_time_cat = time.time()
                category = self.topic_category_mapping[dominant_topic][1]
                end_cat = time.time()

                # Print commit message and its category
                print(f"Commit: \"{commit_message}\" Classified into: \"{category}\"")

                # Update counts for each author
                if author not in types_per_user:
                    types_per_user[author] = {}
                types_per_user[author][category] = types_per_user[author].get(category, 0) + 1

                # Update global counts
                types_of_commits[category] = types_of_commits.get(category, 0) + 1

        # End timer and print the elapsed time
        end_time = time.time()
        print(f"Commit analysis took {end_time - start_time:.2f} seconds.")
        self.summarize_results(types_per_user, types_of_commits)

    def preprocess_commits(self, commit_messages):
        nlp = spacy.load("en_core_web_sm")

        # Define custom stopwords
        custom_stop_words = ["\n\n", "a", "the", "and", "etc", "<", ">", "\n", "=", "zip", "use", "instead", "easy",
                             "\r\n\r\n", " ", "\t", "non", "no", "ensure", "minor", "example", "null", "call", "method",
                             "prepare", "support", "set", "snapshot", "class", "close", "code", "extract", "available",
                             "object", "fix", "type", "follow", "expect", "flag", "src", "main", "master", "sdk"]
        for stop_word in custom_stop_words:
            nlp.vocab[stop_word].is_stop = True

        if nlp.vocab['class'].is_stop:
            print("True")
        else:
            print("False")

        preprocessed_commits = []
        # Process each commit message individually within the batch
        for commit_message in commit_messages:
            # Skip merge commits or handle as desired
            # if "merge pull request" in commit_message.lower() or "merge branch" in commit_message.lower():
            #     preprocessed_commits.append(["merge_commit"])
            #     continue

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

    # def preprocess_commits(self, commit_messages):
    #
    #     # for commit in commit_messages:
    #     #     if "merge pull request" in commit or "merge branch" in commit:
    #     #         # Option 1: Ignore merge commits by returning an empty list.
    #     #         return []
    #     #
    #     #         # Option 2: Mark merge commits distinctly.
    #     #         #return ["merge_commit"]
    #
    #     nlp = spacy.load("en_core_web_sm")
    #
    #     # Add custom stop words
    #     custom_stop_words = ["\n\n", "a", "the", "and", "etc", "<", ">", "\n", "=", "zip", "use", "instead", "easy",
    #                          "\r\n\r\n", " ", "\t", "non", "no", "ensure", "minor", "example"]
    #
    #     for stop_word in custom_stop_words:
    #         nlp.vocab[stop_word].is_stop = True
    #
    #     # Lowercase and filter commit messages before processing
    #     texts = [commit_message.lower() for commit_message in commit_messages]
    #
    #     # Use spaCy's pipe method for efficient batch processing
    #     preprocessed_commits = []
    #     for doc in nlp.pipe(texts, batch_size=20):  # Adjust batch_size based on your system's capabilities
    #         # Filtering out stopwords, punctuation, numbers, and urls. Also lemmatizing.
    #         tokens = [
    #             token.lemma_ for token in doc
    #             if not token.is_stop and not token.is_punct and not token.like_num and not token.like_url
    #         ]
    #         preprocessed_commits.append(tokens)
    #
    #     return preprocessed_commits


        # # Tokenize the commit
        # doc = nlp(commit)
        #
        # # Define custom stopwords.
        # custom_stop_words = ["\n\n", "a", "the", "and", "etc", "<", ">", "\n", "=", "zip", "use", "instead", "easy",
        #                      "\r\n\r\n", " ", "\t", "non", "no", "ensure", "minor", "example"]
        #
        # for stop_word in custom_stop_words:
        #     nlp.Defaults.stop_words.add(stop_word)
        #
        # # Filtering out stopwords, punctuation, numbers, and urls. Also lemmatizing.
        # filtered_tokens = [
        #     token.lemma_ for token in doc if
        #     not token.is_stop and not token.is_punct and not token.like_num and not token.like_url
        # ]
        #
        # return filtered_tokens


    def summarize_results(self, types_per_user, types_of_commits):
        # Format the content string with global commit types and types per user
        content = (f"types_of_commits = {types_of_commits}\n"
                   f"types_per_user = {types_per_user}\n")

        # Specify the file path where you want to append the results
        file_path = 'support/repo_stats.py'

        # Open the file and append the content
        with open(file_path, 'a', encoding="utf-8") as file:
            file.write(content)


