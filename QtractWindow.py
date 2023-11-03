from PyQt5.QtWidgets import QMainWindow, QFileDialog

from Ui_QtractWindow import Ui_QtractWindow
from OCRGraphicsView import ImageNotFoundError, MissingImagePathError
from pytesseract import TesseractNotFoundError


# TODO: Language selection
# TODO: Image filters
# TODO: Screenshot OCR
# TODO: Implement saving text into a .txt file
class QtractWindow(QMainWindow, Ui_QtractWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.select_image_location.pressed.connect(self.new_image_dialog)
        self.extract_text.pressed.connect(self.extract_current_image_text)
        self.minimal_confidence.valueChanged.connect(self.min_confidence_changed)
        self.ocr_image.scene.selectionChanged.connect(self.word_selection_changed)

    def word_selection_changed(self):
        # When the application closes, this method might get called after the graphics view and it's contents have
        #  already been deleted.
        # For now, it seems fine to simply catch the RuntimeError raised when calling deleted objects
        try:
            self.ocr_text_preview.setText(self.ocr_image.get_selected_text())
        except RuntimeError:
            pass

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
            self.ocr_image.extract_text(min_confidence=self.minimal_confidence.value())
            self.ocr_image.setFocus()
        except ImageNotFoundError:
            self.statusbar.showMessage('No image was found at the specified location.')
        except MissingImagePathError:
            self.statusbar.showMessage('Select an image location first.')
        except TesseractNotFoundError:
            self.statusbar.showMessage("Tesseract OCR is not installed or it's not in the PATH.")
