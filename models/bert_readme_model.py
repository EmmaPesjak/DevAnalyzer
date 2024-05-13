from transformers import pipeline
import re


class BertReadmeModel:

    def __init__(self):
        # Initialize the summarization pipeline
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn", truncation=True)

    def preprocess_readme(self, readme_content):
        # Remove HTML tags
        no_html = re.sub(r'<.*?>', '', readme_content)
        # Remove code blocks enclosed in triple backticks
        no_code_blocks = re.sub(r'```.*?```', '', no_html, flags=re.DOTALL)
        # Remove inline code snippets enclosed in single backticks
        no_inline_code = re.sub(r'`.*?`', '', no_code_blocks)
        # Remove indented code blocks
        no_indented_code = re.sub(r'\n\s{4,}.*', '', no_inline_code)
        return no_indented_code

    def summarize_text(self, text, segment_length=1024, summary_max_length=150, summary_min_length=50):
        # Early return if the text is too short to require summarization
        if len(text) < summary_min_length:
            return text

        segments = [text[i:i + segment_length] for i in range(0, len(text), segment_length)]
        summaries = []
        for segment in segments:
            adjusted_max_length = min(summary_max_length, len(segment) // 2)
            summary = self.summarizer(segment, max_length=adjusted_max_length, min_length=summary_min_length, do_sample=False)
            summaries.append(summary[0]['summary_text'])
        combined_summaries = " ".join(summaries)
        if len(combined_summaries) > segment_length:
            adjusted_max_length = min(summary_max_length, len(combined_summaries) // 2)
            final_summary = self.summarizer(combined_summaries, max_length=adjusted_max_length, min_length=summary_min_length, do_sample=False)
            return final_summary[0]['summary_text']
        else:
            return combined_summaries

    def get_readme_summary(self):
        try:
            with open('support/Downloaded_README.txt', 'r', encoding='utf-8') as file:
                readme_content = file.read()

            # Check if the content is empty or consists only of whitespaces
            if not readme_content.strip():
                return "No README file found in the root directory of selected project."

            preprocessed_content = self.preprocess_readme(readme_content)
            return self.summarize_text(preprocessed_content)
        except FileNotFoundError:
            # Handle the case where the README file does not exist
            return "No README file found in the root."

    # def get_readme_summary(self):
    #     with open('support/Downloaded_README.txt', 'r', encoding='utf-8') as file:
    #         readme_content = file.read()
    #     preprocessed_content = self.preprocess_readme(readme_content)
    #     return self.summarize_text(preprocessed_content)

