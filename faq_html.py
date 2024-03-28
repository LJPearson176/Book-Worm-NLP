# faq_html.py

faq_html_content = """
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
            }
            .btn {
                display: inline-block;
                padding: 10px 20px;
                background-color: #3498db;
                color: #fff;
                border-radius: 5px;
                cursor: pointer;
                border: none;
            }
            .btn:hover {
                background-color: #2980b9;
            }
        </style>
    </head>
    <body>
        <h2>FAQ / Getting Started</h2>
        <p>Welcome to the FAQ/Getting Started section, designed to help you navigate and make the most out of Book Worm NLP, even if you're new to the world of Natural Language Processing.</p>

        <h3>Getting Started with Exploratory Data Analysis</h3>
        <p>Embarking on your exploratory data analysis journey with Book Worm NLP is not just about answering questions you already have—it’s also about discovering questions you hadn’t thought to ask. Here’s how to begin:</p>
        <ol>
            <li><b>How to Preprocess Your Text:</b> Begin by copying your text into the 'Preprocessed Input' field. Click 'Preprocess' to prepare your text for analysis by cleaning and organizing the data.</li>
            <li><b>Choosing an Analysis Technique:</b> Dive into our suite of natural language processing techniques through the dropdown menu. Whether you're looking to gauge readability, uncover grammatical structures, or identify key entities, each technique offers unique insights. Experiment with different analyses to inspire your next questions and discover new perspectives.</li>
            <li><b>Viewing and Interpreting Results:</b> Explore your analysis results in an intuitive format, including graphs and summaries. Reflect on these insights, consider their implications, and think about how they can inform your decisions or further inquiries.</li>
        </ol>

        <h3>Frequently Asked Questions</h3>
        <ul>
            <li><b>Can I analyze text in any language?</b> Currently, our tool supports English, but we're actively working to include additional languages.</li>
            <li><b>How can I save my analysis results?</b> Click the 'Save' icon within the results tab to easily store and revisit your insights.</li>
            <li><b>What is POS Tagging?</b> Part-of-Speech Tagging categorizes words in a text into parts of speech, like nouns and verbs. It's foundational for understanding sentence structure and meaning.</li>
            <li><b>Can I customize the analysis parameters?</b> Yes, you can tailor parameters such as stop words and keywords to refine your analysis.</li>
            <li><b>Is there a way to visualize the analysis results?</b> We offer various visualization options, such as graphs, to help you understand and present your findings effectively.</li>
            <li><b>I'm new to NLP. Where can I learn about the terminology used?</b> Our <a href="#open_glossary">Glossary</a> page demystifies common NLP terms, making them accessible to beginners.</li>
        </ul>

        <p>Need more help or have specific questions? Reach out to us at support@bookwormnlp.com for personalized assistance.</p>
    </body>
</html>
"""
