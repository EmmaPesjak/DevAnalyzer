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

# Exempel om man delar upp och joinar:
# Objectbox is a free, open-source, cross-platform app for iOS, Android, and Windows. The app is free to download and
# use, but not to modify. ObjectBox Java is a simple yet powerful database designed specifically for **Java and Kotlin**
# applications. Store and manage data effortlessly in your Android or JVM Linux, macOS or Windows app with ObjectBox.
# Enjoy exceptional speed, frugal resource usage, and environmentally-friendly development. ObjectBox is a free,
# open-source, Java-based data management tool. It can be used for iOS and Android projects. It has built-in support for
# object relations, allowing you to easily establish relationships between objects. Add the plugin to your root
# `build.gradle' app. Add the plugin using the plugin syntax or the old apply syntax. Create a data object class for the
# Playlist entity class. ObjectBox is a NoSQL Java database designed for local data storage on resource-restricted devices.
# It offers efficiency, ease of use, and flexibility. It has excellent performance, while also minimizing CPU, RAM, and
# power usage. ObjectBox simplifies development by requiring less code compared to SQLite. It operates on plain objects
# (POJOs) with built-in relations, eliminating the need to manage rows and columns. This is efficient for handling large
# data volumes and allows for easy model modifications. ObjectBox is a Java-based app-building tool for iOS and Android.
# It is available on GitHub and is available in a number of languages. ObjectBox is a free, open-source, cross-platform
# database. It's used to build fast mobile apps for iOS (and macOS) and desktop apps. Note that this license applies to
# the code in this repository only. pecific language governing permissions and limitations under the License. See our
# website on details about all [licenses for ObjectBox components]

# Exempel om man summarize alla summaries med 130 som maxlängd:
# ObjectBox is a free, open-source, Java-based data management tool. It can be used for iOS and Android projects. The app
# is free to download and use, but not to modify.

# Exempel om man summarize alla summaries med 200 som maxlängd:
# ObjectBox is a free, open-source, Java-based data management tool. It can be used for iOS and Android projects. It has
# built-in support for object relations, allowing you to easily establish relationships between objects. The app is free
# to download and use, but not to modify.

# Om man summarizar med 250 som längd:
# ObjectBox is a free, open-source, Java-based data management tool. It can be used for iOS and Android projects. It
# has built-in support for object relations, allowing you to easily establish relationships between objects. It's used
# to build fast mobile apps for iOS (and macOS) and desktop apps. The app is free to download and use, but not to modify.

# Om man preprocessar, summarizar summaries, och maxlängd 150
# ObjectBox Java is a simple yet powerful database designed specifically for **Java and Kotlin** applications. Store
# and manage data effortlessly in your Android or JVM Linux, macOS or Windows app with ObjectBox.Enjoy exceptional
# speed, frugal resource usage, and environmentally-friendly development.

# Just detta exempel jag har klistrat in genererar en helt ok summary:
# "ObjectBox is a NoSQL Java database designed for local data storage on resource-restricted devices.
# It offers efficiency, ease of use, and flexibility. It has excellent performance, while also
# minimizing CPU, RAM, and power usage."

# Men! kraschar för för långa readmes så vi måste segmentera eller välja ut stycken från dem
# Bestämma exakt vilken modell vi vill använda, T5 är ett annat option

#readme_content = ""
file_path = 'commit_messages/objectbox-java_readme.txt'

with open(file_path, 'r', encoding='utf-8') as file:
    readme_content = file.read()


# ## Key Features
# 🏁 **High performance:** exceptional speed, outperforming alternatives like SQLite and Realm in all CRUD operations.\
# 💚 **Efficient Resource Usage:** minimal CPU, power and memory consumption for maximum flexibility and sustainability.\
# 🔗 **[Built-in Object Relations](https://docs.objectbox.io/relations):** built-in support for object relations, allowing you to easily establish and manage relationships between objects.\
# 👌 **Ease of use:** concise API that eliminates the need for complex SQL queries, saving you time and effort during development.
# ## Why use ObjectBox for Java data management?
#
# ObjectBox is a NoSQL Java database designed for local data storage on resource-restricted devices, prioritizing
# offline-first functionality. It is a smart and sustainable choice for local data persistence in Java and Kotlin
# applications. It offers efficiency, ease of use, and flexibility.
#
# ### Fast but resourceful
# Optimized for speed and minimal resource consumption, ObjectBox is an ideal solution for mobile devices. It has
# excellent performance, while also minimizing CPU, RAM, and power usage. ObjectBox outperforms SQLite and Realm across
# all CRUD (Create, Read, Update, Delete) operations. Check out our [Performance Benchmarking App repository](https://github.com/objectbox/objectbox-performance).
#
# ### Simple but powerful
# With its concise language-native API, ObjectBox simplifies development by requiring less code compared to SQLite. It
# operates on plain objects (POJOs) with built-in relations, eliminating the need to manage rows and columns. This
# approach is efficient for handling large data volumes and allows for easy model modifications.
#
# ### Functionality
#
# 💐 **[Queries](https://docs.objectbox.io/queries):** filter data as needed, even across relations\
# 💻 **[Multiplatform](https://docs.objectbox.io/faq#on-which-platforms-does-objectbox-run):** supports Android and JVM on Linux (also on ARM), Windows and macOS\
# 🌱 **Scalable:** handling millions of objects resource-efficiently with ease\
# 🦮 **Statically typed:** compile time checks & optimizations\
# 📃 **Automatic schema migrations:** no update scripts needed
#
# **And much more than just data persistence**\
# 🔄 **[ObjectBox Sync](https://objectbox.io/sync/):** keeps data in sync between devices and servers\
# 🕒 **[ObjectBox TS](https://objectbox.io/time-series-database/):** time series extension for time based data
#
# ## Community and Support
#
# ❤ **Tell us what you think!** Share your thoughts through our [Anonymous Feedback Form](https://forms.gle/bdktGBUmL4m48ruj7).
#
# At ObjectBox, we are dedicated to bringing joy and delight to app developers by providing intuitive and fun-to-code-with
# APIs. We genuinely want to hear from you: What do you love about ObjectBox? What could be improved? Where do you face
# challenges in everyday app development?
#
# **We eagerly await your comments and requests, so please feel free to reach out to us:**
# - Add [GitHub issues](https://github.com/ObjectBox/objectbox-java/issues)
# - Upvote important issues 👍
# - Drop us a line via [@ObjectBox_io](https://twitter.com/ObjectBox_io/) or contact[at]objectbox.io
# - ⭐ us on GitHub if you like what you see!
#
# Thank you! Stay updated with our [blog](https://objectbox.io/blog)."""

# # Generate summary
# summary = summarizer(readme_content, max_length=130, min_length=30, do_sample=False)
# #TODO välja en bra längd på summarien här
# # do_sample controls whether the model should sample multiple times,
# # affecting the diversity of the output. Setting it to False makes the output more deterministic.
#
# # Print the summarized content
# print(summary[0]['summary_text'])

# Summarize the README content
# Preprocess to remove code snippets and other non-essential parts
preprocessed_content = preprocess_readme(readme_content)

# Generate and print the summary of preprocessed content
final_summary = summarize_text(preprocessed_content)
print(final_summary)
