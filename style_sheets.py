#style_sheets.py

## Preprocess Button ##
### Duplicate styling of Analysis Button ### 
preprocess_button_style_sheet = """
QPushButton {
    background-color: #4CAF50; /* Green */
    color: white;
    border-radius: 10px;
    padding: 8px 20px;
    margin: 10px 5px;
    font-size: 14px;
    font-weight: bold;
    border: 2px solid #397D49; /* Darker green border */
    font-family: 'Arial', sans-serif;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4CAF50, stop:1 #397D49); /* Gradient from lighter to darker green */
}
QPushButton:hover {
    background-color: #5CD65C; /* Lighter green for hover */
    border: 2px solid #4CAF50;
}
QPushButton:pressed {
    background-color: #397D49; /* Even darker green for pressed */
}
"""


## Analysis Button ##
### Duplicate styling of Preprocess Button ###  
analysis_button_style_sheet = """
QPushButton {
    background-color: #4CAF50; /* Green */
    color: white;
    border-radius: 10px;
    padding: 8px 20px;
    margin: 10px 5px;
    font-size: 14px;
    font-weight: bold;
    border: 2px solid #397D49; /* Darker green border */
    font-family: 'Arial', sans-serif;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4CAF50, stop:1 #397D49); /* Gradient from lighter to darker green */
}
QPushButton:hover {
    background-color: #5CD65C; /* Lighter green for hover */
    border: 2px solid #4CAF50;
}
QPushButton:pressed {
    background-color: #397D49; /* Even darker green for pressed */
}
"""



## Stop Words ADD Button ##
### Duplicates with Keywords ADD Button ###
stop_words_add_button_style_sheet = """
        QPushButton {
            background-color: #4CAF50; /* Green */
            color: white;
            border-radius: 5px;
            padding: 4px 10px;
            max-width: 100px;
            min-width: 80px;
            text-align: center;
            margin-left: 0px;
            font-size: 12px;
            font-weight: bold;       
            border: 1px solid #397D49; /* Darker green border */  
            font-family: 'Arial', sans-serif;    
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4CAF50, stop:1 #397D49); /* Gradient from lighter to darker green */
        }
        QPushButton:hover {
            background-color: #5CD65C; /* Lighter green for hover */
            border: 2px solid #4CAF50;
        }
        QPushButton:pressed {
            background-color: #397D49; /* Even darker green for pressed */  
        }
        """

## Key Words ADD Button ##
### Duplicates with Stop Words ADD Button ###
key_words_add_button_style_sheet = """
        QPushButton {
            background-color: #4CAF50; /* Green */
            color: white;
            border-radius: 5px;
            padding: 4px 10px;
            max-width: 100px;
            min-width: 80px;
            text-align: center;
            margin-left: 0px;
            font-size: 12px;
            font-weight: bold;       
            border: 1px solid #397D49; /* Darker green border */  
            font-family: 'Arial', sans-serif;    
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4CAF50, stop:1 #397D49); /* Gradient from lighter to darker green */
        }
        QPushButton:hover {
            background-color: #5CD65C; /* Lighter green for hover */
            border: 2px solid #4CAF50;
        }
        QPushButton:pressed {
            background-color: #397D49; /* Even darker green for pressed */  
        }
        """      
        
        
             
## Stop Words REMOVE Button ##
### Duplicates with Key Words ADD Button ###      
stop_words_remove_button_style_sheet = """
            QPushButton {
                background-color: #d9534f; /* Bootstrap 'btn-danger' red */
                color: white;
                border-radius: 5px;
                padding: 4px 10px;
                max-width: 100px;
                min-width: 80px;
                text-align: center;
                font-size: 12px;
                font-weight: bold;
                border: 1px solid #d43f3a; /* Darker red border */
                font-family: 'Arial', sans-serif;
            }
            QPushButton:hover {
                background-color: #c9302c; /* Lighter red for hover */
                border: 2px solid #d9534f;
            }
            QPushButton:pressed {
                background-color: #ac2925; /* Darker red for pressed */
            }
        """



## Key Words REMOVE Button ##
### Duplicates with Stop Words ADD Button ###
key_words_remove_button_style_sheet = """
            QPushButton {
                background-color: #d9534f; /* Bootstrap 'btn-danger' red */
                color: white;
                border-radius: 5px;
                padding: 4px 10px;
                max-width: 100px;
                min-width: 80px;
                text-align: center;
                font-size: 12px;
                font-weight: bold;
                border: 1px solid #d43f3a; /* Darker red border */
                font-family: 'Arial', sans-serif;
            }
            QPushButton:hover {
                background-color: #c9302c; /* Lighter red for hover */
                border: 2px solid #d9534f;
            }
            QPushButton:pressed {
                background-color: #ac2925; /* Darker red for pressed */
            }
        """      