from PyQt5.QtWidgets import QMainWindow, QFileDialog

from OCRGraphicsView import ImageNotFoundError, MissingImagePathError
from Ui_QtractWindow import Ui_QtractWindow


# TODO: Image filters
# TODO: Screenshot OCR
# TODO: Implement selection of the tesseract OCR modes
class QtractWindow(QMainWindow, Ui_QtractWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.select_image_location_button.pressed.connect(self.new_image_dialog)
        self.extract_text_button.pressed.connect(self.extract_current_image_text)
        self.minimal_confidence.valueChanged.connect(self.min_confidence_changed)
        self.ocr_image.scene.selectionChanged.connect(self.word_selection_changed)
        self.save_selected_text_button.pressed.connect(self.save_selected_text_dialog)
        self.clear_languages_button.pressed.connect(lambda: self.language_list.set_checked_for_all(False))

    def word_selection_changed(self):
        text = self.ocr_image.selected_text
        self.ocr_text_preview.setText(text)
        self.save_selected_text_button.setEnabled(True if text else False)

    def save_selected_text_dialog(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save selected text', '', "Text file (*.txt)")
        with open(file_name.removesuffix('.txt') + '.txt', mode='w', encoding='UTF-8') as file:
            file.write(self.ocr_image.selected_text)

    def min_confidence_changed(self):
        self.ocr_image.filter_words(self.minimal_confidence.value())

    def new_image_dialog(self):
        """
        Select the image path for an image that will be displayed and scanned for text
        """
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open file", ".", "Image Files (*.png *.jpg *.bmp)"
        )
        if not file_name:
            return
        self.statusbar.clearMessage()
        self.ocr_image.set_new_image(file_name)

    def extract_current_image_text(self):
        """
        Attempt to extract text from the specified image and display message in the statusbar if an error occurred
        """
        self.statusbar.clearMessage()
        try:
            self.ocr_image.extract_text(min_confidence=self.minimal_confidence.value(),
                                        lang='+'.join(self.language_list.get_selected_options()))
            self.ocr_image.setFocus()
        except ImageNotFoundError:
            self.statusbar.showMessage('No image was found at the specified location.')
        except MissingImagePathError:
            self.statusbar.showMessage('Select an image location first.')
