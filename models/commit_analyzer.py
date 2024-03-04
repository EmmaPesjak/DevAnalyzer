import gensim.models
import spacy
from gensim import corpora
from gensim import models
from gensim.models import LdaModel
import pyLDAvis.gensim

class CommitAnalyzer:
    def __init__(self):
        self.categories = {
            'BUG_FIXES': ['error', 'bug', 'issue', 'correct', 'resolve', 'patch'],
            'FEATURE_ADDITIONS': ['add', 'feature', 'implement', 'new', 'introduce', 'create'],
            'DOCUMENTATION': ['doc', 'readme', 'comment', 'tutorial', 'documentation', 'wiki'],
            'REFACTORING': ['refactor', 'clean', 'improve', 'performance', 'optimize', 'restructure'],
            'TESTING': ['test', 'unittest', 'integrationtest', 'testing', 'tdd', 'assert'],
            'MERGE_OPERATIONS': ['merge', 'branch', 'pull', 'request', 'integrate', 'conflict'],
            'STYLING': ['style', 'format', 'lint', 'styling', 'convention', 'formatting'],
            'DEPLOYMENT': ['deploy', 'release', 'production', 'deployment', 'rollout', 'launch'],
            'SECURITY': ['security', 'vulnerability', 'secure', 'cve', 'encrypt', 'safety', 'authentication'],
            'CLEANUP': ['cleanup', 'tidy', 'remove', 'delete', 'prune', 'clean', 'refine'],
            'PROJECT_SETUP': ['initial', 'setup', 'first', 'setup', 'installation', 'config'],
            'UPDATE': ['update', 'upgrade', 'refresh', 'renew', 'version'],
            'REVERT': ['revert', 'undo', 'rollback', 'reverse'],
            'PERFORMANCE': ['performance', 'speed', 'efficiency', 'optimize'],
            #'ERROR_HANDLING': ['error handling', 'exception management', 'error logging'], # BEHÅLLA?
            # TODO: här måste det förbättras som tusan!
        }



        # TODO måste bestämma om vi ska träna modellen på repots egna data, eller om vi ska träna på annan data.

    def nlp(self, all_commits):

        # Preprocess the commits
        preprocessed_commits = self.preprocess_data(all_commits)

        # Vectorize the preprocessed commits
        dictionary, bow_corpus = self.vectorize_data(preprocessed_commits)

        # Perform LDA topic modeling and get top keywords for each topic
        topic_keywords, lda_model = self.perform_lda_topic_modeling(bow_corpus, dictionary)

        # Map topics to categories
        topic_category_mapping = self.map_topics_to_categories(topic_keywords)

        # Print the top 10 topic-category mappings
        print("Top 10 Topic-Category Mappings:")
        for i, (topic, category) in enumerate(topic_category_mapping[:10], 1):
            print(f"{i}. Topic {topic} -> Category: {category}")
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
                print("Skipping: Contains 'Merge pull request'")
                # kanske ska ha
                # filtered_tokens = ['merge'] ?
                continue  # Skip this commit- skip och sortera automatiskt som merge commit???

            # Tokenize the commit
            doc = nlp(commit)
            #print(f"Original Commit Message: {commit}")

            # Adding custom stopwords.
            nlp.Defaults.stop_words.add("\n\n")

            stop_words = ["\n\n", "a", "the", "and"] # fler?


            for stop_word in stop_words:
                lexeme = nlp.vocab[stop_word]
                lexeme.is_stop = True

            # POS-tags, NER-tags, dependency injection can be very good but might add unnecessary
            # overhead as training the model is computationally heavy.
            # Här fins POS tags
            # for token in doc:
                # print(token.text, token.pos_, token.tag_)
            #
            # NER tags
            # for ent in doc.ents:
            #     print(ent.text, ent.label_)
            #
            # Depencency injection
            # for chunk in doc.noun_chunks:
            #     print(chunk.text, chunk.root.dep_, chunk.root.head.text)

            # Filtering out stopwords, punctuation, numbers, and  (duplicates can occur when the
            # commit messages contains both a title and a message with the same words). Also lemmatizing.
            filtered_tokens = set(
                [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and not token.like_num])

            print(f"Filtered Tokens: {filtered_tokens}")
            preprocessed_commits.append(filtered_tokens)

        return preprocessed_commits

    # Gensim vectorizing text feature extraction, OBS this is also a part of the pre-processing
    def vectorize_data(self, preprocessed_commits):

        # Vectorize; bag-of-words, TF-IDF, word2vec (chapter 8, chapter 12)
        # these vectors can will be passed into the LDA algorithms
        # TF-IDF is good for measuring how common or rare the word is among the docs, ignores common words - but
        # not good for us because commit messages are already small?? will it ignore "fix" for example?

        # Create a dictionary object from preprocessed_commits (assigns a unique ID to each unique token)
        dictionary = corpora.Dictionary(preprocessed_commits)

        # Filter out low frequency words (remove rare words and limit the vocabulary size)
        # get rid of words that occur in less than 2 documents or que ??? keep_n?
        dictionary.filter_extremes(no_below=2, keep_n=5000)  # might adjust these limits.
        #print(dictionary.token2id)

        # Create a bag of words (a way to count the number of words in each doc)
        bow_corpus = [dictionary.doc2bow(commit) for commit in preprocessed_commits]

        # # Serialize the dictionary and BoW corpus to disk, saving memory
        dictionary.save('support/commit_dictionary.dict')  # Save the dictionary for future use
        corpora.MmCorpus.serialize('support/commit_bow_corpus.mm', bow_corpus)  # Save the BoW corpus
        #
        # # To demonstrate loading them back, not sure what exactly is necessary here yet.
        # loaded_dict = corpora.Dictionary.load('support/commit_dictionary.dict')
        # loaded_bow_corpus = corpora.MmCorpus('support/commit_bow_corpus.mm')
        #
        # print(list(loaded_bow_corpus))  # This will print the loaded corpus without loading it entirely into memory

        # TF-IDF stands for Term Frequency Inverse Document Frequency of records. It can be defined as the
        # calculation of how relevant a word in a series or corpus is to a text.
        # tfidf = models.TfidfModel(loaded_bow_corpus)
        #
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


    def context_analysis(self):
        # TODO do context analysis to be analyze the context of the commit message. for example, if the message
        #  is "README: fix ...", it should belong to "DOCUMENTATION" and not "BUG_FIX". eller ge ord en range?
        #  t.ex README har högre rankning...eller ngt sånt mög
        pass

    def perform_lda_topic_modeling(self, bow_corpus, dictionary):
        # Number of topics
        num_topics = 10  # Adjust based on how many topics we want

        # Train LDA model on the Bag of Words corpus OBS alla parametrar måste vi kirra ordentligt
        # corpus = the dataset the LDA model will be trained
        # id2word = mapping from word IDs to words
        # num_topics = number of topics to extract from corpus
        # random_state = ensure reproducibility of the results
        # update_every = how often the model parameters should be updated (1 is updated after each batch of docs processed)
        # chunksize = number of documents to be used in each traning chunk
        # passes = total number of passes over the corpus during training
        # alpha = 'auto 'allows the model to automatically learn an optimal value
        # per_word_topics = True; computes a list of topics sorted in descending order of most likely topics for each word
        lda_model = LdaModel(corpus=bow_corpus, id2word=dictionary, num_topics=num_topics, random_state=100,
                             update_every=1, chunksize=100, passes=15, alpha='auto', per_word_topics=True)

        topic_keywords = []
        # Print the topics found by the LDA model
        for idx, topic in lda_model.print_topics(-1):
            # Extract only the words
            words = [word for word, _ in lda_model.show_topic(idx)]
            topic_keywords.append(words)
            print('Topic: {} \nWords: {}'.format(idx, topic))

        # Man kan visualisera den tränade lda modellen i jupyter eller som HTML:
        visualization = pyLDAvis.gensim.prepare(lda_model, bow_corpus, dictionary)
        # Display in Jupyter Notebook.
        #pyLDAvis.display(visualization)
        # Or save to a standalone HTML file.
        # tar man denna kan man köra det i sin webbläsare genom att i sin terminal skriva "start lda_visualization.html"
        pyLDAvis.save_html(visualization, "lda_visualization.html")
        return topic_keywords, lda_model

    def map_topics_to_categories(self, topic_keywords):

        # Define priority keywords for certain categories
        priority_keywords = {
            'BUG_FIXES': ['error', 'bug'],
            'DOCUMENTATION': ['readme', 'documentation', 'javadoc'],
            'TESTING': ['testing', 'test']
        }

        topic_category_mapping = []

        for i, keywords in enumerate(topic_keywords):
            best_match = None
            highest_priority_score = 0
            best_score = 0

            # First, check for priority keyword matches
            for category, priority_words in priority_keywords.items():
                if any(word in keywords for word in priority_words):
                    best_match = category
                    highest_priority_score = float('inf')  # Assign infinite score for priority match
                    break  # Stop searching if a priority match is found

            # If no priority match is found, proceed with general matching
            if highest_priority_score == 0:
                for category, cat_keywords in self.categories.items():
                    score = sum(1 for word in keywords if word in cat_keywords)
                    if score > best_score:
                        best_score = score
                        best_match = category

            topic_category_mapping.append((i, best_match))

        return topic_category_mapping

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
