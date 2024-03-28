import nltk
from nltk import bigrams, trigrams, FreqDist, pos_tag, ne_chunk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.chunk.regexp import RegexpParser
from collections import defaultdict
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tree import Tree
from spacy import displacy
import spacy
import pandas as pd
from termcolor import colored
import textstat
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import re

# Load spaCy's English language model
nlp = spacy.load("en_core_web_trf")
#nltk.download('maxent_ne_chunker')
#nltk.download('words')
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('vader_lexicon')

# Define the color mapping for POS tags

POS_COLORS = {
    "CC": {"text": "#000000", "background": "#FFFF99", "description": "Coordinating conjunction"},
    "CD": {"text": "#000000", "background": "#FFCC99", "description": "Cardinal number"},
    "DT": {"text": "#000000", "background": "#FFFFCC", "description": "Determiner"},
    "EX": {"text": "#000000", "background": "#FFCCFF", "description": "Existential there"},
    "FW": {"text": "#000000", "background": "#FFFFFF", "description": "Foreign word"},
    "IN": {"text": "#000000", "background": "#CCFFFF", "description": "Preposition or subordinating conjunction"},
    "JJ": {"text": "#000000", "background": "#CCCCFF", "description": "Adjective"},
    "JJR": {"text": "#000000", "background": "#9999FF", "description": "Adjective, comparative"},
    "JJS": {"text": "#000000", "background": "#6666FF", "description": "Adjective, superlative"},
    "LS": {"text": "#000000", "background": "#CCCCCC", "description": "List item marker"},
    "MD": {"text": "#000000", "background": "#FF99FF", "description": "Modal"},
    "NN": {"text": "#000000", "background": "#99FF99", "description": "Noun, singular or mass"},
    "NNS": {"text": "#000000", "background": "#66CC66", "description": "Noun, plural"},
    "NNP": {"text": "#000000", "background": "#999999", "description": "Proper noun, singular"},
    "NNPS": {"text": "#000000", "background": "#666666", "description": "Proper noun, plural"},
    "PDT": {"text": "#000000", "background": "#99FFFF", "description": "Predeterminer"},
    "POS": {"text": "#000000", "background": "#CCCCCC", "description": "Possessive ending"},
    "PRP": {"text": "#000000", "background": "#6699FF", "description": "Personal pronoun"},
    "PRP$": {"text": "#000000", "background": "#3366FF", "description": "Possessive pronoun"},
    "RB": {"text": "#000000", "background": "#FF9999", "description": "Adverb"},
    "RBR": {"text": "#000000", "background": "#FF6666", "description": "Adverb, comparative"},
    "RBS": {"text": "#000000", "background": "#FF3333", "description": "Adverb, superlative"},
    "RP": {"text": "#000000", "background": "#CCCCCC", "description": "Particle"},
    "SYM": {"text": "#000000", "background": "#FFFF66", "description": "Symbol"},
    "TO": {"text": "#000000", "background": "#CCFFFF", "description": "to"},
    "UH": {"text": "#000000", "background": "#FF99FF", "description": "Interjection"},
    "VB": {"text": "#000000", "background": "#FF6666", "description": "Verb, base form"},
    "VBD": {"text": "#000000", "background": "#FF3333", "description": "Verb, past tense"},
    "VBG": {"text": "#000000", "background": "#FF0000", "description": "Verb, gerund or present participle"},
    "VBN": {"text": "#000000", "background": "#CC0000", "description": "Verb, past participle"},
    "VBP": {"text": "#000000", "background": "#FF6666", "description": "Verb, non-3rd person singular present"},
    "VBZ": {"text": "#000000", "background": "#FF3333", "description": "Verb, 3rd person singular present"},
    "WDT": {"text": "#000000", "background": "#FFFFCC", "description": "Wh-determiner"},
    "WP": {"text": "#000000", "background": "#FFFF99", "description": "Wh-pronoun"},
    "WP$": {"text": "#000000", "background": "#FFFF66", "description": "Possessive wh-pronoun"},
    "WRB": {"text": "#000000", "background": "#FFFFCC", "description": "Wh-adverb"},
}


def tag_and_color(text, POS_COLORS):
    words = nltk.word_tokenize(text)
    tagged_words = nltk.pos_tag(words)
    html_content = '<div style="font-family: Arial, sans-serif;">'
    
    for word, tag in tagged_words:
        default_color_info = {
            "text": "#000000",
            "background": "#FFFFFF",
            "description": "Unknown"
        }
        color_info = POS_COLORS.get(tag, default_color_info)
        html_content += f'<span data-pos="{tag}" style="background-color: {color_info["background"]}; color: {color_info["text"]}; padding: 2px 4px; margin: 2px; border-radius: 4px;" title="{color_info["description"]}">{word}</span> '
    
    html_content += '</div>'
    return html_content

def generate_dependency_viz(text):
    doc = nlp(text)
    html = displacy.render(doc, style='dep', jupyter=False, options={'distance': 80})
    return html


def perform_sentiment_analysis(text):
    # Initialize VADER's SentimentIntensityAnalyzer
    sia = SentimentIntensityAnalyzer()
    
    # Get the sentiment scores for the text
    sentiment_scores = sia.polarity_scores(text)
    
    # Return the sentiment scores
    return sentiment_scores


def generate_ngrams(tokens, n=2):
    if n == 2:
        return list(nltk.bigrams(tokens))  # Use nltk.bigrams directly
    elif n == 3:
        return list(nltk.trigrams(tokens))  # Use nltk.trigrams directly

def get_top_ngrams(tokens, n=2, top=50):
    ngrams = generate_ngrams(tokens, n)
    ngram_freq = nltk.FreqDist(ngrams)
    return ngram_freq.most_common(top)


def calculate_tf(text):
    # Tokenize the text
    tokens = nltk.word_tokenize(text)
    # Count frequencies
    freq_dist = FreqDist(tokens)
    # Normalize frequencies by document length
    tf_scores = {word: freq / len(tokens) for word, freq in freq_dist.items()}
    return tf_scores

def calculate_idf(corpus):
    # Count the number of documents containing each word
    word_doc_count = defaultdict(int)
    for text in corpus:
        tokens = set(nltk.word_tokenize(text))
        for token in tokens:
            word_doc_count[token] += 1
    # Calculate IDF, adding 1 to denominator to avoid division by zero
    idf_scores = {word: np.log(len(corpus) / (1 + count)) for word, count in word_doc_count.items()}
    return idf_scores

def calculate_tfidf(tf_scores, idf_scores):
    tfidf_scores = {word: tf * idf_scores.get(word, 0) for word, tf in tf_scores.items()}
    return tfidf_scores


def perform_ner(text):
    doc = nlp(text)
    return [(entity.text, entity.label_) for entity in doc.ents]

def calculate_readability(text):
    readability_scores = {
        'flesch_reading_ease': textstat.flesch_reading_ease(text),
        'smog_index': textstat.smog_index(text),
        'flesch_kincaid_grade': textstat.flesch_kincaid_grade(text),
        'coleman_liau_index': textstat.coleman_liau_index(text),
        'automated_readability_index': textstat.automated_readability_index(text),
        'dale_chall_readability_score': textstat.dale_chall_readability_score(text),
        'difficult_words': textstat.difficult_words(text),
        'linsear_write_formula': textstat.linsear_write_formula(text),
        'gunning_fog': textstat.gunning_fog(text),
    }
    return readability_scores

# Function to lemmatize text and filter non-alphabetic characters
def lemmatize_text(text):
    doc = nlp(text)
    lemmas = [token.lemma_ for token in doc if token.is_alpha]
    return lemmas

def create_cooccurrence_matrix(text):
    # Tokenize the text and remove punctuation and numbers
    tokens = nltk.word_tokenize(text)
    words = [word.lower() for word in tokens if word.isalpha()]
    
    # Instantiate a CountVectorizer
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform(words)
    
    # Create the co-occurrence matrix
    Xc = (X.T * X)  # This is the co-occurrence matrix
    Xc.setdiag(0)   # We set the diagonal to 0 as we don't want to count self co-occurrences
    
    # Create a DataFrame from the matrix
    vocab = vectorizer.get_feature_names_out()
    cooccurrence_matrix = pd.DataFrame(Xc.toarray(), index=vocab, columns=vocab)
    return cooccurrence_matrix, vocab

def extract_chunks(text):
    patterns = """
        Descriptive Attributes: {<DT>?<JJ>+<NN.*>+}        
        Specific Feature Descriptors: {<NN>+<NN>} 
        Detailed Subject Descriptors: {<NN|NNP|NNS|NNPS>+<IN|DT|NN|VB.|RB>*<JJ>+}    
        Subject Groups: {<NN|NNP|NNS|NNPS>{2,9}}                                     
        Action-Target Pairs: {<VB.>+<NN.>+}                                          
        Action Descriptions: {<RB.*>+<VB.*>+}                                        
        Opinions: {<NN.*|PRP><VBZ><JJ>}
        Strong Opinions: {<RB.*><JJ>}
        Comparative: {<JJR><IN><NN.*>+}
        Key Features Highlight: {<NN.*>+<VBZ|VBP><DT>?<JJ.*>+}
        Benefit: {<NN.*><IN><VBG>}
        Requirement or Need: {<VB.*><TO><VB>+}
    """
    chunk_parser = RegexpParser(patterns)
    sentences = sent_tokenize(text)
    
    phrase_details = defaultdict(lambda: defaultdict(lambda: {'Occurrences': 0, 'Sentences': []}))

    for sentence in sentences:
        words = word_tokenize(sentence)
        tagged_words = pos_tag(words)
        chunked = chunk_parser.parse(tagged_words)

        for subtree in chunked.subtrees():
            if subtree.label() in patterns:
                chunk_type = subtree.label()
                phrase = " ".join(word for word, tag in subtree.leaves())
                
                detail = phrase_details[chunk_type][phrase]
                detail['Occurrences'] += 1
                if sentence not in detail['Sentences']:
                    detail['Sentences'].append(sentence)

    chunk_dfs_html = {}
    
    for chunk_type, phrases in phrase_details.items():
        data = []
        for phrase, detail in phrases.items():
            for sent in detail['Sentences']:
                data.append({'Phrase': phrase, 'Occurrences': detail['Occurrences'], 'Sentence': sent})
        
        df = pd.DataFrame(data)
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'Index'}, inplace=True)
        
        # Generating unique table ID for each table
        table_id = f"table_{chunk_type}"
        
        # Generating HTML table with unique IDs for rows
        table_html = f'<table id="{table_id}"><thead><tr><th>Index</th><th>Phrase</th><th>Occurrences</th><th>Sentence</th></tr></thead><tbody>'
        row_id = 0
        for _, row in df.iterrows():
            row_id += 1
            table_html += f'<tr id="row_{table_id}_{row_id}">'
            table_html += f'<td>{row["Index"]}</td><td>{row["Phrase"]}</td><td>{row["Occurrences"]}</td><td>{row["Sentence"]}</td>'
            table_html += '</tr>'
        table_html += '</tbody></table>'
        
        sorting_buttons_html = f"""
        <div>
            <button onclick="sortByColumn('{table_id}', 1, true)">Sort Phrase A-Z</button>
            <button onclick="sortByColumn('{table_id}', 1, false)">Sort Phrase Z-A</button>
            <button onclick="sortByColumn('{table_id}', 2, true)">Sort Occurrences Asc</button>
            <button onclick="sortByColumn('{table_id}', 2, false)">Sort Occurrences Desc</button>
        </div>
        """
        
        highlight_script = f"""
        <script>
document.addEventListener('keydown', function(event) {{
    if (event.metaKey || event.ctrlKey) {{
        switch (event.key) {{
            case 'g':
                highlightText(window.getSelection().toString(), 'lightgreen');
                break;
            case 'r':
                highlightText(window.getSelection().toString(), 'salmon');
                break;
        }}
    }}
}});

function highlightText(searchText, color) {{
    if (searchText) {{
        var searchRegEx = new RegExp('(' + searchText + ')', 'ig');
        document.body.innerHTML = document.body.innerHTML.replace(searchRegEx, `<span style="background-color: ${{color}};">${{searchText}}</span>`);
    }}
}}

function addColorButton() {{
    var color = prompt('Enter the HEX color code (e.g., #FF5733):', '');
    var description = prompt('Enter a description/association for this color (e.g., Important):', '');
    if (color && description) {{
        var container = document.getElementById('highlightButtons');
        var legend = document.getElementById('legend');
        if (container && legend) {{
            // Update the button HTML to use the color for highlighting
            var buttonHTML = `<button onclick="highlightText(window.getSelection().toString(), '${{color}}')">Highlight ${{description}}</button>`;
            container.innerHTML += buttonHTML;

            // Update the legend with the provided description
            var entryHTML = `<div><span style="display:inline-block; width:20px; height:20px; background-color: ${{color}};"></span> ${{description}}</div>`;
            legend.innerHTML += entryHTML;
        }} else {{
            console.error('Element not found.');
        }}
    }}
}}

function sortByColumn(tableId, column, asc = true) {{
    const dirModifier = asc ? 1 : -1;
    const table = document.getElementById(tableId);
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));

    const sortedRows = rows.sort((a, b) => {{
        const aColText = column === 2 ? parseInt(a.querySelector(`td:nth-child(${{column + 1}})`).textContent.trim()) : a.querySelector(`td:nth-child(${{column + 1}})`).textContent.trim().toLowerCase();
        const bColText = column === 2 ? parseInt(b.querySelector(`td:nth-child(${{column + 1}})`).textContent.trim()) : b.querySelector(`td:nth-child(${{column + 1}})`).textContent.trim().toLowerCase();
        return aColText > bColText ? (1 * dirModifier) : (-1 * dirModifier);
    }});

    while (tbody.firstChild) tbody.removeChild(tbody.firstChild);
    tbody.append(...sortedRows);
}}
</script>
        """

        buttons_html = """
        <div id="highlightButtons">
            <button onclick="addColorButton()">Add New Color</button>
            <button onclick="highlightText(window.getSelection().toString(), 'lightgreen')">Highlight Positive</button>
            <button onclick="highlightText(window.getSelection().toString(), 'salmon')">Highlight Negative</button>
            
        </div>
        <div id="legend"><strong>Legend:</strong></div>
        <div><span style="display:inline-block; width:20px; height:20px; background-color: lightgreen;"></span> Positive</div>
        <div><span style="display:inline-block; width:20px; height:20px; background-color: salmon;"></span> Negative</div>
        <br><br>
        """
        
        title_html = f'<h2>{chunk_type}</h2>'
        chunk_html = title_html + sorting_buttons_html + table_html + buttons_html + highlight_script
        chunk_dfs_html[chunk_type] = chunk_html

    return chunk_dfs_html


def is_ipv4_address(text):
    ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(ipv4_pattern, text):
        octets = text.split('.')
        return all(0 <= int(octet) <= 255 for octet in octets) and not is_subnet_mask(text)
    return False
def is_ipv6_address(text):
    ipv6_pattern = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'
    return bool(re.match(ipv6_pattern, text))

def is_mac_address(text):
    mac_pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
    return bool(re.match(mac_pattern, text))

def is_bitcoin_address(text):
    p2pkh_pattern = r'^1[a-km-zA-HJ-NP-Z1-9]{25,34}$'
    p2sh_pattern = r'^3[a-km-zA-HJ-NP-Z1-9]{25,34}$'
    bech32_pattern = r'^bc1[ac-hj-np-z02-9]{11,71}$'

    return bool(re.match(p2pkh_pattern, text) or
                re.match(p2sh_pattern, text) or
                re.match(bech32_pattern, text))

def is_subnet_mask(text):
    # Attempt to identify a broader range of valid subnet masks by checking the general structure first
    ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(ipv4_pattern, text):
        return False
    
    octets = text.split('.')
    # Check if all octets are within the valid range for a subnet mask
    if not all(0 <= int(octet) <= 255 for octet in octets):
        return False
    
    # Convert octets to binary and join them to form a single binary string
    binary_mask = ''.join([bin(int(octet))[2:].zfill(8) for octet in octets])
    # Check for a valid sequence of '1's followed by '0's
    if '01' in binary_mask:
        return False  # Invalid sequence found, not a valid subnet mask
    return True  # Passed all checks, valid subnet mask

def get_subnet_class_and_range(subnet_mask):
    octets = subnet_mask.split('.')
    if octets[0] == '255' and octets[1] == '0' and octets[2] == '0' and octets[3] == '0':
        return "Class A", "0.0.0.0 - 127.255.255.255"
    elif octets[0] == '255' and octets[1] == '255' and octets[2] == '0' and octets[3] == '0':
        return "Class B", "128.0.0.0 - 191.255.255.255"
    elif octets[0] == '255' and octets[1] == '255' and octets[2] == '255' and octets[3] == '0':
        return "Class C", "192.0.0.0 - 223.255.255.255"
    else:
        return "Unknown Class", "Unknown Range"
    
def extract_numerical_sequences(text):
    # Extended pattern to capture more formats, especially credit cards with spaces/dashes
    num_pattern = r'''
        \b(?:\d{1,3}\.){3}\d{1,3}\b|            # IPv4
        \b[0-9a-fA-F:]{2,39}\b|                # IPv6 and MAC
        \b(?:\d{4}[ -]?){3}\d{4}\b|            # Credit Card, with spaces/dashes
        \b1[a-km-zA-HJ-NP-Z1-9]{25,34}\b|      # Bitcoin
        \b3[a-km-zA-HJ-NP-Z1-9]{25,34}\b|
        \bbc1[ac-hj-np-z02-9]{11,71}\b
    '''

    sequences = re.findall(num_pattern, text, re.VERBOSE)
    # Clean up credit card sequences
    sequences = [seq.replace(" ", "").replace("-", "") for seq in sequences]
    return sequences


def analyze_numerical_patterns(text):
    """
    Analyzes the given text for various numerical patterns by first extracting numerical sequences
    and then applying specific pattern checks.
    """
    results = {
        'IPv4 Addresses': [],
        'IPv6 Addresses': [],
        'MAC Addresses': [],        
        'Bitcoin Addresses': [],
        'Subnet Masks': [],
    }

    numerical_sequences = extract_numerical_sequences(text)
    print(f"Numerical sequences for analysis: {numerical_sequences}")  # Debugging statement

    for seq in numerical_sequences:
        if is_ipv4_address(seq):
            results['IPv4 Addresses'].append(seq)
            print(f"Found IPv4: {seq}")  # Debugging statement
        elif is_ipv6_address(seq):
            results['IPv6 Addresses'].append(seq)
            print(f"Found IPv6: {seq}") 
        elif is_mac_address(seq):
            results['MAC Addresses'].append(seq)        

        if is_bitcoin_address(seq):
            results['Bitcoin Addresses'].append(seq)
        
        if is_subnet_mask(seq):
            class_and_range = get_subnet_class_and_range(seq)
            results['Subnet Masks'].append(seq + f" ({class_and_range[0]}, {class_and_range[1]})")

    return results

