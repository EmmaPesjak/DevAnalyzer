import gensim.models
import spacy
from gensim import corpora
from gensim import models
from gensim.models import LdaModel
import pyLDAvis.gensim

class CommitAnalyzer:
    def __init__(self):
        self.categories = {
            'ERROR/BUG_HANDLING': ['error', 'bug', 'issue', 'correct', 'resolve', 'patch', 'conflict', 'debug', 'exception'],
            'FEATURE_ADDITIONS': ['add', 'feature', 'implement', 'implementation', 'new', 'introduce', 'create', 'generate','method'],
            'DOCUMENTATION': ['doc', 'readme', 'comment', 'tutorial', 'documentation', 'wiki', 'javadoc', 'description',  'javadocs', 'readme.md'],
            'REFACTORING': ['refactor', 'redundant', 'refactoring', 'clean', 'improve', 'performance', 'optimize', 'restructure', 'move', 'replace', 'typo', 'change', 'rename'],
            'TESTING': ['test', 'unittest', 'integrationtest', 'testing', 'tdd', 'assert'],
            'MERGE_OPERATIONS': ['merge', 'branch', 'pull', 'request', 'integrate', 'conflict'],
            'STYLING': ['style', 'format', 'lint', 'styling', 'convention', 'formatting'],
            'DEPLOYMENT/PUBLISH': ['deploy', 'release', 'production', 'deployment', 'rollout', 'launch', 'migration', 'dev', 'publish', 'build', 'compile'],
            'SECURITY': ['security', 'vulnerability', 'secure', 'cve', 'encrypt', 'safety', 'authentication'],
            'CLEANUP': ['cleanup', 'tidy', 'remove', 'delete', 'prune', 'clean', 'refine'],
            'SETUP': ['initial', 'init', 'introduce', 'setup', 'first', 'installation', 'config', 'tool', 'dependency', 'api', 'apis', 'import', 'template', 'library', 'lib', 'libs', 'plugin'],
            'UPDATE': ['update', 'upgrade', 'refresh', 'renew', 'version', 'change'],
            'REVERT': ['revert', 'undo', 'rollback', 'reverse'],
            'PERFORMANCE': ['performance', 'speed', 'efficiency', 'optimize', 'improve'],
            'DATABASE': ['database', 'db', 'sql', 'table', 'schema', 'entity', 'query', 'join', 'sqlcipher', 'relationship']
        }
        # TODO måste bestämma om vi ska träna modellen på repots egna data, eller om vi ska träna på annan data.


    def save_and_load_model(self):
        # TODO save and reload model later
        # trained LdaModel instance and dictionary is the Gensim dictionary used for the model
        # lda_model.save('lda_model.gensim')
        # dictionary.save('dictionary.gensim')
        #
        # # Other components to save
        # with open('topic_to_category_mapping.pkl', 'wb') as f:
        #     pickle.dump(topic_category_mapping, f)
        #
        # # When program starts, open the model
        # # Load the LDA model and dictionary
        # lda_model = LdaModel.load('lda_model.gensim')
        # dictionary = Dictionary.load('dictionary.gensim')
        #
        # # Load the topic-to-category mapping
        # with open('topic_to_category_mapping.pkl', 'rb') as f:
        #     topic_category_mapping = pickle.load(f)
        pass


    def nlp(self, all_commits):

        # Preprocess the commits
        preprocessed_commits = self.preprocess_data(all_commits)

        # Vectorize the preprocessed commits
        dictionary, bow_corpus = self.vectorize_data(preprocessed_commits)

        # Perform LDA topic modeling and get top keywords for each topic with their weights
        topic_keywords_with_weights, lda_model = self.perform_lda_topic_modeling(bow_corpus, dictionary)

        # Map topics to categories
        topic_category_mapping = self.map_topics_to_categories(topic_keywords_with_weights)

        # Print the top mappings
        print("Top Topic-Category Mappings:")
        for i, (topic_num, best_category, weight) in enumerate(topic_category_mapping, 1):
            # Access the keywords and their weights for the current topic
            keywords_with_weights = topic_keywords_with_weights.get(topic_num, [])
            # Format the keywords and weights for printing
            keywords_str = " + ".join([f"{weight:.3f}*\"{word}\"" for word, weight in keywords_with_weights])
            print(
                f"{i}. Topic {topic_num} -> Category: {best_category} with weight {weight:.3f}\n    Words: {keywords_str}")
        # TODO: sen här behöver vi kategorisera varje commit till varje topic, obs det kan finnas dubbletter här

    # SpaCy first step - preprocess data - get rid of all information that will not be used for the final output
    def preprocess_data(self, all_commits):
        nlp = spacy.load("en_core_web_sm")
        preprocessed_commits = []  # To store preprocessed tokens of each commit

        for commit in all_commits:
            # Lowercase the commit message.
            commit = commit.lower()

            # Check if the commit contains "Merge pull request".
            if "merge pull request" in commit:
                #print("Skipping: Contains 'Merge pull request'")
                # kanske ska ha
                # filtered_tokens = ['merge'] ?
                continue  # Skip this commit- skip och sortera automatiskt som merge commit???

            if "merge branch" in commit:
                continue  # Skip this commit

            # Tokenize the commit
            doc = nlp(commit)
            #print(f"Original Commit Message: {commit}")

            # Adding custom stopwords.
            nlp.Defaults.stop_words.add("\n\n")

            # TODO ta bort alla version grejer + alla som är 0.0.1 etc
            stop_words = ["\n\n", "a", "the", "and", "etc", "<", ">", "\n", "=", "zip", "use", "instead", "easy",
                          "\r\n\r\n", " ", "\t", "non", "no", "ensure", "minor", "example"]


            for stop_word in stop_words:
                lexeme = nlp.vocab[stop_word]
                lexeme.is_stop = True

            # Filtering out stopwords, punctuation, numbers, and  (duplicates can occur when the
            # commit messages contains both a title and a message with the same words). Also lemmatizing.
            filtered_tokens = set(
                [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and not token.like_num and
                 not token.like_url and not token.like_url])

            #print(f"Filtered Tokens: {filtered_tokens}")
            preprocessed_commits.append(filtered_tokens)

        return preprocessed_commits


    # Gensim vectorizing text feature extraction, OBS this is also a part of the pre-processing
    def vectorize_data(self, preprocessed_commits):

        # Create a dictionary object from preprocessed_commits (assigns a unique ID to each unique token)
        dictionary = corpora.Dictionary(preprocessed_commits)

        # Filter out low frequency words (remove rare words and limit the vocabulary size)
        dictionary.filter_extremes(no_below=2, keep_n=5000)  # might adjust these limits.

        # Create a bag of words (a way to count the number of words in each doc)
        bow_corpus = [dictionary.doc2bow(commit) for commit in preprocessed_commits]

        # # Serialize the dictionary and BoW corpus to disk, saving memory
        dictionary.save('support/commit_dictionary.dict')  # Save the dictionary for future use
        corpora.MmCorpus.serialize('support/commit_bow_corpus.mm', bow_corpus)  # Save the BoW corpus

        # # To demonstrate loading them back, not sure what exactly is necessary here yet.
        # loaded_dict = corpora.Dictionary.load('support/commit_dictionary.dict')
        # loaded_bow_corpus = corpora.MmCorpus('support/commit_bow_corpus.mm')
        # print(list(loaded_bow_corpus))  # This will print the loaded corpus without loading it entirely into memory

        # TF-IDF stands for Term Frequency Inverse Document Frequency of records. It can be defined as the
        # calculation of how relevant a word in a series or corpus is to a text.
        # tfidf = models.TfidfModel(loaded_bow_corpus)
        # for document in tfidf[loaded_bow_corpus]:
        #     print(document)
            # The float printed next to each word id is the product of the TF and IDF scores,
            # the higher the score - the more important the word is.

        print("-------")
        # bigrams for context??? vet inte om vi verkligen behöver det. isåfall ska det upp överst i denna metod.
        # bigram = gensim.models.Phrases(preprocessed_commits)
        # preprocessed_commits = [bigram[line] for line in preprocessed_commits]
        # print(preprocessed_commits)

        # Return the bag of words corpus and the dictionary object.
        return dictionary, bow_corpus


    def perform_lda_topic_modeling(self, bow_corpus, dictionary):
        # Number of topics
        num_topics = 10  # Adjust based on how many topics we want

        # Train LDA model on the Bag of Words corpus OBS alla parametrar måste vi kirra ordentligt
        lda_model = LdaModel(corpus=bow_corpus, id2word=dictionary, num_topics=num_topics, random_state=100,
                             update_every=1, chunksize=100, passes=15, alpha='auto', per_word_topics=True)

        topic_keywords_with_weights = {}
        for idx, topic in lda_model.show_topics(num_topics=-1, formatted=False):
            # Extract keywords and their weights
            keywords_with_weights = [(word, round(weight, 4)) for word, weight in topic]
            topic_keywords_with_weights[idx] = keywords_with_weights

        # Man kan visualisera den tränade lda modellen i jupyter eller som HTML:
        visualization = pyLDAvis.gensim.prepare(lda_model, bow_corpus, dictionary)
        # To run, write "start lda_visualization.html" in terminal
        pyLDAvis.save_html(visualization, "lda_visualization.html")

        #return topic_keywords, lda_model
        return topic_keywords_with_weights, lda_model

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
                        print("If hej Keyword: " + str(keyword))
                        # Accumulate the weight for that category.
                        category_weights[category] += weight
                #TODO Should none matched be handled differently

            # Determine the category with the highest cumulative weight for this topic
            best_category = max(category_weights, key=category_weights.get)
            topic_category_mappings.append((topic_num, best_category, category_weights[best_category]))

        return topic_category_mappings

    #TODO: Vi behöver refina modellen, tuna alla parametrar, improva preprocessing, definera categorierna mycket mycket bättre

    ## kap 11, räkna distance vectors, similarity queries och sånt på LDA och/eller tf-idf känns bra
    # men vad ska vi jämföra distance med det egentligen? vi har ju bara ett "dokument"

    ## kap 12 vafan ska man ha det till då?
    # ett tips där är att man kan sava alla sina modeller till RAM så som vi gör i vectorize_data
    # då kan man ju loada in dem i vilken metod som helst sen.
    # word2vec/doc2vec hade kanske varit bra för att se kontexten av ett ord? så man kan kategorisera enklare

    ## kap 14 - s251 här står det till och med att deep neural networks inte behöver vara bäst för
    # relativt små datasets, här kan till och med en liten bow performa bättre.

    # POS-tagging - behövs det i preprocessingen??
    # part-of-speech (noun, verb, adverb, etc). kan vara bra kanske för att kategorisera? typ om commiten är en
    # error "fix" eller "fixed new feature" t.ex.

    # NER-tagging - behövs det i preprocessingen?? finns inget built-in i spacy som riktigt passar oss för NER
    # named-entity-recognition. behövs ej

    # Dependency parsing
    # TODO after training the model, serialize the model??? scikit-learn is joblib or pickle
