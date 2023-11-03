import os.path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor, QPen, QCursor, QBrush
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsRectItem, QGraphicsItem, \
    QApplication
from pytesseract import pytesseract

QWIDGETSIZE_MAX = 16777215  # This constant seems to be missing from Pyqt5.


class ImageNotFoundError(Exception):
    pass


class MissingImagePathError(Exception):
    pass


class WordRect(QGraphicsRectItem):
    def __init__(self, word, line_num, word_num, confidence, *args, **kwargs):
        """
        QGraphicsRectItem to store the information about the word detected at its location and to allow word selection
        """
        super().__init__(*args, **kwargs)

        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setToolTip(word)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

        # Set default pen
        rect_pen = QPen(Qt.red)
        rect_pen.setWidth(2)
        self.setPen(rect_pen)

        self.selected_color = QColor(255, 0, 0, 100)  # Default brush color that's to be set when the word is selected

        self.word = word
        self.confidence = confidence

        # Store the predicted line and word numbers for text copying according to the OCR engine
        self.line_num = line_num
        self.word_num = word_num

    def itemChange(self, change, value):
        # TODO: find a way to overwrite the default dashed selection outline. Create custom rect by inheriting
        #  QGraphicsItem?

        #  Change brush color to the specified when the word is selected and back to transparent when unselected
        if change == QGraphicsItem.ItemSelectedChange:
            self.setBrush(QBrush(self.selected_color) if value else QBrush(Qt.transparent))
        return QGraphicsItem.itemChange(self, change, value)


class OCRGraphicsView(QGraphicsView):
    """
    A widget that displays an image and places word rectangles detected with tesseract OCR over it.
    It also allows to select and copy the detected text in a format provided by tesseract.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hide()  # Hide by default and only show when an image path is specified

        policy = self.sizePolicy()
        policy.setRetainSizeWhenHidden(True)
        self.setSizePolicy(policy)

        # TODO: Make custom word selection instead of the default rubberband
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.current_image_path = None
        self.words = []

        self.selected_text = ''
        self.scene.selectionChanged.connect(self.word_selection_changed)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        # Select all words with Ctrl + A and deselect all with Alt + A
        if event.key() == Qt.Key_A:
            if event.modifiers() == Qt.AltModifier:
                self.set_words_selected(False)
            elif event.modifiers() == Qt.ControlModifier:
                self.set_words_selected(True)

        # The Ctrl + C copying behaviour
        if event.modifiers() & Qt.ControlModifier:
            if event.key() == Qt.Key_C:
                text = self.get_formatted_selected_text()
                if text:
                    QApplication.clipboard().setText(text)

    def set_words_selected(self, selected):
        for word in self.words:
            word.setSelected(selected)

    def word_selection_changed(self):
        # When the application closes, this method might get called after the graphics view and it's contents have
        #  already been deleted.
        # For now, it seems fine to simply catch the RuntimeError raised when calling deleted objects
        try:
            # Every time the selection changes, get the newly selected text and store it to minimize calculations.
            self.selected_text = self.get_formatted_selected_text()
        except RuntimeError:
            pass

    def get_formatted_selected_text(self):
        """
        :return: Selected words formatted according to the tesseract line and word prediction
        """
        lines = {}
        for word in self.words:
            if word.isSelected():
                line = word.line_num
                if line in lines:
                    lines[line].append(word)
                else:
                    lines[line] = [word]
        return '\n'.join(' '.join(w.word for w in sorted(lines[i], key=lambda w: w.word_num)) for i in sorted(lines))

    def set_new_image(self, image_path):
        """
        Resets the widget and sets a new image path
        """
        self.reset()
        self.show()
        self.current_image_path = image_path

        # Add the image
        pixmap = QPixmap(image_path)
        item = QGraphicsPixmapItem()
        item.setPixmap(pixmap)
        self.scene.addItem(item)

        x, y, w, h = pixmap.rect().getRect()
        self.scene.setSceneRect(x, y, w, h)
        frame_margin = self.frameWidth() * 2
        # the scroll bars will always appear if the frame isn't taken into account for setting the maximum size
        self.setMaximumSize(w + frame_margin, h + frame_margin)

    def reset(self):
        """
        Resets the state of the widget
        """
        self.hide()
        self.setMaximumSize(QWIDGETSIZE_MAX, QWIDGETSIZE_MAX)

        # Clear the word list first and the scene next to avoid calling deleted items
        self.words.clear()
        self.scene.clear()

        self.current_image_path = None
        self.selected_text = ''

    def remove_word_rects(self):
        """
        Remove the last generated word rectangles, but keep the current image
        """
        for word in self.words:
            self.scene.removeItem(word)
        self.words.clear()
        self.scene.selectionChanged.emit()

    def filter_words(self, min_confidence):
        """
        Show only the words with confidence above or equal to the threshold
        """
        for word in self.words:
            word.setVisible(word.confidence >= min_confidence)

    def extract_text(self, min_confidence=90.0, lang=''):
        """
        Attempt to extract text from the image at the current specified location and raise errors on failure
        """
        if self.current_image_path is None:
            raise MissingImagePathError
        if not os.path.isfile(self.current_image_path):
            self.reset()
            raise ImageNotFoundError

        self.remove_word_rects()

        detected_words = pytesseract.image_to_data(self.current_image_path, lang=lang if lang else 'eng', output_type=pytesseract.Output.DICT)
        for i in range(len(detected_words['level'])):
            row = {k: detected_words[k][i] for k in detected_words}
            if row['conf'] < 0:
                continue
            word, line_num, word_num, confidence, x, y, w, h = row['text'], row['line_num'], row['word_num'], \
                row['conf'], row['left'], row['top'], row['width'], row['height']

            rect = WordRect(word, line_num, word_num, confidence, x, y, w, h)
            self.words.append(rect)
            self.scene.addItem(rect)

        self.filter_words(min_confidence)
