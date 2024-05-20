from transformers import pipeline
import re
from support import constants


def preprocess_readme(readme_content):
    """
    Cleans the README content by removing HTML tags, code blocks, and inline code snippets
     to prepare it for summarization.
    :param readme_content: The original README file content.
    :return: The cleaned README content.
    """
    # Remove HTML tags
    no_html = re.sub(r'<.*?>', '', readme_content)
    # Remove code blocks enclosed in triple backticks
    no_code_blocks = re.sub(r'```.*?```', '', no_html, flags=re.DOTALL)
    # Remove inline code snippets enclosed in single backticks
    no_inline_code = re.sub(r'`.*?`', '', no_code_blocks)
    # Remove indented code blocks
    no_indented_code = re.sub(r'\n\s{4,}.*', '', no_inline_code)
    return no_indented_code


class BertReadmeModel:
    """
    Class for analyzing the README.md file.
    """

    def __init__(self):
        """
        Initializes the BertReadmeModel which utilizes the Hugging Face pipeline for summarization tasks,
        specifically using the pre-trained 'facebook/bart-large-cnn' model with truncation enabled to handle long texts.
        """
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn", truncation=True)

    def summarize_text(self, text, segment_length=1024, summary_max_length=150, summary_min_length=50):
        """
        Summarizes the given text by breaking it into manageable segments and summarizing each segment.
        If the overall summary is longer than the segment length, it is summarized again.
        :param text: The text to be summarized.
        :param segment_length: The length of text segments for individual summarization.
        :param summary_max_length: The maximum length of the summary for each segment.
        :param summary_min_length: The minimum length of the summary for each segment.
        :return: The summarized text.
        """
        # Early return if the text is too short to require summarization.
        if len(text) < summary_min_length:
            return text

        # Split the text into segments based on a predefined length, processing each segment individually
        # for summarization.
        segments = [text[i:i + segment_length] for i in range(0, len(text), segment_length)]
        summaries = []
        for segment in segments:
            # Adjust the maximum summary length based on the segment length.
            adjusted_max_length = min(summary_max_length, len(segment) // 2)
            # Generate a summary for each text segment using the predefined settings in the summarizer pipeline.
            summary = self.summarizer(segment, max_length=adjusted_max_length, min_length=summary_min_length,
                                      do_sample=False)
            summaries.append(summary[0]['summary_text'])
        # Combine individual segment summaries into one summary.
        combined_summaries = " ".join(summaries)
        # If the combined summaries exceed the segment length, summarize them again for conciseness.
        if len(combined_summaries) > segment_length:
            adjusted_max_length = min(summary_max_length, len(combined_summaries) // 2)
            final_summary = self.summarizer(combined_summaries, max_length=adjusted_max_length,
                                            min_length=summary_min_length, do_sample=False)
            return final_summary[0]['summary_text']
        else:
            return combined_summaries

    def get_readme_summary(self):
        try:
            # Attempt to open and read the README file.
            with open('support/Downloaded_README.txt', 'r', encoding='utf-8') as file:
                readme_content = file.read()

            # Return a default message if the README content is empty or only whitespace.
            if not readme_content.strip():
                return constants.NO_README_CONTENT

            # Preprocess and summarize the README content.
            preprocessed_content = preprocess_readme(readme_content)
            return self.summarize_text(preprocessed_content)
        except FileNotFoundError:
            # Handle the case where the README file does not exist.
            return constants.NO_README
