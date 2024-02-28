import gensim.models
import spacy
from gensim import corpora
from gensim import models


class CommitAnalyzer:
    def __init__(self):
        self.categories = ('BUG', 'FEATURE', 'MERGE', 'STYLE', 'REFACTOR', 'DOCUMENTATION', 'TEST',
                           'PRODUCTION', 'SECURITY', 'CLEANUP', 'INITIAL', 'SETUP', 'UPDATE', 'REVERT',
                           'PERFORMANCE')

    """TODO:
    NLP analyzing"""

    def nlp(self, all_commits):
        preprocessed_commits = self.preprocess_data(all_commits)
        word2vec_model = self.vectorize_data(preprocessed_commits)

    # SpaCy first step - preprocess data - get rid of all information that will not be used for the final output
    def preprocess_data(self, all_commits):
        nlp = spacy.load("en_core_web_sm")
        preprocessed_commits = []  # To store preprocessed tokens of each commit

        for commit in all_commits:

            # Check if the commit contains "Merge pull request".
            if "Merge pull request" in commit:
                print("Skipping: Contains 'Merge pull request'")
                continue  # Skip this commit- skip och sortera automatiskt som merge commit???

            doc = nlp(commit)
            #print(f"Original Commit Message: {commit}")

            # Adding custom stopwords.
            nlp.Defaults.stop_words.add("\n\n")

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


    # POS-tagging - behövs det i preprocessingen??
    # NER-tagging - behövs det i preprocessingen?? finns inget built-in i spacy som riktigt passar oss för NER
    # Dependency parsing

    # Topic model
    # Clustering and classification - unsuperviced clusering?