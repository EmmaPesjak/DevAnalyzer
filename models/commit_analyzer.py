import gensim.models
import spacy
from gensim import corpora
from gensim import models
from gensim.models import LdaModel
import pyLDAvis.gensim

class CommitAnalyzer:
    def __init__(self):
        self.categories = ('BUG', 'FEATURE', 'MERGE', 'STYLE', 'REFACTOR', 'DOCUMENTATION', 'TEST',
                           'PRODUCTION', 'SECURITY', 'CLEANUP', 'INITIAL', 'SETUP', 'UPDATE', 'REVERT',
                           'PERFORMANCE')

    """TODO:
    NLP analyzing"""

    def nlp(self, all_commits):
        preprocessed_commits = self.preprocess_data(all_commits)
        dictionary, bow_corpus = self.vectorize_data(preprocessed_commits)

        # Now perform LDA topic modeling.
        lda_model = self.perform_lda_topic_modeling(bow_corpus, dictionary)


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

            doc = nlp(commit)
            #print(f"Original Commit Message: {commit}")

            # Adding custom stopwords.
            nlp.Defaults.stop_words.add("\n\n")

            stop_words = ["\n\n"]
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

        # Create a bag of word representation of the corpus.
        dictionary = corpora.Dictionary(preprocessed_commits)
        print(dictionary.token2id)

        bow_corpus = [dictionary.doc2bow(commit) for commit in preprocessed_commits]

        # Serialize the dictionary and BoW corpus to disk, saving memory
        dictionary.save('support/commit_dictionary.dict')  # Save the dictionary for future use
        corpora.MmCorpus.serialize('support/commit_bow_corpus.mm', bow_corpus)  # Save the BoW corpus

        # To demonstrate loading them back, not sure what exactly is necessary here yet.
        loaded_dict = corpora.Dictionary.load('support/commit_dictionary.dict')
        loaded_bow_corpus = corpora.MmCorpus('support/commit_bow_corpus.mm')

        print(list(loaded_bow_corpus))  # This will print the loaded corpus without loading it entirely into memory

        # TF-IDF stands for Term Frequency Inverse Document Frequency of records. It can be defined as the
        # calculation of how relevant a word in a series or corpus is to a text.
        tfidf = models.TfidfModel(loaded_bow_corpus)

        for document in tfidf[loaded_bow_corpus]:
            print(document)
            # The float printed next to each word id is the product of the TF and IDF scores,
            # the higher the score - the more important the word is.

        print("-------")
        # bigrams for context??? vet inte om vi verkligen behöver det. isåfall ska det upp överst i denna metod.
        bigram = gensim.models.Phrases(preprocessed_commits)
        preprocessed_commits = [bigram[line] for line in preprocessed_commits]
        print(preprocessed_commits)

        return dictionary, bow_corpus

    def perform_lda_topic_modeling(self, bow_corpus, dictionary):
        # Number of topics
        num_topics = 10  # Adjust based on your needs

        # Train LDA model on the Bag of Words corpus OBS alla parametrar måste vi kirra ordentligt
        lda_model = LdaModel(corpus=bow_corpus, id2word=dictionary, num_topics=num_topics, random_state=100,
                             update_every=1, chunksize=100, passes=10, alpha='auto', per_word_topics=True)

        # Print the topics found by the LDA model
        for idx, topic in lda_model.print_topics(-1):
            print('Topic: {} \nWords: {}'.format(idx, topic))


        # Man kan visualisera den tränade lda modellen i jupyter eller som HTML:
        visualization = pyLDAvis.gensim.prepare(lda_model, bow_corpus, dictionary)
        # Display in Jupyter Notebook.
        #pyLDAvis.display(visualization)
        # Or save to a standalone HTML file.
        # tar man denna kan man köra det i sin webbläsare genom att i sin terminal skriva "start lda_visualization.html"
        pyLDAvis.save_html(visualization, "lda_visualization.html")
        return lda_model



    # POS-tagging - behövs det i preprocessingen??
    # NER-tagging - behövs det i preprocessingen?? finns inget built-in i spacy som riktigt passar oss för NER
    # Dependency parsing

    # Topic model
    # Clustering and classification - unsuperviced clusering?