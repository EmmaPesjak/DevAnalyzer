from transformers import BertForSequenceClassification, BertTokenizerFast, pipeline
model_path = "./results/trained_model"

model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizerFast.from_pretrained(model_path)
nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)


# Initialize counters
total_predictions = 0
correct_predictions = 0

def print_prediction(message, should_be):
    global total_predictions, correct_predictions
    prediction = nlp(message)
    predicted_label = prediction[0]['label']
    is_correct = should_be == predicted_label
    if is_correct:
        correct_predictions += 1
        print(f'1 - Should be: "{should_be}" Prediction: {predicted_label}')
    else:
        print(f'0 - Should be: "{should_be}" Prediction: {predicted_label} - Original message: "{message}"')
    total_predictions += 1

# List of messages and their expected labels
messages = [
    ("Added a feature", "Feature"),
    ("Use latest platform tools and tools with travis.", "Structure/Documentation"),
    ("update README.md deps to 3.1.0", "Structure/Documentation"),
    ("add data browser methods to BoxStore.java", "Data Handling"),
    ("Add NotNullThing and basic test.", "Testing"),
    ("added property.nonPrimitiveType flag", "Feature"),
    ("Travis: skip performance tests.", "Testing"),
    ("Merge pull request #990 from greenrobot/proguard-rules-in-readme README: add ProGuard rules.",
                     "Git Operation"),
    ("Merge branch '839-database-error-handler'", "Git Operation"),
    ("Update Gradle [4.10.3 -> 5.6.4].", "Structure/Documentation"),
    ("Increase Gradle default daemon heap size.", "Structure/Documentation"),
    ("Extract publish.gradle, only publish required projects.", "Structure/Documentation"),
    ("DatabaseOpenHelper: move EncryptedHelper out of class, use reflection.", "data handl/struct?"),
    ("Merge pull request #924 from greenrobot/428-avoid-art-warning Wrap EncryptedHelper in interface to reduce Art warnings",
        "Git Operation"),
    ("README: add keep rule for SqlCipherEncryptedHelper.", "Structure/Documentation"),
    ("Update Android Plugin [3.2.1 -> 3.5.3].", "Structure/Documentation"),
    ("Compile with SDK 29, for examples also target SDK 29.", "Structure/Documentation"),
    ("Examples: migrate to AndroidX, remove redundant casts, code clean-up.", "Structure/Documentation"),
    ("Examples: use Java 8 features.", "Structure/Documentation"),
    ("Add required Android JUnit test classes removed in SDK 28.", "Testing"),
    ("Robolectric workaround: set enableUnitTestBinaryResources false.", "Testing"),
    ("Merge pull request #1015 from greenrobot/updates Updates", "Git Operation"),
    ("https etc.", "other??"),
    ("fix JavaDocs: escape or replace some characters (>, <, &)", "Structure/Documentation"),
    ("Update freemarker [2.3.22 -> 2.3.29].", "Structure/Documentation"),
    ("Added styling for the view and diagrams", "Feature"),
    ("Fixed null pointer exception in user login flow", "Bug Fix/Error Handling"),
    ("Optimized image loading for faster page render times", "Feature")
]

for message, should_be in messages:
    print_prediction(message, should_be)

# Calculate and print the percentage of correct predictions
if total_predictions > 0:
    accuracy_percentage = (correct_predictions / total_predictions) * 100
    print(f'Accuracy: {accuracy_percentage:.2f}%')
else:
    print("No predictions were made.")


# print_prediction("Refactored the main database query for performance", "Database"
# print_prediction("Fixed null pointer exception in user login flow", "Bug fix")
# print_prediction("Implemented caching for user sessions", "Feature addition or Database")
# print_prediction("Resolved edge case in payment processing module", "Bug fix??")
# print_prediction("Enhanced search functionality with new filters", "Feature addition??")
# print_prediction("Updated README with new installation instructions", "Documentation")
# print_prediction("Optimized image loading for faster page render times", "Feature addition/Styling")
# print_prediction("Fixed typo in the configuration loader", "Bug fix")
# print_prediction("Added new API endpoint for retrieving user profiles", "Feature addition/Database")
# print_prediction("Merge branch 'fix-load-native-lib-for-static-methods' into 'dev'", "Git op")
# print_prediction("Added styling for the view and diagrams", "styling/frontend")
#
# print_prediction("Refactored session handling for better scalability", "Feature addition")  # Improving functionality
# print_prediction("Corrected data model relationships for consistency", "Bug fix/Database")  # Fixing a model issue
# print_prediction("Introduced JWT for secure authentication", "Feature addition")  # Adding new functionality
# print_prediction("Documented the process for setting up the development environment", "Documentation")  # Enhancing docs
# print_prediction("Updated CSS for responsive design", "Styling/Frontend")  # UI/UX improvements
# print_prediction("Fixed race condition in asynchronous task processing", "Bug fix")  # Correcting concurrency issue
# print_prediction("Added unit tests for the new user service methods", "Testing")  # Expanding test coverage
# print_prediction("Implemented new GraphQL query for custom reports", "Feature addition/Database")  # Adding new query functionality
# print_prediction("Revised README for better project clarity", "Documentation")  # Making project info clearer
# print_prediction("Optimized SQL queries for report generation", "Database")  # Database performance improvement
# print_prediction("Resolved merge conflicts in the feature branch", "Git operations")  # Handling Git workflow
# print_prediction("Enhanced form validation logic", "Feature addition")  # Improving data validation
# print_prediction("Addressed XSS vulnerability in user input handling", "Bug fix")  # Security enhancement
# print_prediction("Implemented lazy loading for images", "Feature addition/Styling")  # Performance and style

