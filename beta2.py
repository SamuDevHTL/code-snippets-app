import json
import sys
import os
import shutil
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QMessageBox,
    QDialog,
    QPlainTextEdit,
    QHBoxLayout,
    QWidget,
    QStatusBar,
    QLabel,
    QLineEdit,
    QFileDialog,
    QTreeWidget,
    QTreeWidgetItem,
    QInputDialog
)
from PyQt6.QtGui import QIcon, QFont, QMouseEvent, QKeySequence
from PyQt6.QtCore import Qt, QPoint

def apply_styles(app):
    """Apply macOS-like styles to the application."""
    app.setStyleSheet("""
        QMainWindow {
            background-color: #2E3440;
            color: #D8DEE9;
        }
        QLabel {
            font-size: 16px;
            font-weight: bold;
            color: #D8DEE9;
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
        QLineEdit {
            background-color: #3B4252;
            color: #ECEFF4;
            border: 1px solid #4C566A;
            border-radius: 5px;
            padding: 5px;
            font-size: 14px;
        }
        QLineEdit:focus {
            border: 1px solid #81A1C1;
        }
        QTreeWidget {
            background-color: #3B4252;
            color: #ECEFF4;
            border: 1px solid #4C566A;
        }
    """)

class AddSnippetDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add/Edit Snippet")
        self.setGeometry(400, 400, 500, 300)



        # Main layout
        layout = QVBoxLayout()

        # Snippet title input
        self.title_edit = QLineEdit(self)
        self.title_edit.setPlaceholderText("Enter snippet title here...")
        layout.addWidget(self.title_edit)

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

    def get_snippet(self):
        """Return the title and text entered in the dialog."""
        title = self.title_edit.text().strip()
        snippet = self.text_edit.toPlainText().strip()
        return title, snippet

class Sidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.snippet_manager = None  # Placeholder for the snippet manager
        self.project_folder = os.path.join(os.getcwd(), "snippets") 
        if not os.path.exists(self.project_folder):
            os.makedirs(self.project_folder)
        self.setStyleSheet("""
            QWidget {
                background-color: #2E3440;
                color: #D8DEE9;
            }
            QTreeWidget {
                background-color: #3B4252;
                color: #ECEFF4;
                border: 1px solid #4C566A;
                border-radius: 5px;
                padding: 10px;
            }
            QTreeWidget::item:hover {
                background-color: #434C5E;
            }
            QTreeWidget::item:selected {
                background-color: #81A1C1;
                color: #ECEFF4;
            }
            QPushButton {
                background-color: #4C566A;
                color: #ECEFF4;
                border: 1px solid #5E81AC;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
        """)

        layout = QVBoxLayout()

        # Add a tree widget to display folders and files
        self.tree_widget = QTreeWidget(self)
        self.tree_widget.setHeaderHidden(True)  # Hide the header
        self.tree_widget.itemClicked.connect(self.on_item_clicked)  # Connect item click event
        layout.addWidget(self.tree_widget)

        # Populate the tree widget with folders and files
        self.populate_tree()

        # Add buttons for sidebar functionality
        self.add_buttons(layout)

        self.setLayout(layout)

    def add_buttons(self, layout):
        """Add buttons to the sidebar."""
        load_button = QPushButton("Add Folder")
        load_button.clicked.connect(self.add_folder)

        save_button = QPushButton("Add Snippet")
        save_button.clicked.connect(self.add_file)

        refresh_button = QPushButton("Delete")
        refresh_button.clicked.connect(self.remove_selected)

        # Add buttons to the layout
        layout.addWidget(load_button)
        layout.addWidget(save_button)
        layout.addWidget(refresh_button)

    def set_snippet_manager(self, snippet_manager):
        """Set the snippet manager for the sidebar."""
        self.snippet_manager = snippet_manager

    def populate_tree(self):
        """Populate the tree widget with folders and JSON files."""
        if not os.path.exists(self.project_folder):
            os.makedirs(self.project_folder)

        root_folder = QTreeWidgetItem(self.tree_widget, ["Snippets"])
        self.tree_widget.addTopLevelItem(root_folder)

        for folder in os.listdir(self.project_folder):
            folder_path = os.path.join(self.project_folder, folder)
            if os.path.isdir(folder_path):
                folder_item = QTreeWidgetItem(root_folder, [folder])
                for file in os.listdir(folder_path):
                    if file.endswith(".json"):
                        file_item = QTreeWidgetItem(folder_item, [file])

        # Expand the root folder by default
        root_folder.setExpanded(True)

    def refresh_sidebar(self):
        """Placeholder for refreshing the sidebar."""
        self.tree_widget.clear()
        self.populate_tree()
        QMessageBox.information(self, "Info", "Sidebar refreshed.")

    def on_item_clicked(self, item):
        """Handle item click event to load JSON files."""
        if item.childCount() == 0:  # Check if the item is a file (no children)
            file_name = item.text(0)
            if item.parent() is not None:  # Check if the item has a parent
                folder_name = item.parent().text(0)
                file_path = os.path.join(self.project_folder, folder_name, file_name)
            else:  # If the item is a top-level item, do not try to open a file
                return

            if os.path.isfile(file_path):  # Check if the file_path is a file
                if file_path.endswith('.json'):  # Check if the file is a JSON file
                    try:
                        with open(file_path, "r") as file:
                            data = json.load(file)
                            if self.snippet_manager:
                                self.snippet_manager.handle_loaded_json(data)
                    except (FileNotFoundError, json.JSONDecodeError) as e:
                        QMessageBox.warning(self, "Error", f"Could not load file: {file_name}")
                else:
                    QMessageBox.warning(self, "Error", f"'{file_name}' is not a JSON file.")
            else:
                if os.path.isdir(file_path):  # Check if the file_path is a directory
                    pass
                else:
                    pass
        else:
            pass

    def add_folder(self):
        """Add a new folder to the tree."""
        current_item = self.tree_widget.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a folder to add a sub-folder.")
            return

        folder_name, ok = QInputDialog.getText(self, "Add Folder", "Enter folder name:")
        if ok and folder_name.strip():
            new_folder = QTreeWidgetItem(current_item, [folder_name])
            current_item.setExpanded(True)  # Expand the parent folder

            # Create the new folder in the project folder
            folder_path = os.path.join(self.project_folder, current_item.text(0), folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

    def add_file(self):
        """Add a new JSON file to the tree."""
        current_item = self.tree_widget.currentItem()

        # If no item is selected, add the file to the root folder
        if current_item is None:
            file_name, ok = QInputDialog.getText(self, "Add File", "Enter file name (with .json extension):")
            if ok and file_name.strip().endswith(".json"):
                # Add the file to the root folder in the tree
                QTreeWidgetItem(self.tree_widget, [file_name])
                # Create the file in the project folder
                file_path = os.path.join(self.project_folder, file_name)
                with open(file_path, 'w') as file:
                    # Initialize the JSON file with an empty list
                    json.dump([], file)
                # Open the file for editing
                self.snippet_manager.handle_loaded_json([])
                self.snippet_manager.current_file = file_path
            else:
                QMessageBox.warning(self, "Invalid File Name", "File name must end with '.json'.")
        else:
            # If a folder is selected, add the file to that folder
            if current_item.childCount() > 0 or current_item.text(0) == "Snippets":
                file_name, ok = QInputDialog.getText(self, "Add File", "Enter file name (with .json extension):")
                if ok and file_name.strip().endswith(".json"):
                    # Add the file to the selected folder in the tree
                    QTreeWidgetItem(current_item, [file_name])
                    current_item.setExpanded(True)  # Expand the parent folder
                    # Create the file in the selected folder
                    folder_path = os.path.join(self.project_folder, current_item.text(0))
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)
                    file_path = os.path.join(folder_path, file_name)
                    with open(file_path, 'w') as file:
                        # Initialize the JSON file with an empty list
                        json.dump([], file)
                    # Open the file for editing
                    self.snippet_manager.handle_loaded_json([])
                    self.snippet_manager.current_file = file_path
                else:
                    QMessageBox.warning(self, "Invalid File Name", "File name must end with '.json'.")
            else:
                QMessageBox.warning(self, "Invalid Selection", "Please select a folder or the root folder to add a file.")

    def remove_selected(self):
        """Remove the selected folder or file."""
        current_item = self.tree_widget.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select an item to remove.")
            return

        parent_item = current_item.parent()
        if parent_item:
            index = parent_item.indexOfChild(current_item)
            parent_item.takeChild(index)

            # Remove the corresponding file from the project folder
            file_path = os.path.join(self.project_folder, parent_item.text(0), current_item.text(0))
            print(f"Removing file: {file_path}")
            try:
                if os.path.isfile(file_path):
                    os.chmod(file_path, 0o777)  # Change file permissions to read, write, and execute
                    os.remove(file_path)
                    QMessageBox.information(self, "Success", f"File '{current_item.text(0)}' removed successfully.")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    QMessageBox.information(self, "Success", f"Folder '{current_item.text(0)}' removed successfully.")
            except OSError as e:
                QMessageBox.warning(self, "Error", f"Could not remove item: {e}")
        else:
            index = self.tree_widget.indexOfTopLevelItem(current_item)
            self.tree_widget.takeTopLevelItem(index)

            # Remove the corresponding folder from the project folder
            folder_path = os.path.join(self.project_folder, current_item.text(0))
            print(f"Removing folder: {folder_path}")
            try:
                shutil.rmtree(folder_path)
                QMessageBox.information(self, "Success", f"Folder '{current_item.text(0)}' removed successfully.")
            except OSError as e:
                QMessageBox.warning(self, "Error", f"Could not remove folder: {e}")


class SnippetManager(QMainWindow):
    def __init__(self):
        super().__init__()

        # Remove the default title bar
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowSystemMenuHint |
                            Qt.WindowType.WindowCloseButtonHint)

        # Apply macOS-like styles
        apply_styles(self)

        # Custom top bar
        self.custom_title_bar = QWidget(self)
        self.custom_title_bar.setStyleSheet("""
            QWidget {
                background-color: #2E3440;
                border-bottom: 1px solid #4C566A;
            }
            QPushButton {
                background-color: transparent;
                border: none;
                color: #D8DEE9;
                font-size: 16px;
            }
            QPushButton:hover {
                color: #81A1C1;
            }
            QPushButton:pressed {
                background-color: #434C5E;
            }
        """)
        self.custom_title_bar.setFixedHeight(30)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        layout.addStretch()  # Fills space on the left

        minimize_button = QPushButton()
        minimize_button.setIcon(QIcon("assets/minimize_icon.png"))
        minimize_button.clicked.connect(self.showMinimized)
        layout.addWidget(minimize_button)

        fullscreen_button = QPushButton()
        fullscreen_button.setIcon(QIcon("assets/fullscreen_icon.png"))
        fullscreen_button.clicked.connect(self.toggle_fullscreen)
        layout.addWidget(fullscreen_button)

        close_button = QPushButton()
        close_button.setIcon(QIcon("assets/close_icon.png"))
        close_button.clicked.connect(self.close_application)
        layout.addWidget(close_button)

        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if widget:
                widget.setFixedSize(24, 24)  # Set a smaller fixed size for the icons

        self.custom_title_bar.setLayout(layout)

        # Sidebar setup
        self.sidebar = Sidebar(self)
        self.sidebar.set_snippet_manager(self)
        
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 3, 0, 1)  # Adjust margins for top bar

        content_layout = QVBoxLayout()

        label = QLabel("Code Snippets:")
        label.setStyleSheet("color: #D8DEE9; font-size: 16px;")
        content_layout.addWidget(label)

        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search snippets...")
        self.search_bar.textChanged.connect(self.filter_snippets)
        content_layout.addWidget(self.search_bar)

        self.snippet_list = QListWidget()
        self.snippet_list.itemDoubleClicked.connect(self.edit_snippet)
        content_layout.addWidget(self.snippet_list)

        self.current_file = None  # Track the currently loaded JSON file

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)

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

        self.load_button = QPushButton("Load Snippets")
        self.load_button.setIcon(QIcon("assets/load_icon.png"))
        self.load_button.clicked.connect(self.load_snippets)
        button_layout.addWidget(self.load_button)

        content_layout.addLayout(button_layout)

        # Add the sidebar and content layout to the main layout
        main_layout.addWidget(self.sidebar)
        main_layout.addLayout(content_layout)

        container = QWidget()
        container.setLayout(main_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.custom_title_bar)
        layout.addWidget(container)
        self.setCentralWidget(QWidget(self))
        self.centralWidget().setLayout(layout)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def load_snippets(self):
        """Open a file dialog to select a JSON file and load snippets."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Snippet File", "", "JSON Files (*.json)")
        if file_name:
            self.current_file = file_name
            try:
                with open(self.current_file, "r") as file:
                    snippets = json.load(file)
                    self.snippet_list.clear()
                    self.snippet_list.addItems([f"{item['title']}: {item['snippet']}" for item in snippets])
            except (FileNotFoundError, json.JSONDecodeError):
                self.snippet_list.clear()
                QMessageBox.warning(self, "Error", "Failed to load snippets from the selected file.")

    def save_snippets(self):
        """Save snippets to the currently loaded JSON file."""
        if not self.current_file:
            # If no file is loaded, prompt the user to save to a new file
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Snippet File", "", "JSON Files (*.json)")
            if file_name:
                self.current_file = file_name
            else:
                QMessageBox.warning(self, "No File Selected", "Please select a file to save the snippets.")
                return

        print(f"Saving to file: {self.current_file}")  # Debug print

        # Prepare the data to save
        snippets = []
        for i in range(self.snippet_list.count()):
            item = self.snippet_list.item(i)
            title, snippet = item.text().split(":", 1)  # Split into title and snippet
            snippets.append({"title": title.strip(), "snippet": snippet.strip()})

        print(f"Data to save: {snippets}")  # Debug print

        # Write the data to the file
        try:
            with open(self.current_file, "w") as file:
                json.dump(snippets, file, indent=4)  # Save with pretty formatting
            print("File saved successfully.")  # Debug print
            self.status_bar.showMessage(f"Snippets saved to {self.current_file}", 2000)

            # Verify the file contents after saving
            with open(self.current_file, "r") as file:
                saved_data = json.load(file)
                print(f"File contents after saving: {saved_data}")  # Debug print
        except Exception as e:
            print(f"Error saving file: {e}")  # Debug print
            QMessageBox.warning(self, "Error", f"Failed to save snippets: {str(e)}")

    def add_snippet(self):
        """Open dialog to add a new snippet."""
        dialog = AddSnippetDialog(self)
        if dialog.exec():
            title, snippet = dialog.get_snippet()
            if title and snippet:
                self.snippet_list.addItem(f"{title}: {snippet}")
                self.save_snippets()
                self.status_bar.showMessage("Snippet added successfully.", 2000)

    def edit_snippet(self):
        """Open dialog to edit the selected snippet."""
        selected_item = self.snippet_list.currentItem()
        if selected_item:
            dialog = AddSnippetDialog(self)
            title, snippet = selected_item.text().split(":", 1)
            dialog.title_edit.setText(title.strip())
            dialog.text_edit.setPlainText(snippet.strip())
            if dialog.exec():
                new_title, new_snippet = dialog.get_snippet()
                if new_title and new_snippet:
                    selected_item.setText(f"{new_title}: {new_snippet}")
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
            snippet = selected_item.text().split(":", 1)[1].strip()
            clipboard = QApplication.clipboard()
            clipboard.setText(snippet)
            self.status_bar.showMessage(f"Snippet copied to clipboard:\n{snippet}", 2000)
        else:
            QMessageBox.warning(self, "No Selection", "Please select a snippet to copy.")

    def close_application(self):
        """Close the application."""
        QApplication.quit()

    def toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def filter_snippets(self, text):
        """Filter snippets based on search text."""
        for i in range(self.snippet_list.count()):
            item = self.snippet_list.item(i)
            item.setHidden(text.lower() not in item.text().lower())

    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press event for dragging the window."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        """Handle mouse move event for dragging the window."""
        if event.buttons() == Qt.MouseButton.LeftButton and hasattr(self, 'drag_position'):
            delta = QPoint(event.globalPosition().toPoint() - self.drag_position)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.drag_position = event.globalPosition().toPoint()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Handle mouse release event to stop dragging."""
        if event.button() == Qt.MouseButton.LeftButton:
            if hasattr(self, 'drag_position'):
                del self.drag_position
        super().mouseReleaseEvent(event)

    def handle_loaded_json(self, data):
        """Handle the loaded JSON data."""
        print("handle loaded json method called")
        print(f"loaded json data: {data}")
        # Clear the current snippet list
        self.snippet_list.clear()
        
        # Add the loaded snippets to the list
        for item in data:
            self.snippet_list.addItem(f"{item['title']}: {item['snippet']}")
        
        # Optionally, set the current file path
        self.current_file = "C:/Users/User/Desktop/code-snippets/code-snippets/snippets/snippets.json"  # Update this as needed

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = SnippetManager()
    window.show()

    sys.exit(app.exec())
