import shutil
import sys

import spacy
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from gensim.corpora.dictionary import Dictionary
import pickle
from pydriller import Repository
import os
from gensim.models.coherencemodel import CoherenceModel

import pyLDAvis.gensim

# Check if the support directory exists, if not, create it
if not os.path.exists('support'):
    os.makedirs('support')


class ModelTrainer:
    def __init__(self, commits, identifier):
        self.categories = {
            'ERROR/BUG_HANDLING': ['error', 'bug', 'issue', 'correct', 'resolve', 'patch', 'conflict', 'debug',
                                   'exception', 'fault', 'glitch', 'incorrect', 'crash', 'failure', 'incomplete', 'diagnose',
                                   'troubleshoot', 'nullpointer', 'regression', 'deprecation', "warning"],
            'FEATURE_ADDITIONS': ['add', 'feature', 'implement', 'implementation', 'new', 'introduce', 'create',
                                  'generate', 'method', 'functionality'],
            'DOCUMENTATION': ['doc','docs', 'readme', 'comment', 'tutorial', 'documentation', 'wiki', 'javadoc', 'description',
                              'javadocs', 'readme.md', 'guide', 'manual', 'faq', 'help', 'specification', 'specs',
                              'commentary', 'instruction', 'file'],
            'REFACTORING': ['refactor', 'redundant', 'refactoring', 'clean', 'improve', 'restructure', 'move', 'replace',
                            'typo', 'change', 'rename', 'refine', 'simplify', 'streamline', 'unused', 'revert', 'undo',
                            'rollback', 'reverse', 'discard'],
            'TESTING': ['test', 'unittest', 'integrationtest', 'testing', 'tdd', 'assert', 'testcase', 'testscript'],
            'GIT_OPERATIONS': ['merge', 'branch', 'pull', 'git', 'gitignore'],
            'STYLING/FRONT_END': ['style', 'format', 'styling', 'convention', 'formatting', 'layout', 'view', 'ux', 'design',
                        'css', 'html', 'ui', 'gui', 'interface', 'graphic', 'graphical', 'stylesheet', 'theme', 'color',
                        'font', 'icon', 'animation', 'transition', 'responsive', 'prototype', 'palette', 'grid', 'alignment',
                        'interactive', 'darkmode', 'lightmode', 'display', 'diagram', 'chart', 'input', 'event-listener',
                                  'menu', 'dark', 'light', 'window'],
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
        self.identifier = identifier

    def preprocess_data(self):
        nlp = spacy.load("en_core_web_sm")

        # Define custom stopwords
        custom_stop_words = ["\n\n", "a", "the", "and", "etc", "<", ">", "\n", "=", "zip", "use", "instead", "easy",
                             "\r\n\r\n", " ", "\t", "non", "no", "ensure", "minor", "example", "null", "call", "method",
                             "prepare", "support", "set", "snapshot", "class", "close", "code", "extract", "available",
                             "object", "fix", "type", "follow", "expect", "flag"]
        for stop_word in custom_stop_words:
            nlp.vocab[stop_word].is_stop = True

        preprocessed_commits = []

        for commit in self.commit_messages:
            # Tokenize and preprocess each commit message
            doc = nlp(commit.lower())
            tokens = [token.lemma_ for token in doc if
                      not token.is_stop and
                      not token.is_punct and
                      not token.like_num and
                      not token.like_url
                      and token.is_alpha  # Ensure token is fully alphabetic
                      ]
            preprocessed_commits.append(tokens)

            # Lowercase the commit message.
            # commit = commit.lower()
            #
            # # Tokenize the commit
            # doc = nlp(commit)
            #
            # # Adding custom stopwords.
            # nlp.Defaults.stop_words.add("\n\n")
            #
            # stop_words = ["\n\n", "a", "the", "and", "etc", "<", ">", "\n", "=", "zip", "use", "instead", "easy",
            #               "\r\n\r\n", " ", "\t", "non", "no", "ensure", "minor", "example"]
            #
            # for stop_word in stop_words:
            #     lexeme = nlp.vocab[stop_word]
            #     lexeme.is_stop = True
            #
            # # Lemmatizes and filters out stopwords, punctuation, numbers, and  (duplicates can occur when the
            # # commit messages contains both a title and a message with the same words).
            # filtered_tokens = set(
            #     [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and not token.like_num and
            #      not token.like_url and not token.like_url])
            #
            # preprocessed_commits.append(filtered_tokens)

        return preprocessed_commits

    def vectorize_data(self, preprocessed_commits):
        # Create a dictionary object from preprocessed_commits
        dictionary = corpora.Dictionary(preprocessed_commits)

        # Filter out low frequency words (remove rare words and limit the vocabulary size)
        dictionary.filter_extremes(no_below=2, keep_n=5000)  # might adjust these limits.

        # Create a bag of words (a way to count the number of words in each doc)
        bow_corpus = [dictionary.doc2bow(commit) for commit in preprocessed_commits]

        # # Serialize the dictionary and BoW corpus to disk, saving memory
        # dictionary.save('support/commit_dictionary.dict')  # Save the dictionary for future use
        # corpora.MmCorpus.serialize('support/commit_bow_corpus.mm', bow_corpus)  # Save the BoW corpus
        #
        # print("-------")
        # return dictionary, bow_corpus
        # Append the identifier to filenames
        dictionary.save(os.path.join('support', f'commit_dictionary_{self.identifier}.dict'))
        corpora.MmCorpus.serialize(os.path.join('support', f'commit_bow_corpus_{self.identifier}.mm'), bow_corpus)

        return dictionary, bow_corpus

    def train_model(self):
        # Preprocess messages
        preprocessed_commits = self.preprocess_data()
        dictionary, corpus = self.vectorize_data(preprocessed_commits)

        # Train LDA model
        lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=8, random_state=100,
                             update_every=1, chunksize=100, passes=20, alpha='auto', per_word_topics=True)

        print("\nTopics found by the LDA model:")
        for idx, topic in lda_model.print_topics(-1, num_words=10):
            print(f"Topic {idx}: {topic}")

        topic_keywords_with_weights = {}
        for idx, topic in lda_model.show_topics(num_topics=-1, formatted=False):
            # Extract keywords and their weights
            keywords_with_weights = [(word, round(weight, 4)) for word, weight in topic]
            topic_keywords_with_weights[idx] = keywords_with_weights

        topic_category_mappings = self.map_topics_to_categories(topic_keywords_with_weights)

        print("\nTop Topic-Category Mappings:")
        for i, (topic_num, best_category, weight) in enumerate(topic_category_mappings, 1):
            # Access the keywords and their weights for the current topic
            keywords_with_weights = topic_keywords_with_weights.get(topic_num, [])
            # Format the keywords and weights for printing
            keywords_str = " + ".join([f"{weight:.3f}*\"{word}\"" for word, weight in keywords_with_weights])
            print(
                f"{i}. Topic {topic_num} -> Category: {best_category} with weight {weight:.3f}\n    Words: {keywords_str}")

        self.save_model(lda_model, dictionary, topic_category_mappings, corpus, preprocessed_commits)

    def map_topics_to_categories(self, topic_keywords_with_weights):

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
                # You might also want to set a default weight for 'OTHER', or just keep it at 0
                topic_category_mappings.append((topic_num, best_category, highest_weight))
            else:
                topic_category_mappings.append((topic_num, best_category, highest_weight))

        return topic_category_mappings
        #     # Determine the category with the highest cumulative weight for this topic
        #     best_category = max(category_weights, key=category_weights.get)
        #     topic_category_mappings.append((topic_num, best_category, category_weights[best_category]))
        #
        # return topic_category_mappings


    def save_model(self, lda_model, dictionary, topic_category_mappings, corpus, preprocessed_commits):
        # # Save the LDA model
        # lda_model.save('lda_model.gensim')
        #
        # # Save the dictionary
        # dictionary.save('dictionary.gensim')
        #
        # # Save the categories.
        # with open('categories.pkl', 'wb') as f:
        #     pickle.dump(self.categories, f)
        #
        # # Save the topic-to-category mapping
        # with open('topic_to_category_mapping.pkl', 'wb') as f:
        #     pickle.dump(topic_category_mappings, f)
        # Append the identifier to filenames
        lda_model.save(os.path.join('support', f'lda_model_{self.identifier}.gensim'))
        dictionary.save(os.path.join('support', f'dictionary_{self.identifier}.gensim'))

        with open(os.path.join('support', f'categories_{self.identifier}.pkl'), 'wb') as f:
            pickle.dump(self.categories, f)

        with open(os.path.join('support', f'topic_to_category_mapping_{self.identifier}.pkl'), 'wb') as f:
            pickle.dump(topic_category_mappings, f)

        visualization = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary)
        # To run, write "start lda_visualization.html" in terminal
        pyLDAvis.save_html(visualization, "lda_visualization.html")

        print('\nPerplexity: ', lda_model.log_perplexity(corpus,
                                                         total_docs=10000))  # a measure of how good the model is. lower the better.

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
    commits = []
    for commit in Repository(path).traverse_commits():
        commits.append(commit.msg)
    return commits


if __name__ == "__main__":
    reset = input("Do you want to reset the model before training? (yes/no): ").lower() == 'yes'

    if reset:
        ModelTrainer.reset_model()
    repo_path = input("Enter the repository path or URL: ")
    try:
        commit_messages = fetch_commit_messages(repo_path)
        print(f"Retrieved {len(commit_messages)} commit messages.")

        # Extract a simple identifier from the repository path or URL
        identifier = os.path.basename(
            repo_path.rstrip('/'))  # Remove trailing slash if present and use basename as identifier

        # You might want to replace or remove characters from the identifier that are not suitable for filenames
        identifier = identifier.replace('/', '_').replace(':', '_').replace(' ', '_')

        trainer = ModelTrainer(commit_messages, identifier)
        trainer.train_model()
    except Exception as e:
        print(f"Error fetching commit messages: {e}", file=sys.stderr)

# if __name__ == "__main__":
#     repo_path = input("Enter the repository path or URL: ")
#     try:
#         commit_messages = fetch_commit_messages(repo_path)
#         print(f"Retrieved {len(commit_messages)} commit messages.")
#         trainer = ModelTrainer(commit_messages)
#         trainer.train_model()
#     except Exception as e:
#         print(f"Error fetching commit messages: {e}", file=sys.stderr)

