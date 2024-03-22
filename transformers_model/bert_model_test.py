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
print_prediction("Implemented caching for user sessions", "Feature addition or Database")
print_prediction("Resolved edge case in payment processing module", "Bug fix??")
print_prediction("Enhanced search functionality with new filters", "Feature addition??")
print_prediction("Updated README with new installation instructions", "Documentation")
print_prediction("Optimized image loading for faster page render times", "Feature addition/Styling")
print_prediction("Fixed typo in the configuration loader", "Bug fix")
print_prediction("Added new API endpoint for retrieving user profiles", "Feature addition/Database")
print_prediction("Merge branch 'fix-load-native-lib-for-static-methods' into 'dev'", "Git op")
print_prediction("Added styling for the view and diagrams", "styling/frontend")

print_prediction("Refactored session handling for better scalability", "Feature addition")  # Improving functionality
print_prediction("Corrected data model relationships for consistency", "Bug fix/Database")  # Fixing a model issue
print_prediction("Introduced JWT for secure authentication", "Feature addition")  # Adding new functionality
print_prediction("Documented the process for setting up the development environment", "Documentation")  # Enhancing docs
print_prediction("Updated CSS for responsive design", "Styling/Frontend")  # UI/UX improvements
print_prediction("Fixed race condition in asynchronous task processing", "Bug fix")  # Correcting concurrency issue
print_prediction("Added unit tests for the new user service methods", "Testing")  # Expanding test coverage
print_prediction("Implemented new GraphQL query for custom reports", "Feature addition/Database")  # Adding new query functionality
print_prediction("Revised README for better project clarity", "Documentation")  # Making project info clearer
print_prediction("Optimized SQL queries for report generation", "Database")  # Database performance improvement
print_prediction("Resolved merge conflicts in the feature branch", "Git operations")  # Handling Git workflow
print_prediction("Enhanced form validation logic", "Feature addition")  # Improving data validation
print_prediction("Addressed XSS vulnerability in user input handling", "Bug fix")  # Security enhancement
print_prediction("Implemented lazy loading for images", "Feature addition/Styling")  # Performance and style

