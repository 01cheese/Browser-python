# Browser-python

![image](https://github.com/01cheese/Browser-python/assets/115219323/48ba3c86-c341-4f9b-a17b-565d676c77fb)

My Browser is a custom web browser built using PyQt5 and PyQtWebEngine. It features a tabbed interface, bookmarking functionality, theme management, and a download manager.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Features](#features)
4. [Code Structure](#code-structure)
5. [Detailed Explanation of Modules](#detailed-explanation-of-modules)
6. [Contributing](#contributing)
7. [License](#license)

## Installation

To install the necessary dependencies, ensure you have Python 3.x installed and run:

```sh
pip install PyQt5 PyQtWebEngine
```

## Usage

To run the browser, simply execute the following command:

```sh
python browser.py
```

## Features

- **Tabbed Browsing**: Open multiple tabs for different websites.
- **Bookmark Management**: Add, edit, and delete bookmarks.
- **Theme Management**: Switch between light and dark themes.
- **Download Manager**: Manage file downloads within the browser.

## Code Structure

The project is organized into three main modules:

1. `browser.py`: Contains the main browser window and core functionalities.
2. `bookmarks.py`: Manages bookmark functionalities.
3. `theme.py`: Handles theme management.

## Detailed Explanation of Modules

### browser.py

This is the main module that initializes the browser window and sets up the core functionalities.

#### Key Classes and Methods

- **Browser Class**: Inherits from `QMainWindow` and sets up the UI elements and functionalities.
  - `__init__`: Initializes the browser window, navigation bar, bookmarks bar, status bar, and menu.
  - `create_navbar`: Creates the navigation bar with buttons for back, forward, reload, home, URL bar, bookmark, and downloads.
  - `create_bookmarks_bar`: Creates the bookmarks bar and updates it with current bookmarks.
  - `update_bookmarks_bar`: Updates the bookmarks bar with the latest bookmarks.
  - `create_status_bar`: Creates the status bar for displaying status messages.
  - `create_menu`: Sets up the menu bar with options for file, settings, and bookmarks.
  - `add_new_tab`: Adds a new tab to the browser.
  - `navigate_home`: Navigates the current tab to the homepage.
  - `navigate_to_url`: Navigates the current tab to the URL entered in the URL bar.
  - `bookmark_page`: Adds the current page to bookmarks.
  - `show_downloads`: Displays the downloads dialog with a list of current downloads.

### bookmarks.py

This module manages the bookmark functionalities.

#### Key Classes and Methods

- **BookmarkManager Class**: Manages the list of bookmarks and updates the UI accordingly.
  - `__init__`: Initializes the BookmarkManager with a reference to the parent (browser).
  - `add_bookmark`: Adds a new bookmark and updates the bookmarks menu and bar.
  - `delete_bookmark`: Deletes an existing bookmark and updates the bookmarks menu and bar.
  - `edit_bookmark`: Edits an existing bookmark's title.
  - `populate_bookmarks_menu`: Populates the bookmarks menu with current bookmarks.
  - `update_bookmarks_menu`: Updates the bookmarks menu with the latest bookmarks.
  - `clear_bookmarks`: Clears all bookmarks and updates the UI.

### theme.py

This module handles theme management, allowing the user to switch between light and dark themes.

#### Key Classes and Methods

- **ThemeManager Class**: Manages the application theme.
  - `__init__`: Initializes the ThemeManager with a reference to the parent (browser).
  - `show_theme_dialog`: Displays a dialog for the user to choose between light and dark themes.
  - `change_theme`: Applies the selected theme (light or dark).
  - `enable_dark_mode`: Enables the dark theme.
  - `disable_dark_mode`: Disables the dark theme (reverts to light theme).
  - `apply_theme_to_app`: Applies the chosen theme to the application.
  - `dark_qss`: Returns the style sheet string for the dark theme.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

### Example Code Usage

To bookmark a page programmatically:

```python
browser_instance.bookmark_manager.add_bookmark("Example Title", "http://example.com")
```

To change the theme programmatically:

```python
browser_instance.theme_manager.change_theme(True)  # Enable dark mode
browser_instance.theme_manager.change_theme(False)  # Enable light mode
```
