import sys
import json
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QLabel,
    QMessageBox,
    QDialog,
    QPlainTextEdit,
    QHBoxLayout,
    QWidget,
)


class AddSnippetDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add/Edit Snippet")
        self.setGeometry(400, 400, 500, 300)

        # Main layout
        layout = QVBoxLayout()

        self.text_edit = QPlainTextEdit(self)
        layout.addWidget(self.text_edit)

        # Buttons
        button_layout = QHBoxLayout()

        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.accept)
        button_layout.addWidget(save_button)

        cancel_button = QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def get_text(self):
        """Return the text entered in the dialog."""
        return self.text_edit.toPlainText()


class SnippetManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Code Snippet Manager")
        self.setGeometry(300, 300, 600, 400)

        # Main layout
        main_layout = QVBoxLayout()

        # Label
        label = QLabel("Code Snippets:")
        main_layout.addWidget(label)

        # List of snippets
        self.snippet_list = QListWidget()
        self.snippet_list.itemDoubleClicked.connect(self.edit_snippet)
        main_layout.addWidget(self.snippet_list)

        # Load snippets from JSON
        self.snippet_file = "snippets.json"
        self.load_snippets()

        # Buttons
        button_layout = QHBoxLayout()

        add_button = QPushButton("Add Snippet")
        add_button.clicked.connect(self.add_snippet)
        button_layout.addWidget(add_button)

        edit_button = QPushButton("Edit Snippet")
        edit_button.clicked.connect(self.edit_snippet)
        button_layout.addWidget(edit_button)

        delete_button = QPushButton("Delete Snippet")
        delete_button.clicked.connect(self.delete_snippet)
        button_layout.addWidget(delete_button)

        copy_button = QPushButton("Copy to Clipboard")
        copy_button.clicked.connect(self.copy_snippet)
        button_layout.addWidget(copy_button)

        main_layout.addLayout(button_layout)

        # Set central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def load_snippets(self):
        """Load snippets from the JSON file."""
        try:
            with open(self.snippet_file, "r") as file:
                snippets = json.load(file)
                self.snippet_list.addItems(snippets)
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn't exist or is invalid, start with an empty list
            self.snippet_list.addItems([])

    def save_snippets(self):
        """Save snippets to the JSON file."""
        snippets = [self.snippet_list.item(i).text() for i in range(self.snippet_list.count())]
        with open(self.snippet_file, "w") as file:
            json.dump(snippets, file, indent=4)

    def add_snippet(self):
        """Open dialog to add a new snippet."""
        dialog = AddSnippetDialog(self)
        if dialog.exec():
            snippet = dialog.get_text()
            if snippet.strip():
                self.snippet_list.addItem(snippet)
                self.save_snippets()

    def edit_snippet(self):
        """Open dialog to edit the selected snippet."""
        selected_item = self.snippet_list.currentItem()
        if selected_item:
            dialog = AddSnippetDialog(self)
            dialog.text_edit.setPlainText(selected_item.text())
            if dialog.exec():
                snippet = dialog.get_text()
                if snippet.strip():
                    selected_item.setText(snippet)
                    self.save_snippets()
        else:
            QMessageBox.warning(self, "No Selection", "Please select a snippet to edit.")

    def delete_snippet(self):
        """Delete the selected snippet."""
        selected_item = self.snippet_list.currentItem()
        if selected_item:
            self.snippet_list.takeItem(self.snippet_list.row(selected_item))
            self.save_snippets()
            QMessageBox.information(self, "Deleted", "Snippet deleted successfully.")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a snippet to delete.")

    def copy_snippet(self):
        """Copy the selected snippet to the clipboard."""
        selected_item = self.snippet_list.currentItem()
        if selected_item:
            snippet = selected_item.text()
            clipboard = QApplication.clipboard()
            clipboard.setText(snippet)
            QMessageBox.information(self, "Success", f"Snippet copied to clipboard:\n{snippet}")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a snippet to copy.")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = SnippetManager()
    window.show()

    sys.exit(app.exec())
