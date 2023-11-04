from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidgetItem, QListWidget

from known_tesseract_language_options import known_tesseract_language_options as known_options

from pytesseract import pytesseract


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
