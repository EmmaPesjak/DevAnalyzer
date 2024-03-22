from transformers import BertForSequenceClassification, BertTokenizerFast, pipeline
model_path = "./results/modelhej"

model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer= BertTokenizerFast.from_pretrained(model_path)
nlp= pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

print("*******")
# print(nlp("Refactored the main database query for performance"))
# print(nlp("Fixed null pointer exception in user login flow"))
# print(nlp("Added pagination support to product listings"))
# print(nlp("Implemented caching for user sessions"))
# print(nlp("Resolved edge case in payment processing module"))
# print(nlp("Enhanced search functionality with new filters"))
# print(nlp("Updated README with new installation instructions"))
# print(nlp("Optimized image loading for faster page render times"))
# print(nlp("Fixed typo in the configuration loader"))
# print(nlp("Added new API endpoint for retrieving user profiles"))
# print(nlp("Merge branch 'fix-load-native-lib-for-static-methods' into 'dev'"))
# print(nlp("Added styling for the view and diagrams"))

def print_prediction(message):
    prediction = nlp(message)  # Assuming this returns the category as a string
    print(f"Message: \"{message}\" Prediction: {prediction}")

print_prediction("Refactored the main database query for performance")
print_prediction("Fixed null pointer exception in user login flow")
print_prediction("Added pagination support to product listings")
print_prediction("Implemented caching for user sessions")
print_prediction("Resolved edge case in payment processing module")
print_prediction("Enhanced search functionality with new filters")
print_prediction("Updated README with new installation instructions")
print_prediction("Optimized image loading for faster page render times")
print_prediction("Fixed typo in the configuration loader")
print_prediction("Added new API endpoint for retrieving user profiles")
print_prediction("Merge branch 'fix-load-native-lib-for-static-methods' into 'dev'")
print_prediction("Added styling for the view and diagrams")
