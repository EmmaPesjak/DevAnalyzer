from transformers import BertForSequenceClassification, BertTokenizerFast, pipeline
model_path = "./results/trained_model"

model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizerFast.from_pretrained(model_path)
nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)


def print_prediction(message, should_be):
    prediction = nlp(message)
    # print(f"Should be: \"{should_be}\" Prediction: {prediction}")
    # Extract the label from the prediction
    # Extract the label from the prediction
    predicted_label = prediction[0]['label']
    # Check if the predicted label matches the "should be" label exactly
    if should_be == predicted_label:
        print(f'1 - Should be: "{should_be}" Prediction: {predicted_label}')
    else:
        print(
            f'0 - Should be: "{should_be}" Prediction: {predicted_label} - Original message: "{message}"')


print_prediction("Added a feature","Feature")
print_prediction("Use latest platform tools and tools with travis.","Structure/Documentation")
print_prediction("update README.md deps to 3.1.0","Structure/Documentation")
print_prediction("add data browser methods to BoxStore.java","Data Handling")
print_prediction("Add NotNullThing and basic test.","Testing")
print_prediction("added property.nonPrimitiveType flag","Feature")
print_prediction("Travis: skip performance tests.","Testing")
print_prediction("Merge pull request #990 from greenrobot/proguard-rules-in-readme README: add ProGuard rules.","Git Operation")
print_prediction("Merge branch '839-database-error-handler'", "Git Operation")
print_prediction("Update Gradle [4.10.3 -> 5.6.4].", "Structure/Documentation")
print_prediction("Increase Gradle default daemon heap size.", "Structure/Documentation")
print_prediction("Extract publish.gradle, only publish required projects.", "Structure/Documentation")
print_prediction("DatabaseOpenHelper: move EncryptedHelper out of class, use reflection.", "data handl/struct?")
print_prediction("Merge pull request #924 from greenrobot/428-avoid-art-warning Wrap EncryptedHelper in interface to reduce Art warnings","Git Operation")
print_prediction("README: add keep rule for SqlCipherEncryptedHelper.", "Structure/Documentation")
print_prediction("Update Android Plugin [3.2.1 -> 3.5.3].", "Structure/Documentation")
print_prediction("Compile with SDK 29, for examples also target SDK 29.", "Structure/Documentation")
print_prediction("Examples: migrate to AndroidX, remove redundant casts, code clean-up.", "Structure/Documentation")
print_prediction("Examples: use Java 8 features.", "Structure/Documentation")
print_prediction("Add required Android JUnit test classes removed in SDK 28.", "Testing")
print_prediction("Robolectric workaround: set enableUnitTestBinaryResources false.", "Testing")
print_prediction("Merge pull request #1015 from greenrobot/updates Updates", "Git Operation")
print_prediction("https etc.", "other??")
print_prediction("fix JavaDocs: escape or replace some characters (>, <, &)", "Structure/Documentation")
print_prediction("Update freemarker [2.3.22 -> 2.3.29].", "Structure/Documentation")

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

