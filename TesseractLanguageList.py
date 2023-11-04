from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidgetItem, QListWidget

from csv import reader

from pytesseract import pytesseract

LANGUAGE_OPTIONS_TSV_PATH = 'Known tesseract language options.tsv'


class LanguageItem(QListWidgetItem):
    """
    QListWidgetItem to store information about a tesseract language option
    """

    def __init__(self, tesseract_option, description, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setText(f'{tesseract_option} - {description}')
        self.setCheckState(Qt.Unchecked)
        self.tesseract_option = tesseract_option
        self.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)


class TesseractLanguageList(QListWidget):
    """
    QListWidget to store the available tesseract language options as items and to easily select and retrieve them
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        available_options = pytesseract.get_languages()

        with open(LANGUAGE_OPTIONS_TSV_PATH, 'r', newline='', encoding='UTF-8') as f:
            r = reader(f, delimiter='\t')
            next(r)
            known_options = dict(r)

        self.languages = []
        for option in available_options:
            item = LanguageItem(option, known_options[option] if option in known_options else 'Unknown option')
            self.addItem(item)
            self.languages.append(item)

    def set_checked_for_all(self, checked):
        for lang in self.languages:
            lang.setCheckState(Qt.Checked if checked else Qt.Unchecked)

    def get_selected_options(self):
        """
        :return: Selected tesseract OCR options
        """
        return [lang.tesseract_option for lang in self.languages if lang.checkState() == Qt.Checked]
