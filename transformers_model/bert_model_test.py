from transformers import BertForSequenceClassification, BertTokenizerFast, pipeline
model_path = "./results/trained_model"

model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizerFast.from_pretrained(model_path)
nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)


def print_prediction(message, should_be):
    prediction = nlp(message)
    print(f"Should be: \"{should_be}\" Prediction: {prediction}")


print_prediction("Refactored the main database query for performance", "Database")
print_prediction("Fixed null pointer exception in user login flow", "Bug fix")
print_prediction("Added pagination support to product listings", "Feature addition")
print_prediction("Implemented caching for user sessions", "Feature addition")
print_prediction("Resolved edge case in payment processing module", "Bug fix??")
print_prediction("Enhanced search functionality with new filters", "Feature addition??")
print_prediction("Updated README with new installation instructions", "Documentation")
print_prediction("Optimized image loading for faster page render times", "Feature addition?")
print_prediction("Fixed typo in the configuration loader", "Bug fix?")
print_prediction("Added new API endpoint for retrieving user profiles", "Feature addition?")
print_prediction("Merge branch 'fix-load-native-lib-for-static-methods' into 'dev'", "Git op")
print_prediction("Added styling for the view and diagrams", "styling/frontend")
