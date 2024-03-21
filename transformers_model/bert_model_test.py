from transformers import BertForSequenceClassification, BertTokenizerFast, pipeline
model_path = "./results/modelhej"

model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer= BertTokenizerFast.from_pretrained(model_path)
nlp= pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

print("*******")
print(nlp("Refactored the main database query for performance"))
print(nlp("Fixed null pointer exception in user login flow"))
print(nlp("Added pagination support to product listings"))
print(nlp("Implemented caching for user sessions"))
print(nlp("Resolved edge case in payment processing module"))
print(nlp("Enhanced search functionality with new filters"))
print(nlp("Updated README with new installation instructions"))
print(nlp("Optimized image loading for faster page render times"))
print(nlp("Fixed typo in the configuration loader"))
print(nlp("Added new API endpoint for retrieving user profiles"))
print(nlp("Merge branch 'fix-load-native-lib-for-static-methods' into 'dev'"))
print(nlp("Added styling for the view and diagrams"))

