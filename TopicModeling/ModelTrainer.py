import shutil
import sys
import spacy
from gensim import corpora
from gensim.models.ldamodel import LdaModel
import pickle
from pydriller import Repository
import os
from gensim.models.coherencemodel import CoherenceModel
import pyLDAvis.gensim

# Check if the support directory exists, if not, create it
if not os.path.exists('support'):
    os.makedirs('support')

class ModelTrainer:
    """
    Class to train the LDA model.
    """

    def __init__(self, commits):
        """
        Initialize the Model Trainer.
        :param commits: Commits to be trained on.
        """

        # Initialize predefined categories.
        self.categories = {
            'ERROR/BUG_HANDLING': ['error', 'bug', 'issue', 'correct', 'resolve', 'patch', 'conflict', 'debug',
                                   'exception', 'fault', 'glitch', 'incorrect', 'crash', 'failure', 'incomplete', 'diagnose',
                                   'troubleshoot', 'nullpointer', 'regression', 'deprecation', "warning"],
            'FEATURE_ADDITIONS': ['add', 'feature', 'implement', 'implementation', 'new', 'introduce', 'create',
                                  'generate', 'method', 'functionality'],
            'DOCUMENTATION': ['doc','docs', 'readme', 'comment', 'tutorial', 'documentation', 'wiki', 'javadoc', 'description',
                              'javadocs', 'readme.md', 'guide', 'manual', 'faq', 'help', 'specification', 'specs',
                              'commentary', 'instruction', 'file'],
            'REFACTORING': ['refactor', 'refactore', 'redundant', 'refactoring', 'clean', 'improve', 'restructure', 'move', 'replace',
                            'typo', 'change', 'rename', 'refine', 'simplify', 'streamline', 'unused', 'revert', 'undo',
                            'rollback', 'reverse', 'discard'],
            'TESTING': ['test', 'unittest', 'integrationtest', 'testing', 'tdd', 'assert', 'testcase', 'testscript'],
            'GIT_OPERATIONS': ['merge', 'branch', 'pull', 'git', 'gitignore'],
            'STYLING/FRONT_END': ['style', 'format', 'styling', 'convention', 'formatting', 'layout', 'view', 'ux', 'design',
                        'css', 'html', 'ui', 'gui', 'interface', 'graphic', 'graphical', 'stylesheet', 'theme', 'color',
                        'font', 'icon', 'animation', 'transition', 'responsive', 'prototype', 'palette', 'grid', 'alignment',
                        'interactive', 'darkmode', 'lightmode', 'display', 'diagram', 'chart', 'input', 'event-listener',
                                  'menu', 'dark', 'light', 'window', "image", "img"],
            'DEPLOYMENT/PUBLISH': ['deploy', 'release', 'production', 'deployment', 'rollout', 'launch', 'migration',
                                   'dev', 'publish', 'build', 'compile'],
            'SECURITY': ['security', 'vulnerability', 'secure', 'cve', 'encrypt', 'safety', 'authentication', 'auth',
                         'authorization', 'encryption', 'crypt', 'ssl', 'hack', 'breach', 'password', 'firewall', '2fa',
                         'csrf', 'xss', 'sqlinject', 'malware', 'ransomware', 'phishing', 'ddos'],
            'CLEANUP': ['cleanup', 'tidy', 'remove', 'delete', 'prune', 'clean', 'refine'],
            'SETUP': ['initial', 'init', 'introduce', 'setup', 'first', 'installation', 'config', 'configure', 'tool', 'dependency',
                      'api', 'apis', 'import', 'template', 'library', 'lib', 'libs', 'plugin', 'mvc', 'structure', 'backbone',
                      'skeleton', 'boilerplate', 'build', 'package', 'gradle', 'integration', 'start', 'release', 'jdk', 'extension', 'import'],
            'UPDATE': ['update', 'upgrade', 'refresh', 'renew', 'version', 'change', 'revise', 'deprecation'],
            'PERFORMANCE': ['performance', 'speed', 'efficiency', 'optimize', 'optimization', 'improve', 'latency',
                            'load', 'time', 'concurrency', 'thread', 'multithread', 'parallel', 'bottleneck', 'async',
                            'asynchronous', 'throttle', 'debounce', 'response', 'accelerate', 'memory', 'stable', 'sync'],
            'DATABASE': ['database', 'db', 'sql','sqlite', 'table', 'schema', 'entity', 'query', 'join', 'sqlcipher',
                         'relationship', 'column', 'data', 'datastore', 'mongodb', 'mysql', 'postgresql', 'postgresqlp',
                         'postgres', 'modeling', 'transaction', 'key', 'alter', 'drop', 'partition', 'migrate',
                         'querybuilder', 'request', 'querycondition'],
            'OTHER': []
        }
        self.commit_messages = commits

    def preprocess_data(self):
        """
        Preprocess the git commit messages by defining stop words, lemmatize, and tokenize.
        :return: Preprocessed commit messages.
        """
        nlp = spacy.load("en_core_web_sm")

        # Define custom stopwords
        custom_stop_words = ['a', 'the', 'and', 'etc', 'zip', 'use', 'instead', 'easy', ' ', 'non', 'no', 'ensure'
                           'minor', 'example', 'null', 'call', 'method', 'prepare', 'support', 'set', 'snapshot',
                           'class', 'close', 'code', 'extract', 'available', 'object', 'fix', 'type', 'follow',
                           'expect', 'flag', 'src', 'main', 'master']

        for stop_word in custom_stop_words:
            nlp.vocab[stop_word].is_stop = True

        preprocessed_commits = []

        for commit in self.commit_messages:
            # Tokenize and preprocess each commit message
            doc = nlp(commit.lower())
            tokens = [token.lemma_ for token in doc
                      if not token.is_stop
                      and token.is_alpha  # Ensure token is fully alphabetic
                      ]
            preprocessed_commits.append(tokens)

        return preprocessed_commits

    @staticmethod
    def vectorize_data(preprocessed_commits):
        """
        Vectorize the preprocessed commits.
        :param preprocessed_commits: Preprocessed commits.
        :return: The dictionary and the bag-of-words corpus.
        """
        # Create a dictionary object from preprocessed_commits
        dictionary = corpora.Dictionary(preprocessed_commits)

        # Filter out low frequency words (remove rare words and limit the vocabulary size)
        dictionary.filter_extremes(no_below=2, keep_n=5000)

        # Create a bag of words (a way to count the number of words in each doc)
        bow_corpus = [dictionary.doc2bow(commit) for commit in preprocessed_commits]

        # Serialize the dictionary and BoW corpus to disk, saving memory
        dictionary.save('support/commit_dictionary.dict')  # Save the dictionary for future use
        corpora.MmCorpus.serialize('support/commit_bow_corpus.mm', bow_corpus)  # Save the BoW corpus

        return dictionary, bow_corpus

    def train_model(self):
        """
        Train the model.
        """

        # Preprocess messages
        preprocessed_commits = self.preprocess_data()
        dictionary, corpus = self.vectorize_data(preprocessed_commits)

        # Train LDA model
        lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=12, random_state=100,
                             update_every=1, chunksize=100, passes=10, alpha='auto', per_word_topics=True)

        # print("\nTopics found by the LDA model:")
        # for idx, topic in lda_model.print_topics(-1, num_words=10):
        #     print(f"Topic {idx}: {topic}")

        topic_keywords_with_weights = {}

        # For each topic found in the lda-model, extract the keywords with its weights.
        for idx, topic in lda_model.show_topics(num_topics=-1, formatted=False):
            # Extract keywords and their weights
            keywords_with_weights = [(word, round(weight, 4)) for word, weight in topic]
            topic_keywords_with_weights[idx] = keywords_with_weights

        # Map the keywords to category.
        topic_category_mappings = self.map_topics_to_categories(topic_keywords_with_weights)

        print("\nTop Topic-Category Mappings:")
        for i, (topic_num, best_category, weight) in enumerate(topic_category_mappings, 1):
            # Access the keywords and their weights for the current topic
            keywords_with_weights = topic_keywords_with_weights.get(topic_num, [])
            # Format the keywords and weights for printing
            keywords_str = " + ".join([f"{weight:.3f}*\"{word}\"" for word, weight in keywords_with_weights])
            print(
                f"{i}. Topic {topic_num} -> Category: {best_category} with weight {weight:.3f}\n    Words: {keywords_str}")

        # Save the lda-model.
        self.save_model(lda_model, dictionary, topic_category_mappings, corpus, preprocessed_commits)

    def map_topics_to_categories(self, topic_keywords_with_weights):
        """
        Maps topic to category.
        :param topic_keywords_with_weights: Topic keywords with their weights.
        :return: The result of the mapping.
        """

        topic_category_mappings = []

        # Loop over each topic with its keywords + weights.
        for topic_num, keywords_with_weights in topic_keywords_with_weights.items():
            # Initialize a dictionary to hold cumulative weights for each category
            category_weights = {category: 0 for category in self.categories.keys()}

            # For each keyword and its weight...
            for keyword, weight in keywords_with_weights:
                # For each category with its keywords...
                for category, cat_keywords in self.categories.items():
                    # If the keyword contains any of the substrings from cat_keywords...
                    if any(sub_keyword in keyword for sub_keyword in cat_keywords):
                        # Accumulate the weight for that category.
                        category_weights[category] += weight

            # Determine the category with the highest cumulative weight for this topic
            best_category = max(category_weights, key=category_weights.get)
            highest_weight = category_weights[best_category]

            # Check if there are no matching keywords, and assign to 'OTHER' if so
            if highest_weight == 0:
                best_category = 'OTHER'
                topic_category_mappings.append((topic_num, best_category, highest_weight))
            else:
                topic_category_mappings.append((topic_num, best_category, highest_weight))

        return topic_category_mappings
    
    def save_model(self, lda_model, dictionary, topic_category_mappings, corpus,  preprocessed_commits):
        """
        Saves the trained model.
        :param lda_model: Trained model.
        :param dictionary: Dictionary of preprocessed commits.
        :param topic_category_mappings: Topic-category mappings.
        :param corpus: Corpus of the data.
        :param preprocessed_commits: Preprocessed commits.
        """
        # Save the LDA model
        lda_model.save('lda_model.gensim')

        # Save the dictionary
        dictionary.save('dictionary.gensim')

        # Save the categories.
        with open('categories.pkl', 'wb') as f:
            pickle.dump(self.categories, f)

        # Save the topic-to-category mapping
        with open('topic_to_category_mapping.pkl', 'wb') as f:
            pickle.dump(topic_category_mappings, f)

        visualization = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary)
        # To run, write "start lda_visualization.html" in terminal
        pyLDAvis.save_html(visualization, "lda_visualization.html")

        # Measure the model.
        print('\nPerplexity: ', lda_model.log_perplexity(corpus,
                                                         total_docs=10000))

        coherence_model_lda = CoherenceModel(model=lda_model, texts=preprocessed_commits, dictionary=dictionary,
                                             coherence='c_v')
        coherence_lda = coherence_model_lda.get_coherence()
        print('\nCoherence Score: ', coherence_lda)  # higher is better

    @staticmethod
    def reset_model():
        try:
            if os.path.exists('support'):
                # Remove everything in the support directory
                shutil.rmtree('support')
                print("Removed the entire 'support' directory.")
                # Recreate the 'support' directory
                os.makedirs('support')
                print("Recreated the 'support' directory.")
        except Exception as e:
            print(f"Failed to reset model: {e}")


def fetch_commit_messages(path):
    """
    Fetches the commit-messaged from the repository path.
    :param path: Repository path.
    :return: Commits.
    """
    commits = []
    for commit in Repository(path).traverse_commits():
        commits.append(commit.msg)
    return commits


if __name__ == "__main__":
    """
    Main function.
    """
    # Initialize an empty list to hold all commit messages from all repositories
    all_commit_messages = []

    # Ask the user to enter the number of repositories
    num_repos = int(input("Enter the number of repositories: "))

    # Loop to handle multiple repositories
    for i in range(num_repos):
        repo_path = input(f"Enter the repository path or URL #{i + 1}: ")
        try:
            # Fetch commit messages for each repository
            commit_messages = fetch_commit_messages(repo_path)
            print(f"Retrieved {len(commit_messages)} commit messages from repository #{i + 1}.")

            # Append these messages to the overall list
            all_commit_messages.extend(commit_messages)
        except Exception as e:
            print(f"Error fetching commit messages from repository #{i + 1}: {e}", file=sys.stderr)

    # After collecting commits from all repositories, proceed with training
    if all_commit_messages:
        print(f"Total commit messages collected: {len(all_commit_messages)}")
        trainer = ModelTrainer(all_commit_messages)
        trainer.train_model()
    else:
        print("No commit messages were collected. Exiting.")
