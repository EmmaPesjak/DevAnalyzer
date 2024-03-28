from transformers import pipeline

# Load the summarization pipeline with the BART model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


# Just detta exempel jag har klistrat in genererar en helt ok summary:
# "ObjectBox is a NoSQL Java database designed for local data storage on resource-restricted devices.
# It offers efficiency, ease of use, and flexibility. It has excellent performance, while also
# minimizing CPU, RAM, and power usage."

# Men! kraschar för för långa readmes så vi måste segmentera eller välja ut stycken från dem
# Bestämma exakt vilken modell vi vill använda, T5 är ett annat option

# TODO: detta får man ju ta från miningen
readme_content = """

## Key Features
🏁 **High performance:** exceptional speed, outperforming alternatives like SQLite and Realm in all CRUD operations.\
💚 **Efficient Resource Usage:** minimal CPU, power and memory consumption for maximum flexibility and sustainability.\
🔗 **[Built-in Object Relations](https://docs.objectbox.io/relations):** built-in support for object relations, allowing you to easily establish and manage relationships between objects.\
👌 **Ease of use:** concise API that eliminates the need for complex SQL queries, saving you time and effort during development.
## Why use ObjectBox for Java data management?

ObjectBox is a NoSQL Java database designed for local data storage on resource-restricted devices, prioritizing 
offline-first functionality. It is a smart and sustainable choice for local data persistence in Java and Kotlin 
applications. It offers efficiency, ease of use, and flexibility.

### Fast but resourceful
Optimized for speed and minimal resource consumption, ObjectBox is an ideal solution for mobile devices. It has 
excellent performance, while also minimizing CPU, RAM, and power usage. ObjectBox outperforms SQLite and Realm across 
all CRUD (Create, Read, Update, Delete) operations. Check out our [Performance Benchmarking App repository](https://github.com/objectbox/objectbox-performance).

### Simple but powerful
With its concise language-native API, ObjectBox simplifies development by requiring less code compared to SQLite. It 
operates on plain objects (POJOs) with built-in relations, eliminating the need to manage rows and columns. This 
approach is efficient for handling large data volumes and allows for easy model modifications.

### Functionality

💐 **[Queries](https://docs.objectbox.io/queries):** filter data as needed, even across relations\
💻 **[Multiplatform](https://docs.objectbox.io/faq#on-which-platforms-does-objectbox-run):** supports Android and JVM on Linux (also on ARM), Windows and macOS\
🌱 **Scalable:** handling millions of objects resource-efficiently with ease\
🦮 **Statically typed:** compile time checks & optimizations\
📃 **Automatic schema migrations:** no update scripts needed

**And much more than just data persistence**\
🔄 **[ObjectBox Sync](https://objectbox.io/sync/):** keeps data in sync between devices and servers\
🕒 **[ObjectBox TS](https://objectbox.io/time-series-database/):** time series extension for time based data

## Community and Support

❤ **Tell us what you think!** Share your thoughts through our [Anonymous Feedback Form](https://forms.gle/bdktGBUmL4m48ruj7).

At ObjectBox, we are dedicated to bringing joy and delight to app developers by providing intuitive and fun-to-code-with
APIs. We genuinely want to hear from you: What do you love about ObjectBox? What could be improved? Where do you face
challenges in everyday app development?

**We eagerly await your comments and requests, so please feel free to reach out to us:**
- Add [GitHub issues](https://github.com/ObjectBox/objectbox-java/issues) 
- Upvote important issues 👍
- Drop us a line via [@ObjectBox_io](https://twitter.com/ObjectBox_io/) or contact[at]objectbox.io
- ⭐ us on GitHub if you like what you see! 

Thank you! Stay updated with our [blog](https://objectbox.io/blog).
"""

# Generate summary
summary = summarizer(readme_content, max_length=130, min_length=30, do_sample=False)
#TODO välja en bra längd på summarien här
# do_sample controls whether the model should sample multiple times,
# affecting the diversity of the output. Setting it to False makes the output more deterministic.

# Print the summarized content
print(summary[0]['summary_text'])
