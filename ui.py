import sys
import os
import nltk
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QComboBox, QLabel, QLineEdit, QCheckBox, QTabWidget, QFileDialog,
    QMessageBox, QStatusBar, QToolTip, QSizePolicy, QTextBrowser, QTableWidget, QTableWidgetItem, QDialog, QInputDialog
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtGui import (QAction, QIcon, QPixmap, QScreen, QCursor, QPainter)
from PySide6.QtCore import (QEvent, QPoint, Qt, QUrl, QObject, Slot, Signal) 
from PySide6.QtWebChannel import QWebChannel
 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd

import fitz  
from PIL import Image
import pytesseract
import io

from controller import NLPToolkitController  
import style_sheets
from faq_html import faq_html_content
from welcome_html import welcome_html_content
from glossary_html import glossary_html_content

HELP_EXPLANATIONS = {
    "Preprocessed Input": "This section displays the raw input text before any preprocessing is applied.",
    "Processed Input": "This section shows the input text after preprocessing, which includes operations like lowercasing, removing punctuation, and tokenization.",
    "Preprocess": "Clicking this button applies the preprocessing steps to the input text and updates the Processed Input section.",
    "Technique": "Select an NLP technique from the dropdown menu to perform analysis on the processed text.",
    "Analyze": "Clicking this button runs the selected NLP technique on the processed text and displays the results in a new tab.",
    "Stop Words": "Stop words are common words that are often filtered out before processing text. You can add custom stop words and toggle their usage.",
    "Key Words": "Key words are important terms that you want to emphasize or focus on in the analysis. You can add custom key words and toggle their usage.",
}

##Remove # below and update pathway to pytesseract exe - not py file- specifically the exe.
#pytesseract.pytesseract.tesseract_cmd = r'/pathway/to/pytesseract'

def create_help_icon(explanation):
    label = QLabel()
    label.setPixmap(QPixmap("resources/icons/question.png"))  # Replace with the path to your help icon image
    label.setToolTip(explanation)

    # Add event handling for click and hover
    label.mousePressEvent = lambda event: show_explanation(explanation)
    label.enterEvent = lambda event: show_tooltip(label, explanation)
    label.leaveEvent = lambda event: hide_tooltip(label)
    
    return label

class ListSelectionDialog(QDialog):
    listSelected = Signal(str, str)  # Emit both the list type and the selected path

    def __init__(self, listType, parent=None):
        super().__init__(parent)
        self.listType = listType  # Store the list type
        self.setWindowTitle(f"Select {listType}")
        layout = QVBoxLayout(self)

        self.listTypeComboBox = QComboBox()
        self.populateComboBox(listType)  # Populate the ComboBox based on the list type

        layout.addWidget(self.listTypeComboBox)

        self.confirmButton = QPushButton("Confirm Selection")
        self.confirmButton.clicked.connect(self.emitSelection)
        layout.addWidget(self.confirmButton)

    def populateComboBox(self, listType):
        if listType == 'Stop Words':
            files = os.listdir('resources/lists/Filter')
            self.listTypeComboBox.addItems(["Select List"] + files)
        elif listType == 'Key Words':
            categories = ["regional_vernacular", "domain", "people", "religious"]
            self.listTypeComboBox.addItems(["Select Category"] + categories)
        elif listType == 'Custom List':
            custom_dir = 'resources/lists/Custom'
            if not os.path.exists(custom_dir):
                os.makedirs(custom_dir)
            files = [f for f in os.listdir(custom_dir) if os.path.isfile(os.path.join(custom_dir, f))]
            self.listTypeComboBox.addItems(["Create New..."] + files)
        # Add conditions for other list types as necessary

    def emitSelection(self):
        selectedItem = self.listTypeComboBox.currentText()
        self.listSelected.emit(self.listType, selectedItem)  # Emit both list type and the selected item
        self.accept()
        
        
class ListManagementDialog(QDialog):
    def __init__(self, title, filePath, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.filePath = filePath
        layout = QVBoxLayout(self)

        self.listDisplay = QTextEdit()
        self.listDisplay.setText(self.loadItems())
        self.listDisplay.setReadOnly(False)  # Set to False if you want users to edit directly
        layout.addWidget(self.listDisplay)

        self.confirmButton = QPushButton("Confirm")
        self.confirmButton.clicked.connect(self.saveItems)
        layout.addWidget(self.confirmButton)

    def loadItems(self):
        try:
            with open(self.filePath, "r") as file:
                return file.read()
        except FileNotFoundError:
            return "File not found. Please create it."

    def saveItems(self):
        with open(self.filePath, "w") as file:
            file.write(self.listDisplay.toPlainText())
        self.accept()
       
       
class UseListDecisionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Use List For")
        layout = QVBoxLayout(self)

        # Options for the user to choose
        self.useForStopWordsBtn = QPushButton("Use for Stop Words")
        self.useForStopWordsBtn.clicked.connect(self.useForStopWords)
        layout.addWidget(self.useForStopWordsBtn)

        self.useForKeyWordsBtn = QPushButton("Use for Key Words")
        self.useForKeyWordsBtn.clicked.connect(self.useForKeyWords)
        layout.addWidget(self.useForKeyWordsBtn)

        self.cancelBtn = QPushButton("Cancel")
        self.cancelBtn.clicked.connect(self.reject)
        layout.addWidget(self.cancelBtn)

    def useForStopWords(self):
        self.done(1)  # Custom code to indicate selection

    def useForKeyWords(self):
        self.done(2)  # Custom code to indicate selection
       
       
class SentimentAnalysisHandler(QObject):
    @Slot(str, result=str)
    def analyzeSentiment(self, text):
        # Direct call to the perform_sentiment_analysis function
        sentiment_scores = perform_sentiment_analysis(text)
        # Here, you format the result as needed to display in the UI, this is just an example
        result = f"Compound: {sentiment_scores['compound']}"
        return result

def show_explanation(explanation):
    QMessageBox.information(None, "Help", explanation)

def show_tooltip(label, explanation):
    QToolTip.showText(QCursor.pos(), explanation, label)

def hide_tooltip(label):
    QToolTip.hideText()
    
    
class ToolTipComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tooltips = []
        self.installEventFilter(self)
        
    def setItemToolTip(self, index, tooltip):
        """Assigns a tooltip to a specific item index."""
        if index >= 0 and index < self.count():
            # Ensure the tooltips list has enough elements
            while len(self.tooltips) <= index:
                self.tooltips.append("")
            self.tooltips[index] = tooltip
            
    def showEvent(self, event):
        """Ensures the event filter is installed."""
        super().showEvent(event)
        self.view().viewport().installEventFilter(self)
        
    def eventFilter(self, watched, event):
        """Shows tooltips when hovering over items."""
        if event.type() == QEvent.Type.ToolTip:
            index = self.view().indexAt(event.pos())
            if index.isValid() and 0 <= index.row() < len(self.tooltips):
                QToolTip.showText(QCursor.pos(), self.tooltips[index.row()])
                return True
        return super().eventFilter(watched, event)    


class MplCanvas(FigureCanvas):
    def __init__(self, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class NLPToolkitUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setupUI()
        self.createMenus()
       
       
    def setupUI(self):
        self.setWindowTitle("Book Worm NLP")
        
        # Retrieve the size of the primary screen
        screen = QApplication.primaryScreen()
        rect = screen.availableGeometry()
        new_width = rect.width() * 0.95
        new_height = rect.height() * 0.95     
           
        # Set the new size
        self.resize(int(new_width), int(new_height)) 
                                  
        # Main layout setup
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Setup columns
        self.setupLeftColumn(main_layout)
        self.setupCentralColumn(main_layout)
        self.setupRightColumn(main_layout)
        
    
                    
    def setupLeftColumn(self, layout):
        left_column_layout = QVBoxLayout()
        layout.addLayout(left_column_layout)
        
        preprocessed_input_layout = QHBoxLayout()  # Horizontal layout to contain the label and the help icon
        preprocessed_input_label = QLabel("Preprocessed Input:")
        preprocessed_input_layout.addWidget(preprocessed_input_label)
        
        # Assuming HELP_EXPLANATIONS["Preprocessed Input"] exists
        preprocessed_help_icon = create_help_icon(HELP_EXPLANATIONS["Preprocessed Input"])
        preprocessed_input_layout.addWidget(preprocessed_help_icon)
        preprocessed_input_layout.addStretch()
        
        left_column_layout.addLayout(preprocessed_input_layout)
        
        # Tab widget for Preprocessed Inputs
        self.preprocessed_inputs_tabs = QTabWidget()
        self.preprocessed_inputs_tabs.setTabsClosable(True)
        self.preprocessed_inputs_tabs.tabCloseRequested.connect(self.closePreprocessedInputTab)
        
        # Add the Preprocessed Inputs Tab Widget to the left column layout
        left_column_layout.addWidget(self.preprocessed_inputs_tabs)
        
        # Create the first tab for Preprocessed Input
        self.addNewPreprocessedInputTab("Preprocessed Input")
        
        processed_input_layout = QHBoxLayout()  # Similar setup for processed input
        processed_input_label = QLabel("Processed Inputs:")
        processed_input_layout.addWidget(processed_input_label)
        
        # Assuming HELP_EXPLANATIONS["Processed Input"] exists
        processed_help_icon = create_help_icon(HELP_EXPLANATIONS["Processed Input"])
        processed_input_layout.addWidget(processed_help_icon)
        processed_input_layout.addStretch()
        
        left_column_layout.addLayout(processed_input_layout)
        
        # Tab widget for Processed Inputs
        self.processed_inputs_tabs = QTabWidget()
        self.processed_inputs_tabs.setTabsClosable(True)
        self.processed_inputs_tabs.tabCloseRequested.connect(self.closeProcessedInputTab)
        
        # Add the Processed Inputs Tab Widget to the left column layout
        left_column_layout.addWidget(self.processed_inputs_tabs)
        
        # Create the first tab for Processed Input
        self.addNewProcessedInputTab("Processed Input")

    def addNewPreprocessedInputTab(self, tabName):
        tab_content_widget = QWidget()
        tab_layout = QVBoxLayout(tab_content_widget)
        preprocessed_input_text = QTextEdit()
        tab_layout.addWidget(preprocessed_input_text)
        self.preprocessed_inputs_tabs.addTab(tab_content_widget, tabName)

    def addNewProcessedInputTab(self, tabName):
        tab_content_widget = QWidget()
        tab_layout = QVBoxLayout(tab_content_widget)
        processed_input_text = QTextEdit()
        tab_layout.addWidget(processed_input_text)
        self.processed_inputs_tabs.addTab(tab_content_widget, tabName)
        return processed_input_text  # Make sure this line exists and works as expected


    def closePreprocessedInputTab(self, index):
        self.preprocessed_inputs_tabs.removeTab(index)

    def closeProcessedInputTab(self, index):
        self.processed_inputs_tabs.removeTab(index)

    def onPreprocessClicked(self):
        if self.preprocessed_inputs_tabs.count() > 0:
            current_preprocessed_tab_index = self.preprocessed_inputs_tabs.currentIndex()
            current_preprocessed_tab_widget = self.preprocessed_inputs_tabs.currentWidget()
            # Retrieve the QTextEdit from the current tab's layout
            text_edit = current_preprocessed_tab_widget.findChild(QTextEdit)
            text = text_edit.toPlainText()

            processed_text = self.controller.preprocess_text(text)

            preprocessed_tab_name = self.preprocessed_inputs_tabs.tabText(current_preprocessed_tab_index)
            processed_tab_name = f"Processed {preprocessed_tab_name}"

            if self.processed_inputs_tabs.count() <= current_preprocessed_tab_index:
                # If a corresponding processed input tab doesn't exist, create a new one
                processed_text_edit = self.addNewProcessedInputTab(processed_tab_name)
            else:
                # If the corresponding processed input tab exists, retrieve the QTextEdit from it
                processed_tab_widget = self.processed_inputs_tabs.widget(current_preprocessed_tab_index)
                processed_text_edit = processed_tab_widget.findChild(QTextEdit)
            
            # Set the processed text in the QTextEdit of the processed input tab
            processed_text_edit.setText(processed_text)


        
    def setupCentralColumn(self, layout):
        central_column_layout = QVBoxLayout()
        layout.addLayout(central_column_layout)
        
        # Preprocess Button
        preprocess_layout = QHBoxLayout()
        self.preprocess_button = QPushButton("Preprocess")
        self.preprocess_button.setStyleSheet(style_sheets.preprocess_button_style_sheet)
       
        self.preprocess_button.setIcon(QIcon('resources/icons/broom-code.png'))
        self.preprocess_button.clicked.connect(self.onPreprocessClicked)
        preprocess_layout.addWidget(self.preprocess_button)  # Add the preprocess button to the horizontal layout

        # Create and add the help icon to the preprocess_layout
        preprocess_help_icon = create_help_icon(HELP_EXPLANATIONS["Preprocess"])
        preprocess_layout.addWidget(preprocess_help_icon)
        central_column_layout.addWidget(self.preprocess_button)
        
        # Technique Selection
        self.technique_label = QLabel("Technique:")
        self.technique_combo_box = ToolTipComboBox(self)
        techniques = ["Select", "Readability_Score", "POS_Tagging", "POS_Chunking", "Bi-grams", "Tri-grams", "Co-occurrence_Matrix", "NER"]
        self.technique_combo_box.addItems(techniques)
        self.technique_combo_box.currentTextChanged.connect(self.onTechniqueSelected)
        
        
        technique_tooltips = {
        "Select": "Select an Natural Language Processing technique to apply.",
        "Readability_Score": "Assesses text difficulty to ensure it matches the target audience's comprehension level, enhancing overall communication impact",
        "POS_Tagging": "Visualize words by their grammar roles, like verbs and nouns, using colors. This makes it easier to see and understand sentence patterns and structure." ,
        "POS_Chunking": "Insightful phrase detection" ,
        "Bi-grams":"Identifies common word pairs, providing insights into language use and content themes.", 
        "Tri-grams": "Frequent three-word pairings, offering deeper understanding of common phrases and context within the text",
        "Co-occurrence_Matrix": "Structured way to analyze the relationships that words form within the text",
        "NER": "Highlights valuable information into predefined categories, such as the names of people, organizations, locations, expressions of times, etc."         
        }
        
        for index, technique in enumerate(techniques):
            tooltip = technique_tooltips.get(technique, "")
            self.technique_combo_box.setItemToolTip(index, tooltip)
        
        central_column_layout.addWidget(self.technique_label)
        central_column_layout.addWidget(self.technique_combo_box)
        
        ## Analysis Button ##
        self.analysis_button = QPushButton("Analyze")

        self.analysis_button.setStyleSheet(style_sheets.analysis_button_style_sheet)
        self.analysis_button.setIcon(QIcon('resources/icons/auction-hammer.png'))
        self.analysis_button.clicked.connect(self.onAnalyzeClicked)
        central_column_layout.addWidget(self.analysis_button)
        
        # Stop Words Input
        self.setupStopWordsInput(central_column_layout)
        
        # Key Words Input
        self.setupKeyWordsInput(central_column_layout)
                 
    def addWelcomeTab(self):
        welcome_text_browser = QTextBrowser()
        welcome_text_browser.setHtml(welcome_html_content)
        welcome_text_browser.setReadOnly(True)
        self.addAnalysisTab("Welcome", welcome_text_browser)
        
        
    def addFAQTab(self):
        faq_text_browser = QTextBrowser()
        faq_text_browser.setOpenExternalLinks(False)  # Prevent automatic link opening
        faq_text_browser.setHtml(faq_html_content)
        faq_text_browser.anchorClicked.connect(self.handleLinkClick) # Connect to the slot
        faq_text_browser.setReadOnly(True)
        self.addAnalysisTab("FAQ / Getting Started", faq_text_browser)
        
    def handleLinkClick(self, url: QUrl):

        # Handling the custom action to open the Glossary tab
        if url.fragment() == "open_glossary":            
            self.addGlossaryTab()
        else:
            print("URL did not match expected actions.")

    def addGlossaryTab(self):
        glossary_web_view = QWebEngineView()
        glossary_web_view.setHtml(glossary_html_content)
        self.addAnalysisTab("Glossary", glossary_web_view)        
                    
                
    def setupRightColumn(self, layout):
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)  # Enable the close button on each tab
        self.tabs.tabCloseRequested.connect(self.closeTab)  # Connect the signal to the slot
        layout.addWidget(self.tabs)
        self.addWelcomeTab()
        self.addFAQTab() 

    def closeTab(self, index):
        self.tabs.removeTab(index)  # Close the tab at the given index
        
    def addAnalysisTab(self, tabName, tabContent, isHtml=False):
        # Check if tabContent is already a QWidget (e.g., QWebEngineView)
        if isinstance(tabContent, QWidget):
            # Directly use the widget as the tab
            tab = tabContent
        else:
            # Create a new QWidget and layout for non-widget content
            tab = QWidget()
            tabLayout = QVBoxLayout(tab)
            
            # Create a QTextEdit widget for displaying text or HTML content
            textWidget = QTextEdit()
            textWidget.setReadOnly(True)  # Make the QTextEdit read-only
            
            # Decide between setting HTML or plain text based on isHtml flag
            if isHtml:
                textWidget.setHtml(tabContent)  # Set HTML content if isHtml is True
            else:
                textWidget.setText(tabContent)  # Set plain text otherwise
            
            # Add the QTextEdit to the tab's layout
            tabLayout.addWidget(textWidget)
        
        # Add the tab to the tab widget with the specified tab name
        self.tabs.addTab(tab, tabName)

        
    def addGraphTab(self, title, plot_function, *args, **kwargs):
        canvas = MplCanvas(width=5, height=4, dpi=100)
        plot_function(canvas.axes, *args, **kwargs)
        tabIndex = self.tabs.addTab(canvas, title)
        self.tabs.setCurrentIndex(tabIndex)
    
    
    def onTechniqueSelected(self):
        # Placeholder for future functionality
        pass
       
    
    def onAnalyzeClicked(self):
        selectedTechnique = self.technique_combo_box.currentText()
        if selectedTechnique == "Bi-grams":
            self.performNGramAnalysis(n=2)
        elif selectedTechnique == "Tri-grams":
            self.performNGramAnalysis(n=3)
        elif selectedTechnique == "NER":
            self.performNerAnalysis()
        elif selectedTechnique == "POS_Tagging":
            self.performPOS_Tagging()
        elif selectedTechnique == "POS_Chunking":
            self.performPOSChunkingAnalysis()
        elif selectedTechnique == "Readability_Score":
            self.performReadabilityAnalysis()
        elif selectedTechnique == "Co-occurrence_Matrix":
            self.performCooccurrenceMatrixAnalysis()

    
    def plot_ngrams(self, ax, ngrams_data):
        ngrams, frequencies = zip(*ngrams_data)
        ngrams = [' '.join(gram) for gram in ngrams]
        ax.bar(ngrams, frequencies)
        ax.set_xlabel('N-grams')
        ax.set_ylabel('Frequency')
        ax.set_title('Top N-grams')
        ax.tick_params(axis='x', rotation=45)
    
    def performNGramAnalysis(self, n=2):
        if self.processed_inputs_tabs.count() > 0:
            current_tab_widget = self.processed_inputs_tabs.currentWidget()
            input_text_edit = current_tab_widget.findChild(QTextEdit)
            processed_text = input_text_edit.toPlainText()

            top_ngrams = self.controller.perform_ngram_analysis(processed_text, n=n, top=10)
            results_text = "\n".join([f"{' '.join(gram)}: {freq}" for gram, freq in top_ngrams])
            tabName = "Bi-gram Results" if n == 2 else "Tri-gram Results"
            self.addAnalysisTab(tabName, results_text)
            self.addGraphTab(tabName, self.plot_ngrams, top_ngrams)

        
               
    def performNerAnalysis(self):
        if self.processed_inputs_tabs.count() > 0:
            current_tab_widget = self.processed_inputs_tabs.currentWidget()
            input_text_edit = current_tab_widget.findChild(QTextEdit)
            processed_text = input_text_edit.toPlainText()

            ner_entities = self.controller.perform_ner_analysis(processed_text)

            # Prepare the table widget
            table_widget = QTableWidget()
            table_widget.setRowCount(len(ner_entities))
            table_widget.setColumnCount(3)  # For Entity, Label, Frequency
            table_widget.setHorizontalHeaderLabels(['Index', 'Entity', 'Label', 'Frequency'])
            table_widget.setSortingEnabled(True)

            # Count the frequency of each entity
            entity_frequency = {}
            for entity, label in ner_entities:
                key = (entity, label)
                if key not in entity_frequency:
                    entity_frequency[key] = 0
                entity_frequency[key] += 1

            # Populate the table
            for row, ((entity, label), frequency) in enumerate(entity_frequency.items()):
                table_widget.setItem(row, 0, QTableWidgetItem(str(row)))
                table_widget.setItem(row, 1, QTableWidgetItem(entity))
                table_widget.setItem(row, 2, QTableWidgetItem(label))
                table_widget.setItem(row, 3, QTableWidgetItem(str(frequency)))

            # Adjust column widths to content
            table_widget.resizeColumnsToContents()

            # Create a new widget to hold the table and set it as the layout
            tab_content_widget = QWidget()
            layout = QVBoxLayout(tab_content_widget)
            layout.addWidget(table_widget)

            self.addAnalysisTab("NER Results", tab_content_widget)


    def performPOS_Tagging(self):
        if self.processed_inputs_tabs.count() > 0:
            current_tab_widget = self.processed_inputs_tabs.currentWidget()
            input_text_edit = current_tab_widget.findChild(QTextEdit)
            processed_text = input_text_edit.toPlainText()

            html_content = self.controller.tag_and_color_text_to_html(processed_text)

            pos_tagging_web_view = QWebEngineView()
            pos_tagging_web_view.setHtml(html_content)

            channel = QWebChannel(pos_tagging_web_view.page())
            sentiment_handler = SentimentAnalysisHandler()  # Ensure this is correctly implemented or available
            channel.registerObject("sentimentAnalysis", sentiment_handler)
            pos_tagging_web_view.page().setWebChannel(channel)

            self.addAnalysisTab("POS Tagging Results", pos_tagging_web_view)

            
                
    def performPOSChunkingAnalysis(self):
        if self.processed_inputs_tabs.count() > 0:
            current_tab_widget = self.processed_inputs_tabs.currentWidget()
            # Assuming the first child widget added to current_tab_widget is the QTextEdit you're interested in
            input_text_edit = current_tab_widget.findChild(QTextEdit)
            input_text = input_text_edit.toPlainText()

            chunk_dfs_html = self.controller.perform_pos_chunking(input_text)

            for chunk_type, html_content in chunk_dfs_html.items():
                webEngineView = QWebEngineView()
                webEngineView.setHtml(html_content)
                self.addAnalysisTab(chunk_type, webEngineView, isHtml=True)

            
            
    def performCooccurrenceMatrixAnalysis(self):
            # Example pseudocode
            processed_text = self.processed_input_text.toPlainText()
            cooccurrence_matrix, vocab = self.controller.create_text_cooccurrence_matrix(processed_text)
            self.addGraphTab("Co-occurrence Matrix", self.plot_cooccurrence_matrix, cooccurrence_matrix, vocab)

    def plot_cooccurrence_matrix(self, axes, cooccurrence_matrix, vocab):
        import seaborn as sns
        # Use seaborn's heatmap function to plot the co-occurrence matrix
        sns.heatmap(cooccurrence_matrix, ax=axes, cmap='viridis', xticklabels=vocab, yticklabels=vocab)
        axes.set_xticklabels(axes.get_xticklabels(), rotation=45, ha='right')
        axes.set_yticklabels(axes.get_yticklabels(), rotation=45)
        axes.set_title('Co-occurrence Matrix')


    def performReadabilityAnalysis(self):
        if self.processed_inputs_tabs.count() > 0:
            current_tab_widget = self.processed_inputs_tabs.currentWidget()
            input_text_edit = current_tab_widget.findChild(QTextEdit)
            processed_text = input_text_edit.toPlainText()

            readability_scores = self.controller.calculate_readability_score(processed_text)
            scores_text = (
                f"Flesch Reading Ease: {readability_scores['flesch_reading_ease']}\n"
                "Indicates how easy it is to understand the text. It is based on the length of sentences and the number of syllables per word. Scores range from 0 to 100, with higher scores indicating easier readability. Typically, scores between 60 to 70 are considered acceptable for a wide audience.\n"
                "Real-World Implications: This metric is widely used in various fields, such as journalism, marketing, and web content creation, to ensure that the text is accessible to the intended audience.\n\n"
                
                f"Flesch Kincaid Grade: {readability_scores['flesch_kincaid_grade']}\n"
                "Corresponds to U.S. grade levels needed to understand the text. It takes into account sentence length and word syllable count. Lower grades indicate easier readability.\n"
                "Real-World Implications: This metric is commonly used in education to ensure that learning materials are suitable for the intended grade level. It helps teachers and textbook authors adjust the complexity of the text to match the students' reading comprehension abilities.\n\n"
                
                f"Dale Chall Readability Score: {readability_scores['dale_chall_readability_score']}\n"
                "This score uses a list of approximately 3000 words that fourth-grade American students can reliably understand. If the text contains words not on that list, it is considered more challenging to read. This score also factors in sentence length.\n"
                "Real-World Implications: This metric is particularly useful for assessing the readability of content for a general audience, such as patient education materials, public notices, and government publications. It helps ensure that the text is accessible to a wide range of readers.\n\n"
                
                f"Gunning Fog: {readability_scores['gunning_fog']}\n"
                "Estimates the years of formal education needed to understand a text on the first reading.\n"
                "Real-World Implications: This metric is widely used in various fields, such as journalism, business writing, and technical documentation, to ensure that the text is comprehensible to the target audience. It helps writers adjust the complexity of their writing based on the expected education level of their readers.\n\n"
            )
            self.addAnalysisTab("Readability Scores", scores_text)
           
    ### Stop Words ###        
    def setupStopWordsInput(self, layout):
        # Horizontal layout for the Stop Words label and help icon
        stop_words_label_layout = QHBoxLayout()
        stop_words_label_layout.setSpacing(0)  # Remove spacing between elements
        stop_words_label = QLabel("Stop Words:")
        stop_words_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)  # Prevent the label from expanding unnecessarily
        stop_words_help_icon = create_help_icon(HELP_EXPLANATIONS["Stop Words"])
        stop_words_help_icon.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Fixed size policy for the icon
        # Add widgets to the horizontal layout with zero margins
        stop_words_label_layout.addWidget(stop_words_label)
        stop_words_label_layout.addWidget(stop_words_help_icon)
        stop_words_label_layout.addStretch()  # This will push the label and icon to the left
        # Now add the horizontal layout for the label and icon to the main layout
        layout.addLayout(stop_words_label_layout)
        # Continue with the rest of the setup for stop words input
        self.stop_words_display = QTextEdit("Current Stop Words:\n" + "\n".join(sorted(self.controller.stop_words)))
        self.stop_words_display.setReadOnly(True)
        layout.addWidget(self.stop_words_display)
        self.stop_words_edit = QLineEdit()        
        # Layout for add and remove buttons
        stop_words_buttons_layout = QHBoxLayout()        
        # Stop Words Add Button
        self.stop_words_add_button = QPushButton("Add")
        self.stop_words_add_button.setStyleSheet(style_sheets.stop_words_add_button_style_sheet)   
             
        # Stop Words Remove Button
        self.stop_words_remove_button = QPushButton("Remove")
        self.stop_words_remove_button.setStyleSheet(style_sheets.stop_words_remove_button_style_sheet)
        stop_words_buttons_layout.addWidget(self.stop_words_edit)
        stop_words_buttons_layout.addWidget(self.stop_words_add_button)
        stop_words_buttons_layout.addWidget(self.stop_words_remove_button)
        layout.addLayout(stop_words_buttons_layout)
        
        self.stop_words_checkbox = QCheckBox("Use Stop Words")
        self.stop_words_checkbox.setChecked(True)
        layout.addWidget(self.stop_words_checkbox)        
        # Connect buttons to their respective slot functions
        self.stop_words_add_button.clicked.connect(self.onAddStopWordClicked)
        self.stop_words_remove_button.clicked.connect(self.onRemoveStopWordClicked)
        self.stop_words_checkbox.stateChanged.connect(self.onToggleUseStopWords)
    # Add a slot function for remove button click event
    def onRemoveStopWordClicked(self):
        word = self.stop_words_edit.text().strip()
        if word:
            self.controller.remove_stop_word(word)
            self.updateStopWordsDisplay()
            self.stop_words_edit.clear()
            
    def manageStopWords(self):
        # Open ListSelectionDialog for selecting a stop words list
        dialog = ListSelectionDialog(listType="StopWords", parent=self)
        dialog.listSelected.connect(self.openListManagementDialog)
        dialog.exec()

            
    ### Key Words ###
    def setupKeyWordsInput(self, layout):
        # Create a horizontal layout for the Key Words label and its help icon
        key_words_label_layout = QHBoxLayout()
        key_words_label_layout.setSpacing(0) 
        key_words_label = QLabel("Key Words:")
        key_words_label_layout.addWidget(key_words_label)
        key_words_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)  # Prevent the label from expanding unnecessarily        
        # Create and add the help icon for Key Words
        key_words_help_icon = create_help_icon(HELP_EXPLANATIONS["Key Words"])
        key_words_help_icon.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Fixed size policy for the icon
        key_words_label_layout.addWidget(key_words_help_icon)
        key_words_label_layout.addStretch()  # Push everything to the left
        # Add the horizontal layout to the main layout
        layout.addLayout(key_words_label_layout)        
        self.key_words_display = QTextEdit("Current Key Words:\n" + "\n".join(sorted(self.controller.key_words_list)))
        self.key_words_display.setReadOnly(True)
        layout.addWidget(self.key_words_display)        
        self.key_words_edit = QLineEdit()
        
        # Layout for add and remove buttons
        key_words_buttons_layout = QHBoxLayout()
        
        # Key Words Add Button
        self.key_words_add_button = QPushButton("Add")
        self.key_words_add_button.setStyleSheet(style_sheets.key_words_add_button_style_sheet)
        
        # Key Words Remove Button
        self.key_words_remove_button = QPushButton("Remove")
        self.key_words_remove_button.setStyleSheet(style_sheets.key_words_remove_button_style_sheet)
        
        key_words_buttons_layout.addWidget(self.key_words_edit)
        key_words_buttons_layout.addWidget(self.key_words_add_button)
        key_words_buttons_layout.addWidget(self.key_words_remove_button)
        layout.addLayout(key_words_buttons_layout)
        
        self.key_words_checkbox = QCheckBox("Use Key Words")
        self.key_words_checkbox.setChecked(False)
        layout.addWidget(self.key_words_checkbox)
        
        # Connect buttons to their respective slot functions
        self.key_words_add_button.clicked.connect(self.onAddKeyWordClicked)
        self.key_words_remove_button.clicked.connect(self.onRemoveKeyWordClicked)
        self.key_words_checkbox.stateChanged.connect(self.onToggleUseKeyWords)

    def onRemoveKeyWordClicked(self):
        word = self.key_words_edit.text().strip()
        if word:
            self.controller.remove_key_word(word)
            self.updateKeyWordsDisplay()
            self.key_words_edit.clear()
            
    def manageKeyWords(self):
        # This method should contain the logic to manage key words.
        print("Manage Key Words clicked")
        # Similar to manageStopWords, implement the logic to manage key words.
        # This could involve opening a dialog for adding/removing key words.            
      
    
    def onAddStopWordClicked(self):
        word = self.stop_words_edit.text().strip()
        if word:
            self.controller.add_stop_word(word)
            self.updateStopWordsDisplay()
            self.stop_words_edit.clear()
            
      
    def onAddKeyWordClicked(self):
        word = self.key_words_edit.text().strip()
        if word:
            self.controller.add_key_word(word)
            self.updateKeyWordsDisplay()
            self.key_words_edit.clear()
    
    def onToggleUseStopWords(self, _):
        current_state = self.stop_words_checkbox.isChecked()
        print(f"UI File: Toggling stop words to: {'ON' if current_state else 'OFF'}")
        self.controller.toggle_use_stop_words(current_state)
    
    def onToggleUseKeyWords(self, _):
        current_state = self.key_words_checkbox.isChecked()
        print(f"UI File: Toggling key words to: {'ON' if current_state else 'OFF'}")
        self.controller.toggle_use_key_words(current_state)
    
    def updateStopWordsDisplay(self):
        self.stop_words_display.setText("Current Stop Words:\n" + "\n".join(sorted(self.controller.stop_words)))
    
    def updateKeyWordsDisplay(self):
        self.key_words_display.setText("Current Key Words:\n" + "\n".join(sorted(self.controller.key_words_list)))
        
    def manageCustomLists(self):
        dialog = ListSelectionDialog(listType="Custom List", parent=self)
        dialog.listSelected.connect(self.handleListSelection)
        dialog.exec()
    
    def createMenus(self):
        menuBar = self.menuBar()
        self.fileMenu = menuBar.addMenu('File')  # Save as an attribute of the class
                
        openAction = QAction(QIcon('resources/icons/document--plus.png'), 'Open...', self)
        openAction.triggered.connect(self.openFile)
        self.fileMenu.addAction(openAction)
        
        saveAction = QAction(QIcon('resources/icons/disk--plus.png'), 'Save As...', self)
        saveAction.triggered.connect(self.saveFile)
        self.fileMenu.addAction(saveAction)
        
        exitAction = QAction(QIcon('resources/icons/door-open-out.png'), 'Exit', self)
        exitAction.triggered.connect(self.close)
        self.fileMenu.addAction(exitAction)
        
        helpMenu = menuBar.addMenu('Help')
        aboutAction = QAction(QIcon('resources/icons/book-question.png'), 'About', self)
        aboutAction.triggered.connect(self.showAboutDialog)
        helpMenu.addAction(aboutAction)
        
        # Move the creation of the "Import PDF" action inside this method
        import_pdf_action = QAction(QIcon('resources/icons/document-office.png'), "Import PDF", self)
        import_pdf_action.triggered.connect(self.import_pdf)
        self.fileMenu.addAction(import_pdf_action)  # Correctly reference the attribute

        listsMenu = menuBar.addMenu('Lists')
        
        stopWordsAction = QAction('Stop Words', self)
        stopWordsAction.triggered.connect(lambda: self.openListDialog('Stop Words'))
        listsMenu.addAction(stopWordsAction)

        keyWordsAction = QAction('Key Words', self)
        keyWordsAction.triggered.connect(lambda: self.openListDialog('Key Words'))
        listsMenu.addAction(keyWordsAction)

        customListsAction = QAction('Custom Lists', self)
        customListsAction.triggered.connect(lambda: self.openListDialog('Custom List'))
        listsMenu.addAction(customListsAction)

    def openListDialog(self, listType):
        if listType == 'Stop Words':
            self.manageStopWords()
        elif listType == 'Key Words':
            self.manageKeyWords()
        elif listType == 'Custom List':
            self.manageCustomLists()
        else:
            print(f"Unknown list type: {listType}")

            
    def openListSelectionDialog(self, listType):
        selectionDialog = ListSelectionDialog(listType, self)
        selectionDialog.listSelected.connect(self.handleListSelection)
        selectionDialog.exec()
        
    def handleListSelection(self, listType, selection):
        if listType == 'Stop Words':
            filePath = f"resources/lists/Filter/{selection}"
            self.openListManagementDialog(f"Manage Stop Words: {selection}", filePath)
        elif listType == 'Key Words':
            self.openKeywordListSelection(selection)
        elif listType == 'Custom List':
            custom_dir = 'resources/lists/Custom'
            if selection == 'Create New...':
                name, ok = QInputDialog.getText(self, 'New Custom List', 'List name:')
                if not ok or not name:
                    return
                if not name.endswith('.txt'):
                    name += '.txt'
                filePath = os.path.join(custom_dir, name)
                os.makedirs(custom_dir, exist_ok=True)
                open(filePath, 'a').close()
                self.openListManagementDialog(f"Manage Custom List: {name}", filePath)
            else:
                filePath = os.path.join(custom_dir, selection)
                self.openListManagementDialog(f"Manage Custom List: {selection}", filePath)

    def openKeywordListSelection(self, category):
        # This function would open another dialog to select a specific list within the chosen category
        # You would list files within the selected 'category' directory here
        directoryPath = f"resources/lists/Key/{category.replace(' ', '/')}"
        files = [f for f in os.listdir(directoryPath) if os.path.isfile(os.path.join(directoryPath, f))]
        fileSelectionDialog = ListSelectionDialog('Select File', self)  # Use a modified or different dialog for this
        fileSelectionDialog.listTypeComboBox.clear()  # Clear previous items if any
        fileSelectionDialog.listTypeComboBox.addItems(["Select File"] + files)
        fileSelectionDialog.listSelected.connect(lambda _, file: self.openListManagementDialog(f"Manage Key Words: {file}", os.path.join(directoryPath, file)))
        fileSelectionDialog.exec()

    def openListManagementDialog(self, title, filePath):
        dialog = ListManagementDialog(title, filePath, self)
        if dialog.exec():
            useListDecisionDialog = UseListDecisionDialog(self)
            decision = useListDecisionDialog.exec()

            if decision == 1:  # Use for Stop Words
                self.applyList(filePath, applyTo='stop_words')
            elif decision == 2:  # Use for Key Words
                self.applyList(filePath, applyTo='key_words_list')

    def applyList(self, filePath, applyTo):
        # Read list items from the selected file
        with open(filePath, "r") as file:
            listItems = [line.strip() for line in file if line.strip()]

        # Prompt for action: Append or Replace
        actionDialog = QMessageBox(self)
        actionDialog.setWindowTitle("Apply List")
        actionDialog.setText("Do you want to append to or replace the current list?")
        appendBtn = actionDialog.addButton("Append", QMessageBox.AcceptRole)
        replaceBtn = actionDialog.addButton("Replace", QMessageBox.DestructiveRole)
        actionDialog.addButton("Cancel", QMessageBox.RejectRole)
        actionDialog.exec()

        response = actionDialog.clickedButton()
        if response == appendBtn:
            # Append selected list to the existing one
            if applyTo == 'stop_words':
                updatedList = sorted(set(self.controller.stop_words + listItems))
                self.controller.stop_words = updatedList
                self.updateStopWordsDisplay()
            elif applyTo == 'key_words_list':
                updatedList = sorted(set(self.controller.key_words_list + listItems))
                self.controller.key_words_list = updatedList
                self.updateKeyWordsDisplay()
        elif response == replaceBtn:
            # Replace the existing list with the selected one
            if applyTo == 'stop_words':
                self.controller.stop_words = listItems
                self.updateStopWordsDisplay()
            elif applyTo == 'key_words_list':
                self.controller.key_words_list = listItems
                self.updateKeyWordsDisplay()

    def manageList(self, listType, selectedList):
        if listType == 'Key Words':
            listPath = f"resources/lists/Key/{selectedList.replace(' ', '/')}.txt"
        elif listType == 'Custom List':
            listPath = f"resources/lists/Custom/{selectedList}.txt"
        
        dialog = ListManagementDialog(f"Manage {listType}: {selectedList}", listPath, self)
        dialog.exec()
    

    def import_pdf(self):
        # Open a file dialog to select the PDF
        pdf_path, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF files (*.pdf)")
        if pdf_path:
            text = self.extract_text_from_pdf(pdf_path)
            # Assuming you have a method to set the text in your preprocessing input section
            self.preprocessed_input_text.setText(text)
        
    def extract_text_from_pdf(self, pdf_path):
        document = fitz.open(pdf_path)
        text = ""

        for page_num in range(len(document)):
            page = document[page_num]
            page_text = page.get_text().strip()

            # If the extracted text is very short, it might be a scanned page.
            # You can adjust the length threshold as needed.
            if len(page_text) < 50:
                # Attempt OCR on the page image
                pix = page.get_pixmap()
                img_bytes = pix.tobytes("ppm")
                img = Image.open(io.BytesIO(img_bytes))
                page_text = pytesseract.image_to_string(img)

            text += page_text + "\n"

        document.close()
        return text   
    
        
    def openFile(self):
        filePaths, _ = QFileDialog.getOpenFileNames(self, "Open Text Files", "", "Text Files (*.txt);;All Files (*)")
        if not filePaths:
            return  # User cancelled or no selection
        
        reply = QMessageBox.question(
            self, "Document Compilation",
            "Do you want to compile all selected documents into one?",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )
        
        if reply == QMessageBox.Cancel:
            return  # User cancelled the action
        elif reply == QMessageBox.Yes:
            self.compileDocumentsIntoOne(filePaths)
        else:
            self.openDocumentsSeparately(filePaths)

    def compileDocumentsIntoOne(self, filePaths):
        combined_text = ""
        for filePath in filePaths:
            with open(filePath, 'r', encoding='utf-8') as file:
                combined_text += file.read() + "\n"
        
        # Check if there's already a tab for combined documents, or create a new one
        if self.preprocessed_inputs_tabs.count() == 0:
            # If no tabs exist, create a new one for the combined documents
            self.addNewPreprocessedInputTab("Combined Documents")
        
        # Assuming the combined documents always go into the first tab
        tab_widget = self.preprocessed_inputs_tabs.widget(0)
        tab_layout = tab_widget.layout()
        preprocessed_input_text = tab_layout.itemAt(0).widget()
        preprocessed_input_text.setText(combined_text)

    
    def openDocumentsSeparately(self, filePaths):
        for filePath in filePaths:
            tab_content_widget = QWidget()  # Create a container widget for the tab
            tab_layout = QVBoxLayout(tab_content_widget)  # Create a layout for the container
            
            with open(filePath, 'r', encoding='utf-8') as file:
                document_text = file.read()
                textWidget = QTextEdit()
                textWidget.setText(document_text)
                textWidget.setReadOnly(True)  # Optional based on your needs

            tab_layout.addWidget(textWidget)  # Add the QTextEdit to the layout
            self.preprocessed_inputs_tabs.addTab(tab_content_widget, os.path.basename(filePath))  # Add the container widget as the tab


        
    def saveFile(self):
        dirPath = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dirPath:
            try:
                # Save Preprocessed and Processed Text as .txt files
                self._save_text(self.preprocessed_input_text.toPlainText(), 'preprocessed_text.txt', dirPath)
                self._save_text(self.processed_input_text.toPlainText(), 'processed_text.txt', dirPath)
                
                # Iterate through tabs to save their contents based on type
                for i in range(self.tabs.count()):
                    tabName = self.tabs.tabText(i).replace(" ", "_")
                    tabWidget = self.tabs.widget(i)

                    if isinstance(tabWidget, FigureCanvas) or "POS_Tagging" in tabName:
                        figure = tabWidget.figure
                        figure.savefig(os.path.join(dirPath, f'{tabName}.png'))
                    elif isinstance(tabWidget, QTextEdit):
                        self._save_text(tabWidget.toPlainText(), f'{tabName}.csv', dirPath)
                    else:
                        # Handle generic QWidget cases
                        self._handle_generic_widget(tabWidget, tabName, dirPath)
            except Exception as e:
                QMessageBox.critical(self, "Error Saving Files", f"An error occurred: {str(e)}")

    def _save_text(self, content, filename, dirPath):
        filePath = os.path.join(dirPath, filename)
        with open(filePath, 'w', encoding='utf-8') as file:
            file.write(content)

    def _handle_generic_widget(self, widget, tabName, dirPath):
        # Attempt to find a QTextEdit or similar text-containing widget within the generic QWidget
        if hasattr(widget, 'findChildren'):
            textWidgets = widget.findChildren(QTextEdit)
            if textWidgets:
                # Assuming we want to save the content of the first found QTextEdit
                content = textWidgets[0].toPlainText()
                filename = f'{tabName}.csv'  # Defaulting to .csv for textual content
                self._save_text(content, filename, dirPath)
                return
        # Fallback or additional logic for other widget types
        QMessageBox.warning(self, "Unsupported Content", f"Could not extract content for saving from tab '{tabName}'.")
    def showAboutDialog(self):
        QMessageBox.about(self, "About Book Worm NLP", "Comprehensive NLP GUI Toolkit version 1.0\nAuthor: Lucas Pearson")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = NLPToolkitController()  # Ensure you have an instance of your controller here
    window = NLPToolkitUI(controller)
    window.show()
    sys.exit(app.exec())
    
