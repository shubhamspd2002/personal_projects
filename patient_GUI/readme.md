# PyQt5 Subject Management GUI

## Overview

This is a simple GUI application built using **PyQt5** that manages a list of subjects. Each subject consists of:
- Name
- Year of Birth
- Gender (male, female, or unknown)
- Symptoms

The application provides an intuitive interface to:
- **Add**, **Edit**, **Delete** subject entries
- **Load** data from a file
- **Save** data to a file
- **Reorder** entries using drag-and-drop

## Features

- 📋 **List Widget** to display subject names
- ➕ **Add Button** to open a dialog and input new subject details
- ✏️ **Edit Button** to update selected subject details
- ❌ **Delete Button** to remove a subject from the list
- 💾 **Save Button** to write subject data to a `.txt` file (CSV-style format)
- 📂 **Load Button** to read subject data from a compatible `.txt` file
- 🔄 **Drag-and-Drop Support** for rearranging list order
- 📑 **Dialog Box** with text fields, spinbox, and radio buttons for structured input

## How It Works

1. **SubjectDialog**: A `QDialog` used for both adding and editing subject information.
   - Uses `QLineEdit` for Name and Symptoms
   - Uses `QSpinBox` for Year of Birth (1900–2100)
   - Uses `QRadioButton` for Gender (m, f, ?)

2. **ListWindow**: The main `QWidget` window that:
   - Displays subject names in a `QListWidget`
   - Provides buttons for Add, Edit, Delete, Load, Save
   - Maintains subject data in a Python list of lists:  
     ```python
     [['Name', 1990, 'm', 'symptoms'], ...]
     ```

3. **File Operations**:
   - **Save**: Saves subjects in comma-separated format:
     ```
     Alice,1995,f,fever
     Bob,1980,m,cough
     ```
   - **Load**: Reads files in the above format and populates the GUI

## Usage

### Run the Application

```bash
python your_script_name.py
