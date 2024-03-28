from preprocessing import clean_text, convert_emojis_to_text, convert_numbers_to_words, replace_underscores, expand_contractions
import nltk
from nltk.corpus import stopwords
from features import generate_ngrams, get_top_ngrams, perform_ner, tag_and_color, POS_COLORS, calculate_readability, lemmatize_text, create_cooccurrence_matrix, extract_chunks, perform_sentiment_analysis
import pandas as pd

class NLPToolkitController:
    def __init__(self):
        self.stop_words_list = []
        self.stop_words = set(stopwords.words('english'))
        self.key_words_list = []
        self.use_stop_words = True
        self.use_key_words = False

    def preprocess_text(self, text):
        # Apply initial preprocessing steps in the correct sequence
        text = expand_contractions(text)
        text = convert_emojis_to_text(text)
        text = replace_underscores(text)
        text = convert_numbers_to_words(text)
        text = clean_text(text)
        text = convert_numbers_to_words(text)  # This seems to be repeated; consider if it's necessary

        # Conditional stop words filtering
        if self.use_stop_words:
            text_tokens = nltk.word_tokenize(text)
            text = ' '.join([word for word in text_tokens if word.lower() not in self.stop_words])

        # Apply lemmatization
        # Assuming `lemmatize_text_content` is a function you've defined that takes a string and returns a list of lemmatized words
        text = ' '.join(self.lemmatize_text_content(text))

        # Optionally emphasize key words if enabled
        # This part depends on how you want to emphasize key words - this is a placeholder for the logic
        if self.use_key_words and self.key_words_list:
            emphasized_text = []
            for word in text.split():
                if word.lower() in [kw.lower() for kw in self.key_words_list]:
                    # This is a placeholder for emphasis, e.g., making the word uppercase or appending a tag
                    emphasized_text.append(word.upper())  # Example: emphasize by making uppercase
                else:
                    emphasized_text.append(word)
            text = ' '.join(emphasized_text)

        print(f"Preprocessed text: {text}")
        return text


    def perform_ngram_analysis(self, text, n=2, top=50):
        # Tokenize the preprocessed text
        tokens = nltk.word_tokenize(text)
        # Optionally remove stop words from tokens if enabled
        if self.use_stop_words:
            tokens = [token for token in tokens if token not in self.stop_words]
        # Generate and get top n-grams
        return get_top_ngrams(tokens, n=n, top=top)

    def add_stop_word(self, word):
        self.stop_words.add(word)  # Efficiently manage stop words using a set

    def remove_stop_word(self, word):
        self.stop_words.discard(word)  # Safely remove the word if it exists

    def add_key_word(self, word):
        if word not in self.key_words_list:
            self.key_words_list.append(word)  # Maintain a list of key words
            
    def remove_key_word(self, word):
        if word in self.key_words_list:
            self.key_words_list.remove(word)  # Use remove method for lists


    def toggle_use_stop_words(self, use):
        self.use_stop_words = use
        print(f"Stop words filtering is now controller file debug {'enabled' if use else 'disabled'}.")  # Debug print

    def toggle_use_key_words(self, use):
        self.use_key_words = use
        print(f"key words filtering is now controller file debug {'enabled' if use else 'disabled'}.")  # Debug print
        
    def perform_ner_analysis(self, text):
        print("Starting NER analysis...")
        try:
            # Perform NER on the preprocessed text
            entities = perform_ner(text)
            print(f"NER entities found: {entities}")
            return entities
        except Exception as e:
            print(f"Error during NER analysis: {e}")
            return []

    def tag_and_color_text_to_html(self, text):
        # Use tag_and_color to generate the HTML content for tagged words
        tagged_html_content = tag_and_color(text, POS_COLORS)

        # Start constructing the final HTML content with a proper HTML structure
        final_html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
    body, html {
        margin: 0;
        padding: 0;
        height: 100%;
        box-sizing: border-box;
    }
    .content-area {
        padding: 10px;
        padding-bottom: 120px; /* Adjust based on legend height, ensures scrollable content does not go under the legend */
        overflow-y: auto;
        height: calc(100vh - 50px); /* Adjust if you have other headers or elements, subtract their height */
    }
    .legend {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        border-top: 2px solid #2c3e50;
        background: #f4f4f4;
        border-radius: 5px;
        padding: 5px;
        box-sizing: border-box;
        height: 400px; /* Define a fixed height for the legend */
    }
    table {
        width: 100%;
        table-layout: fixed;
        border-collapse: collapse;
    }
</style>
        </head>
        <body>
        """

        # Content area where the tagged text will be scrollable
        final_html_content += f'<div class="content-area">{tagged_html_content}</div>'

        # Fixed footer (legend) at the bottom
        final_html_content += '<div class="legend"><h2 style="text-align: center; margin-bottom: 10px;">POS Tags Legend</h2><table>'
        
        # Splitting the POS_COLORS into chunks to form rows in the table
        pos_items = list(POS_COLORS.items())
        num_columns = 6  # Define the number of columns you want
        for i in range(0, len(pos_items), num_columns):
            final_html_content += '<tr>'
            for pos, color_info in pos_items[i:i + num_columns]:
                final_html_content += f"""
                <td style="padding: 2px; text-align: center; font-size: 14px;">
                    <input type="checkbox" id="{pos}" name="pos_filter" value="{pos}" checked onclick="filterPOS()" style="margin-right: 5px;">
                    <label for="{pos}" style="background-color: {color_info["background"]}; color: {color_info["text"]}; padding: 2px 4px; border-radius: 4px; display: inline-block; width: auto;">{pos}</label>
                    <div style="color: #333; font-size: 12px;">{color_info["description"]}</div>
                </td>
                """
            final_html_content += '</tr>'
        final_html_content += '</table></div>'
        
        # JavaScript for POS filter functionality
        final_html_content += """
        <script type="text/javascript">
        function filterPOS() {
            var checkboxes = document.querySelectorAll('input[name="pos_filter"]:checked');
            var allWords = document.querySelectorAll('[data-pos]');
            allWords.forEach(word => word.style.display = 'none');
            checkboxes.forEach(checkbox => {
                document.querySelectorAll('[data-pos="' + checkbox.value + '"]').forEach(word => {
                    word.style.display = 'inline'; // Use 'inline' to keep word spacing consistent
                });
            });
        }
        document.addEventListener('DOMContentLoaded', filterPOS);
        </script>
        </body>
        </html>
        """

        return final_html_content

    def analyze_sentiment(self, text):
        # Perform sentiment analysis using the function from features.py
        sentiment_scores = perform_sentiment_analysis(text)
        
        # Return the full dictionary of sentiment scores
        # You could also return just sentiment_scores['compound'] for the overall sentiment
        return sentiment_scores    
    
    def calculate_readability_score(self, text):
        readability_scores = calculate_readability(text)
        return readability_scores
        
    def lemmatize_text_content(self, text):
        lemmatized_text = lemmatize_text(text)       
        return lemmatized_text

    def create_text_cooccurrence_matrix(self, text):
        cooccurrence_matrix, vocab = create_cooccurrence_matrix(text)
        return cooccurrence_matrix, vocab
    
    def perform_pos_chunking(self, text):
        # Call the extract_chunks function from features.py
        chunk_dfs = extract_chunks(text)                
        return chunk_dfs

