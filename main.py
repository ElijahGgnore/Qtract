import sys

from pytesseract import pytesseract, TesseractNotFoundError

from QtractWindow import QtractWindow
from PyQt5.QtWidgets import QApplication, QMessageBox

if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        # Initial tesseract call to verify it's installed correctly.
        # This function raises TesseractNotFoundError if it is unable to call tesseract
        pytesseract.get_tesseract_version()
    except TesseractNotFoundError as e:
        # Show an error message if tesseract couldn't be accessed during the initial call
        error_name = e.__class__.__name__
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(error_name)
        msg.setInformativeText("Tesseract OCR is not installed or it's not in the PATH.")
        msg.setWindowTitle(error_name)
        sys.exit(msg.exec_())

    window = QtractWindow()
    window.show()
    sys.exit(app.exec_())
