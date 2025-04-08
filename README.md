
# Snippet App

A desktop clipboard manager built using PyQt and SQLite/MySQL for storing and managing useful code snippets like a Git cheat sheet. The application allows users to add, edit, and delete snippets, categorize them, and filter them based on category. It also provides hotkey support for easy access and copying of active snippets.

## Features

- **Main Window**: Displays a list view of all snippets with the ability to edit or delete them.
- **Editor Window**: Provides a text area for adding or editing snippets.
- **Categorization & Filtering**: Allows snippets to be categorized for easy searching and filtering.
- **Find Snippets Quickly by Category**: Easily find snippets by category in the main window.
- **Hotkey Support**: Supports `Meta + C` to copy the active snippet to the clipboard.
- **Save Snippets**: Save all snippets as a CSV file for later use or backup.

## Installation

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/snippet-app.git
   ```

2. Navigate into the project directory:
   ```bash
   cd snippet-app
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Running the Application**:
   Start the application with the following command:
   ```bash
   python main.py
   ```

2. **Adding a Snippet**:
   - Open the Editor Window and add your code snippet in the text area.
   - Assign a category to the snippet for easy filtering later.

3. **Editing or Deleting a Snippet**:
   - In the Main Window, click on a snippet to edit or delete it.

4. **Categorizing & Filtering**:
   - Filter snippets by category in the main window for quick access.

5. **Hotkey Support**:
   - Use `Meta + C` (Mac) or `Ctrl + C` (Windows/Linux) to copy the active snippet to your clipboard.

6. **Saving Snippets**:
   - Save all your snippets to a CSV file by selecting the "Save" option in the menu.

## Building the Application

To create a standalone executable of the Snippet App, you can use **PyInstaller**. Follow the steps below:

1. Install PyInstaller if you haven't already:
   ```bash
   pip install pyinstaller
   ```

2. Navigate to the directory containing your project files.

3. Use the following command to build the application into a single executable file:
   ```bash
   pyinstaller --onefile --windowed        --add-data "mainwindow.ui:."        --add-data "addsnippetdialog.ui:."        --add-data "snippet_db.db:."        interface.py
   ```

   - `--onefile`: Creates a single executable file.
   - `--windowed`: Prevents a terminal window from opening when running the app (useful for GUI apps).
   - `--add-data`: Ensures the necessary UI and database files are bundled with the executable.
   - `interface.py`: The main Python script that runs the application.

4. After the build completes, the executable will be found in the `dist` directory.

5. You can now distribute the executable to others without requiring them to install Python or dependencies.

## Technologies Used

- **Python**
- **PyQt** (for the GUI)
- **SQLite/MySQL** (for storing snippets)
- **CSV** (for exporting snippets)

## Contributing

1. Fork this repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to your branch (`git push origin feature-name`).
6. Open a pull request.

## License

This project is licensed under the MIT License 
