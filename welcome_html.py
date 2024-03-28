# welcome_html.py
#.app-icon { display: inline-block; vertical-align: middle; width: 50px; height: auto; margin-bottom: 20px; }

welcome_html_content = """
        <html>
            <head>
                <style>
        body {
            font-family: 'Arial', sans-serif;
            padding: 20px;
            max-width: 1000px;
            margin: auto;
            background-color: #f4f4f4;
            color: #333;
        }
        .welcome-message, .title, .subtitle, .content, .footer {
            text-align: center;
            margin-bottom: 20px;
        }
        .title {
            font-size: 24px;
            color: #2c3e50;
        }
        .subtitle {
            font-size: 20px;
            color: #3498db;
        }
        .content p, .footer {
            font-size: 16px;
            line-height: 1.6;
            color: #555;
            max-width: 800px;
            margin: auto;
            text-align: justify;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            background-color: #fff;
            margin-bottom: 10px;
            padding: 10px;
            border-left: 5px solid #3498db;
        }
        b {
            color: #3498db;
        }
        .app-icon {
            display: block;
            margin: auto;
            width: 100px; /* Adjusted size for better visibility */
            height: auto;
            margin-bottom: 20px;
        }
    </style>
            </head>
            <body>
                <div class='welcome-message'>
                    <div class='title'>Welcome to Book Worm NLP</div>
                    <div style='text-align: center;'>
                        <img class='app-icon' src='resources/icons/appicon.png' alt='App Icon'>
                    </div>
                    <div class='subtitle'>Your personal NLP analysis toolkit</div>
                    <div class='content'>
                        <p>
                            Book Worm NLP is a powerful application that allows you to analyze text using various Natural Language Processing (NLP) techniques.
                            It provides a user-friendly interface to preprocess your text, select from a range of analysis techniques, and view the results in an intuitive manner.
                        </p>
                        <p>
                            To get started, simply paste your text into the 'Preprocessed Input' field on the left side of the application window.
                            You can then use the 'Preprocess' button to clean and prepare your text for analysis. This step includes tasks such as lowercasing, removing punctuation, and tokenizing the text.
                        </p>
                        <p>
                            Once your text is preprocessed, you can choose from a variety of NLP techniques available in the central column of the application.
                            These techniques include:
                        </p>
                        <ul>
                            <li><b>Readability Score:</b> Assess the difficulty level of your text based on various readability metrics such as Flesch Reading Ease, Smog Index, and more.</li>
                            <li><b>POS Tagging:</b> Analyze the part of speech for each word in your text, identifying whether a word is a noun, verb, adjective, etc.</li>
                            <li><b>POS Chunking:</b> Identify and extract meaningful phrases from your text based on part of speech patterns.</li>
                            <li><b>Bi-grams and Tri-grams:</b> Discover common word pairs and triplets in your text, providing insights into frequently occurring phrases.</li>
                            <li><b>Co-occurrence Matrix:</b> Explore the relationships between words in your text by visualizing their co-occurrence patterns.</li>
                            <li><b>NER:</b> Identify and extract named entities such as person names, organizations, locations, and more from your text.</li>
                        </ul>
                        <p>
                            After selecting the desired analysis technique, click the 'Analyze' button to run the analysis. The results will be displayed in the right column of the application.
                            You can view the results in various formats such as tables, graphs, and interactive visualizations, depending on the chosen technique.
                        </p>
                        <p>
                            Book Worm NLP also provides additional features to enhance your analysis experience. You can customize the list of stop words to exclude common words from your analysis.
                            Similarly, you can define your own set of key words to focus on specific terms of interest. The application allows you to easily add or remove stop words and key words as needed.
                        </p>
                        <p>
                            We hope that Book Worm NLP proves to be a valuable tool in your text analysis journey. Whether you're a researcher, data analyst, or simply curious about exploring the intricacies of language, this application aims to provide you with the necessary tools and insights.
                        </p>
                    </div>
                    <div class='footer'>
                        For any support or feedback, please feel free to reach out to us at support@bookwormnlp.com. We value your input and are committed to continuously improving the application to meet your needs.
                    </div>
                </div>
            </body>
        </html>
"""
