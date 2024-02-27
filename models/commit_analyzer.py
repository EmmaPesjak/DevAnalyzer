import spacy

class CommitAnalyzer:
    def __init__(self):
        self.categories = ('BUG', 'FEATURE', 'MERGE', 'STYLE', 'REFACTOR', 'DOCUMENTATION', 'TEST',
                           'PRODUCTION', 'SECURITY', 'CLEANUP', 'INITIAL', 'SETUP', 'UPDATE', 'REVERT',
                           'PERFORMANCE')

    """TODO:
    NLP analyzing"""

    # SpaCy first step - preprocess data - get rid of all information that will not be used for the final output
    def preprocess_data(self, all_commits):
        nlp = spacy.load("en_core_web_sm")

        for commit in all_commits:

            # Check if the commit contains "Merge pull request".
            if "Merge pull request" in commit:
                print("Skipping: Contains 'Merge pull request'")
                print("-------\n")
                continue  # Skip this commit- skip och sortera automatiskt som merge commit???

            doc = nlp(commit)
            #print(f"Original Commit Message: {commit}")

            # Adding custom stopwords.
            nlp.Defaults.stop_words.add("\n\n")

            # Filtering out stopwords, punctuation, numbers, and duplicates.
            filtered_tokens = set(
                [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and not token.like_num])

            print(f"Filtered Tokens: {filtered_tokens}")
            print("-------\n")



    # Gensim vectorizing text

    # POS-tagging
    # NER-tagging
    # Dependency parsing

    # Topic model
    # Clustering and classification