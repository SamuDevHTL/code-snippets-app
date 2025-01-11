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
    QStatusBar,
)
from PyQt6.QtGui import QIcon, QFont, QKeySequence
from PyQt6.QtCore import Qt


class AddSnippetDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add/Edit Snippet")
        self.setGeometry(400, 400, 500, 300)

        # Main layout
        layout = QVBoxLayout()

        # Code snippet editor
        self.text_edit = QPlainTextEdit(self)
        self.text_edit.setPlaceholderText("Enter your code snippet here...")
        self.text_edit.setFont(QFont("Courier New", 10))  # Monospace font for code
        layout.addWidget(self.text_edit)

        # Buttons
        button_layout = QHBoxLayout()

        save_button = QPushButton("Save", self)
        save_button.setIcon(QIcon("assets/save_icon.png"))
        save_button.clicked.connect(self.accept)
        button_layout.addWidget(save_button)

        cancel_button = QPushButton("Cancel", self)
        cancel_button.setIcon(QIcon("assets/cancel_icon.png"))
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

        # Apply modern styles
        self.apply_styles()

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

        self.add_button = QPushButton("Add Snippet")
        self.add_button.setIcon(QIcon("assets/add_icon.png"))
        self.add_button.clicked.connect(self.add_snippet)
        self.add_button.setShortcut(QKeySequence("Ctrl+A"))  # Keyboard shortcut
        button_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Edit Snippet")
        self.edit_button.setIcon(QIcon("assets/edit_icon.png"))
        self.edit_button.clicked.connect(self.edit_snippet)
        self.edit_button.setShortcut(QKeySequence("Ctrl+E"))  # Keyboard shortcut
        button_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Delete Snippet")
        self.delete_button.setIcon(QIcon("assets/delete_icon.png"))
        self.delete_button.clicked.connect(self.delete_snippet)
        self.delete_button.setShortcut(QKeySequence("Ctrl+D"))  # Keyboard shortcut
        button_layout.addWidget(self.delete_button)

        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.setIcon(QIcon("assets/copy_icon.png"))
        self.copy_button.clicked.connect(self.copy_snippet)
        self.copy_button.setShortcut(QKeySequence("Ctrl+C"))  # Keyboard shortcut
        button_layout.addWidget(self.copy_button)

        main_layout.addLayout(button_layout)

        # Set central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Add a status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar )

    def apply_styles(self):
        """Apply modern styles to the application."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E3440;
                color: #D8DEE9;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #FFFFFF
            }
            QListWidget {
                background-color: #3B4252;
                color: #ECEFF4;
                border: 1px solid #4C566A;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton {
                background-color: #5E81AC;
                color: #ECEFF4;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #81A1C1;
            }
            QPlainTextEdit {
                background-color: #3B4252;
                color: #ECEFF4;
                border: 1px solid #4C566A;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
            }
        """)

    def load_snippets(self):
        """Load snippets from the JSON file."""
        try:
            with open(self.snippet_file, "r") as file:
                snippets = json.load(file)
                self.snippet_list.addItems(snippets)
        except (FileNotFoundError, json.JSONDecodeError):
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
                self.status_bar.showMessage("Snippet added successfully.", 2000)

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
                    self.status_bar.showMessage("Snippet edited successfully.", 2000)
        else:
            QMessageBox.warning(self, "No Selection", "Please select a snippet to edit.")

    def delete_snippet(self):
        """Delete the selected snippet."""
        selected_item = self.snippet_list.currentItem()
        if selected_item:
            self.snippet_list.takeItem(self.snippet_list.row(selected_item))
            self.save_snippets()
            self.status_bar.showMessage("Snippet deleted successfully.", 2000)
        else:
            QMessageBox.warning(self, "No Selection", "Please select a snippet to delete.")

    def copy_snippet(self):
        """Copy the selected snippet to the clipboard."""
        selected_item = self.snippet_list.currentItem()
        if selected_item:
            snippet = selected_item.text()
            clipboard = QApplication.clipboard()
            clipboard.setText(snippet)
            self.status_bar.showMessage(f"Snippet copied to clipboard:\n{snippet}", 2000)
        else:
            QMessageBox.warning(self, "No Selection", "Please select a snippet to copy.")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = SnippetManager()
    window.show()

    sys.exit(app.exec())