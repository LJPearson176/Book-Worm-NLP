#glossary_html.py
glossary_html_content = """
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Glossary of Terms</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            padding: 20px;
            max-width: 1000px;
            margin: auto;
            background-color: #f4f4f4;
            color: #333;
        }
        h2, h3 {
            color: #2c3e50;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 10px;
        }
        p, li {
            font-size: 16px;
            line-height: 1.6;
            color: #555;
        }
        a {
            color: #3498db;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .header, .footer {
            text-align: center;
            margin: 20px 0;
        }
        input[type="text"], select {
            width: 100%;
            padding: 10px;
            margin: 10px 0 20px 0;
            border-radius: 5px;
            border: 1px solid #ccc;
            box-sizing: border-box;
        }
        ul, ol {
            list-style-type: none;
            padding: 0;
        }
        li {
            margin-bottom: 10px;
            padding: 10px;
            background-color: #fff;
            border-left: 5px solid #3498db;
            text-align: left;
        }
        b {
            color: #3498db;
        }
        li:hover {
            background-color: #bdc3c7;
        }
    </style>
</head>
<body>
    <div class="header">
        <h2>Glossary of Terms</h2>
        <input type="text" id="searchInput" placeholder="Type to search...">
    </div>
    <ul id="glossaryList">
        <!-- Glossary items will be inserted here by JavaScript -->
    </ul>

    <script>
        const glossaryItems = [
"A/B Testing: A randomized experiment with two variants, A and B, which are the control and treatment in the controlled experiment.",
"Abstraction-Based Summarization: A more complex approach in text summarization where the summary is generated anew, often involving paraphrasing or generating new sentences, not just extracting the existing ones from the source document. This approach often involves understanding the document and rephrasing its content in a shorter form.",
"Adjective: A word used to describe or modify a noun or pronoun, giving more information about the object's size, shape, age, color, origin, material, or purpose.",
"Adverb: A word that modifies or provides more information about a verb, adjective, or other adverb, often indicating manner, time, place, degree, or frequency.",
"Algorithm: A set of rules or processes to be followed in calculations or problem-solving operations, especially by a computer. In the context of NLP and data analysis, algorithms can range from simple statistical methods to complex machine learning models.",
"Artificial Intelligence (AI): A field of computer science dedicated to creating systems capable of performing tasks that typically require human intelligence, such as visual perception, speech recognition, decision-making, and language translation.",
"Auto-tag Generation: The process of automatically generating and assigning tags or keywords to a piece of content based on its content and context.",
"Bag of Words: A representation of text data where the text is represented as a bag (set) of its words, disregarding grammar and even word order but keeping multiplicity.",
"Chunking: Also known as shallow parsing, it's a process of extracting phrases from unstructured text, grouping together nouns, verbs, adjectives, etc., into chunks.",
"Co-occurrence Matrix: A matrix that counts how often different words occur together in a given dataset, helpful in understanding the context and relationship between words.",
"Corpus: A large and structured set of texts used in linguistic and NLP research.",
"Cosine Similarity: A metric used to measure how similar two documents are irrespective of their size, often used in text analysis.",
"Count Vector: A representation of text data where each dimension of the vector corresponds to a specific word in a corpus, and the value in each dimension counts the number of times the word appears in a document. It's a common way to transform text into a format that machine learning algorithms can process.",
"Data Analysis Pipeline: A sequence of data processing steps designed for transforming, enriching, and analyzing data to derive meaningful insights and information.",
"Data Frame: A table-like data structure, commonly used in data analysis and manipulation, that allows for the storage of data in rows and columns. Each column can hold values of a single data type and can be named to provide context for the data it holds.",
"Data Scientist: A professional who uses scientific methods, processes, algorithms, and systems to extract knowledge and insights from structured and unstructured data.",
"Dataset: A collection of data, typically tabulated by rows and columns in a table, so that a computer program can easily process it.",
"Exploratory Data Analysis (EDA): An approach to analyzing datasets to summarize their main characteristics, often with visual methods, before formal modeling.",
"Extraction-Based Summarization: A method in text summarization where sentences or phrases are selected directly from the source document to make up the new summary.",
"Filtering: The process of selecting or excluding certain elements, data, or information based on specific criteria.",
"GPT (Generative Pre-trained Transformer): An autoregressive language model that uses deep learning to produce human-like text. It is the third generation language prediction model in the GPT-n series created by OpenAI.",
"Genre Classification: The process of categorizing pieces of music, literature, or other forms of art into distinct genres.",
"Genre: A category of artistic composition, as in music or literature, characterized by similarities in form, style, or subject matter.",
"Inverse Document Frequency (IDF): A measure that reflects how important a word is to a document in a collection or corpus. The IDF increases with the rarity of the word across documents, allowing for the weighting of terms based on their relevance and uniqueness.",
"Inverse Document Frequency (IDF): A measure that reflects how important a word is to a document in a collection or corpus. The IDF value increases as the word appears in fewer documents, indicating the word is more unique to the specific document.",
"LDA (Latent Dirichlet Allocation): A generative statistical model that allows sets of observations to be explained by unobserved groups that explain why some parts of the data are similar.",
"Language Model: A statistical model that determines the probability of a sequence of words. It's used in various applications, including speech recognition, spelling correction, and machine translation.",
"Lemmatization: The process of reducing a word to its base or dictionary form, considering the word's part-of-speech and meaning.",
"Linear Regression: A linear approach to modeling the relationship between a scalar response and one or more explanatory variables (also known as dependent and independent variables).",
"Logistic Regression: A statistical model that in its basic form uses a logistic function to model a binary dependent variable, although many more complex extensions exist.",
"Machine Learning: A subset of artificial intelligence that provides systems the ability to automatically learn and improve from experience without being explicitly programmed.",
"N-grams: A contiguous sequence of n items from a given sample of text or speech. The items can be phonemes, syllables, letters, words, or base pairs according to the application.",
"Named Entity Recognition (NER): The identification and classification of named entities in text into predefined categories such as the names of persons, organizations, locations, expressions of times, quantities, monetary values, percentages, etc.",
"Natural Language Generation (NLG): The process of producing meaningful phrases and sentences in the form of natural language from some internal representation.",
"Natural Language Processing (NLP): A branch of artificial intelligence that helps computers understand, interpret, and manipulate human language.",
"Natural Language Understanding (NLU): A subtopic of natural language processing in artificial intelligence that deals with machine reading comprehension.",
"Noun: A word that serves as the name of a specific object or set of objects, such as living creatures, places, actions, qualities, states of existence, or ideas.",
"PCA (Principal Component Analysis): A statistical procedure that uses an orthogonal transformation to convert a set of observations of possibly correlated variables into a set of values of linearly uncorrelated variables called principal components.",
"Parsing: The process of analyzing a string of symbols, either in natural language or in computer languages, according to the rules of a formal grammar.",
"Part-of-Speech (POS) Tagging: The process of labeling words in a sentence as nouns, verbs, adjectives, etc., based on their definition and context.",
"Penn Treebank Project: A project that produced a large annotated corpus of English, providing part-of-speech tagging, syntactic parsing, and other forms of linguistic structure annotations. It has been widely used in computational linguistics and natural language processing research.",
"Phonemes: The smallest units of sound in a language that can distinguish one word from another. For example, the difference between the word 'bat' and 'pat' is the phonemes /b/ and /p/.",
"Preposition: A word governing, and usually preceding, a noun or pronoun and expressing a relation to another word or element in the clause.",
"Preprocessing Strategies: Techniques used to prepare raw data for further analysis or processing. In NLP, preprocessing may include tasks such as tokenization, lowercasing, removing stop words, and lemmatization, aimed at reducing noise and focusing on relevant information.",
"Python Library: A collection of modules and packages that allows developers to perform many tasks without writing their code.",
"Python: A high-level, interpreted, and general-purpose programming language known for its readability and versatility.",
"Readability Score: A measure used to assess how easy a text is to read. Various formulas consider factors such as sentence length and word complexity.",
"Regex (Regular Expression): A sequence of characters that forms a search pattern. Regex can be used to check if a string contains the specified search pattern, making it a powerful tool for string matching and manipulation.",
"Regex Parsing: The process of using regular expressions to identify and extract specific patterns from text. This technique is commonly used for data cleaning, data extraction, and complex text manipulation.",
"Rule-based System: A set of 'if-then' rules used for creating artificial intelligence (AI) applications, particularly for decision-making processes.",
"Semantics: The study of meaning in language. It deals with interpreting the meanings of words, phrases, and sentences.",
"Sentiment Analysis: The process of computationally identifying and categorizing opinions expressed in a piece of text to determine the writer's attitude towards a particular topic, product, etc.",
"Sentiment: A qualitative measure of the tone, viewpoint, or opinion expressed in a piece of text.",
"Spam: Irrelevant or unsolicited messages sent over the Internet, typically to a large number of users, for the purposes of advertising, phishing, spreading malware, etc.",
"Stop Words: Commonly used words (such as 'the', 'is', 'in') that a search engine has been programmed to ignore, both when indexing entries for searching and when retrieving them as the result of a search query.",
"Syllables: Units of organization for a sequence of speech sounds, typically consisting of a vowel sound and optionally, beginning or ending with one or more consonant sounds.",
"Syntax: The set of rules, principles, and processes that govern the structure of sentences in a given language, specifically word order.",
"TF-IDF (Term Frequency-Inverse Document Frequency): A numerical statistic intended to reflect how important a word is to a document in a collection or corpus. It is often used as a weighting factor in searches, text mining, and user modeling.",
"Term Frequency (TF): A measure of how frequently a term appears in a document, relative to the length of the document. It provides insight into the importance or relevance of a term within a specific document of a corpus.",
"Text Classification: The process of categorizing text into organized groups. It's used in a variety of applications, such as spam filtering and sentiment analysis.",
"Tokenization: The process of breaking down text into its individual components, such as words or sentences.",
"Topic Modeling: A type of statistical model for discovering the abstract 'topics' that occur in a collection of documents. It's frequently used in text mining.",
"Transformer: A deep learning model architecture designed to handle sequential data. It's known for its efficiency and scalability, especially in tasks like translation and text summarization.",
"Verb: A word that expresses an action, occurrence, or state of being.",
"Vernacular: The language or dialect spoken by the ordinary people in a particular country or region. In the context of NLP, vernacular processing involves understanding and interpreting regional slang or colloquial terms.",
"Word Cloud: A visual representation of text data, typically used to depict keyword metadata on websites, or to visualize free form text where the importance of each word is shown with font size or color.",
"Word Embeddings: A type of word representation that allows words with similar meaning to have a similar representation.",
        ];

        function filterGlossaryItems(query) {
            const filteredItems = glossaryItems.filter(item => item.toLowerCase().includes(query.toLowerCase()));
            const glossaryList = document.getElementById("glossaryList");
            glossaryList.innerHTML = filteredItems.map(item => {
                const [term, definition] = item.split(": ");
                return `<li><b>${term}:</b> ${definition}</li>`;
            }).join("");
        }

        document.getElementById("searchInput").addEventListener("input", (e) => {
            filterGlossaryItems(e.target.value);
        });

        // Initial display of all glossary items
        filterGlossaryItems("");
    </script>
</body>
</html>
"""
