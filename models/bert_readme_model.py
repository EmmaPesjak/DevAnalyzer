from transformers import pipeline
import re

# Load the summarization pipeline with the BART model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", truncation=True)


# TODO preprocess readme to remove code etc

def preprocess_readme(readme_content):
    # Remove HTML tags
    no_html = re.sub(r'<.*?>', '', readme_content)

    # Remove code blocks enclosed in triple backticks
    no_code_blocks = re.sub(r'```.*?```', '', no_html, flags=re.DOTALL)

    # Remove inline code snippets enclosed in single backticks
    no_inline_code = re.sub(r'`.*?`', '', no_code_blocks)

    # Remove indented code blocks
    no_indented_code = re.sub(r'\n\s{4,}.*', '', no_inline_code)

    return no_indented_code


def summarize_text(text, segment_length=1024, summary_max_length=150, summary_min_length=50):
    # Divide the text into segments
    segments = [text[i:i + segment_length] for i in range(0, len(text), segment_length)]
    summaries = []

    for segment in segments:
        # Adjust max_length based on the segment size
        adjusted_max_length = min(summary_max_length, len(segment) // 2)

        # Generate summary for each segment
        summary = summarizer(segment, max_length=adjusted_max_length, min_length=summary_min_length, do_sample=False)
        summaries.append(summary[0]['summary_text'])

        # Combine the summaries into a single text
        combined_summaries = " ".join(summaries)

        # Summarize the combined summaries if it's longer than the segment length; otherwise, just use it as is
        if len(combined_summaries) > segment_length:
            # Adjust max_length based on the combined summaries' size
            adjusted_max_length = min(summary_max_length, len(combined_summaries) // 2)

            # Final summarization of the combined summaries
            final_summary = summarizer(combined_summaries, max_length=adjusted_max_length,
                                       min_length=summary_min_length, do_sample=False)
            return final_summary[0]['summary_text']
        else:
            return combined_summaries


# readme_content = ""
file_path = '../transformers_model/readmes/red5-server_readme.txt'

with open(file_path, 'r', encoding='utf-8') as file:
    readme_content = file.read()

# Summarize the README content
# Preprocess to remove code snippets and other non-essential parts
preprocessed_content = preprocess_readme(readme_content)

# Generate and print the summary of preprocessed content
final_summary = summarize_text(preprocessed_content)
print(final_summary)
