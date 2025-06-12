# -*- coding: utf-8 -*-

import sys # this initialises a QApplication instance and handles Command Line Arguments
from PyQt5.QtWidgets import (
    QWidget, #base class for all windows
    QLabel, #to display non editable text in GUI
    QLineEdit, #allows users to input single line text
    QTextEdit, #allows users to input multi line text
    QListWidget, #a list view for displaying multiple items
    QPushButton, #buttons to perform actions like "add", "edit", "delete", etc
    QSpinBox, #allows users to select numeric values within a range.
    QRadioButton, #Provides selectable options where only one button can be chosen at a time (the button looks like a buttet point and once selected, turns blue). 
                    #only one radio button at a time can be checked; if the user selects another button, the previously selected button is switched off.
    QButtonGroup, # Groups radio buttons to enforce single selection
    QApplication, 
    QDialog, #Represents the pop-up dialog box for editing subject details.
    QFileDialog, # Allows users to select files for loading and saving data.
    QGridLayout, QHBoxLayout, QVBoxLayout, QFormLayout #Layout managers to arrange widgets in a grid, horizontal, vertical, or labeled rows.
)
from PyQt5.QtCore import Qt #Provides constants like Qt.InternalMove used for enabling drag-and-drop reordering in the list

'''
This class opens a QDialog box which takes input from the user about their name, Year of birth, symptom and gender
This QBox has two buttons:
Ok: This saves the data (tells the QWidget behind to accept this data and store it and display it)
Cancel: closes the QDialog box without saving its contents (if entered)
'''
class SubjectDialog(QDialog): #here we are making the dialogue box which will pop up if we click Add or Edit
    def __init__(self, parent=None, data=None): #Setting data to None by default means that if no specific data is provided when creating an instance of SubjectDialog, the dialog can still be instantiated without any initial data. This allows for flexibility in how the dialog is used.
        super().__init__(parent) #

        # Create widgets
        self.name_edit = QLineEdit() #whatever u enter in the QLineEdit will be stored in the object
        self.year_spinbox = QSpinBox() 
        self.year_spinbox.setRange(1900, 2100) #we meed to set the range when we create a QSpinBox()
        self.symptoms_edit = QLineEdit() 

        self.gender_group = QButtonGroup(self) #this Qbuttongroup will consist of qradio buttons (if u initialize them as below) and it will enforce only selection of one option. 
                                               #if u select something else, then the previously selected one will get automatically unselected. self is passed as an argument here 
                                               # so that it becomes a part of the widget hierarchy of the parent widget self and this group is destroyed when the parent widget is destroyed
        self.male_button = QRadioButton('m') 
        self.female_button = QRadioButton('f')
        self.unknown_button = QRadioButton('?')

        #the following three lines adds the 3 buttons to the QButtonGroup()
        self.gender_group.addButton(self.male_button) 
        self.gender_group.addButton(self.female_button)
        self.gender_group.addButton(self.unknown_button)

        ok_button = QPushButton("OK") #this will save the data. This push button will get highlighted if we hover our cursor on it 
        cancel_button = QPushButton("Cancel") #this will close the small window without saving the data

        ok_button.clicked.connect(self.accept) #cliclked is a signal emitted by QPushbutton when button is clicked. .connect() links the signal to a slot. self.accept is a builtin method of the QDIalog class which marks the data entered by the user as accepted and closes the dialogue box. 
                                                #the dialogue result after it closes itself is QDialogue.Accepted
        cancel_button.clicked.connect(self.reject) #self.reject marks the data entered by the user as rejected. The dialogue result after it closes itself is QDialogue.Rejected

        # Layout setup
        form_layout = QFormLayout() #this lays out its children in two column form. it is like an imaginary table in which we add rows and they are adjusted automatically. 
        form_layout.addRow("Name", self.name_edit) #it is something like this addrow(label, widget) label (column1) typically should contain labels and widgets  should contain input fields
        form_layout.addRow("Year of Birth", self.year_spinbox) 
        form_layout.addRow("Symptoms", self.symptoms_edit)
        form_layout.addRow("Gender", self.male_button) #we are exploiting the QFormLayout()'s organisation to represent the gender in a neat way
        form_layout.addWidget(self.female_button) #addWidget() just adds something to the widget column. Note that there is no such method as addLabel() just to add a label
        form_layout.addWidget(self.unknown_button) #to add just a label u can do: form_layout.addRow("Gender", None) or form_layout.addRow(Qlabel("The label"))
                                                    #to add just widget u can do: form_layout.addRow(None, self.male_button) or form_layout.addRow(QWidget("The label"))

        button_layout = QHBoxLayout() #This creates a horizontal layout where u can add widgets from left to right and the order depends on which line is written first. U can also try QVBoxLayout()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        main_layout = QVBoxLayout() #in these 3 lines what we are doing is we are creating a vertical box and then we add:
        main_layout.addLayout(form_layout) #this is the name, year of birth, gender etc which is in the QFormLayout(). We use addLayout() to add one layout to another
        main_layout.addLayout(button_layout) #then below it we add the ok and cancel buttons which are in the QHBoxLayout(). #addLayout is different from setLayout. It nests a child layout inside a parent layout 
                                             #addLayout is used when u combine multiple layouts like QFormLayout, QHBoxlayout, QVBoxLayout to a parent layout 
                                            # and the parent layout can itself be any one of the above 3 or something else
                                            

        self.setLayout(main_layout)#after adding all the layouts using addLayout() you can set the layout that u gave created as the main one using setLayout(). U always use setLayout() at the end when everything is done
                                            #Now main_layout becomes the primary layout of the class SubjectDialog after using setLayout()

        self.setGeometry(300, 300, 350, 300) #here the format is (x, y, width, length) where x and y values represent the coordinates (x,y) of the top left corner of the widget relative to the screen. i.e where the dialog box should appear on the screen i.e in the middle or left or right etc. make it 1000 1000 and understand the function
                                                #here in the length even if u make it 10, the widgets will be one besides the other (as it is a QVBox) but they wont overlap cause every widget in the QVBox has a boundary
        self.setWindowTitle('Subject')

        if data: #here data consists of list and this if statement will be true if there are elements in the list. This will be run when we select a data and then we click edit so that we can see the data in the cells  
            self.setData(data) 
                                                
    """
    This function takes subject as an input which is a list representing subject details. Whenever the
    function is called the dialog box shows (or displays) the current data of the subject. You call this function when u
    open a dialog box to edit an existing subject's details
    """                                            
    def setData(self, subject):
        self.name_edit.setText(subject[0]) # settext() displays the 1st element of the list subject in the box created using QLineEdit()
        self.year_spinbox.setValue(subject[1])

        if subject[2] == 'm':
            self.male_button.setChecked(True)
        elif subject[2] == 'f':
            self.female_button.setChecked(True) #if u put false here and then execute the code then when u click some data and click f and save it, it wont get saved
        else:
            self.unknown_button.setChecked(True)

        self.symptoms_edit.setText(subject[3])
        """This function reads the data entered in the GUI elements. This also saves the data if modified by the user
            returns: a list (this list is then used by set data later)
        """
    def getData(self):
        gender = 'm' if self.male_button.isChecked() else ('f' if self.female_button.isChecked() else '?') #ischecked() determines whether the radio button is selected not
        return [
            self.name_edit.text(), #.text() gets the name as a string
            self.year_spinbox.value(), #.value() as an integer
            gender,
            self.symptoms_edit.text()
        ]

"""
This is the class ListWindow which is a QWidget which will display the contents 'Dummy Name' and 'Other Dummy Name' on the widget
This QWidget also gives us buttons. The buttons and their respective functions are as follows:
Add: To add data to the list widget in front (uses the class SubjectDialog)
Edit: To edit any selected content already displayed on the widget (uses the class SubjectDialog)
Delete: Deletes any selected content
Load: to upload any data saved on the PC
Save: to save the data in the list widget to ur PC
"""
class ListWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.data = [
            ['Dummy Name', 1900, 'm', 'some symptoms'],
            ['Other Dummy Name', 1970, 'f', 'other symptoms']
        ]

        self.list = QListWidget() #helps to diplay a list of items. Helps in managing a collection of data in a simple list format
        self.list.setDragDropMode(QListWidget.InternalMove) #this setDragDropMode helps in reordering of the list contents. To use this, just press and hold one list content and then reorder it
                                                            # InternalMove means items can only be moved within the widget, not outside it
        self.list.model().rowsMoved.connect(self.onRowsMoved) #if the rows are moved then arrange and update the data accordingly in the self.data

        self.updateList() #this populates the self.list widget with the self.data. The function is below in the code

        button_add = QPushButton('Add') # add a new subject
        button_edit = QPushButton('Edit') #edit a selected subject (this will only work if any list is selected)
        button_delete = QPushButton('Delete') #delete a subject (this will only work if any list is selected)
        button_load = QPushButton('Load') #load a data from the pc in which the contents are in the required format
        button_save = QPushButton('Save') #save the data in a directory

        #these 5 lines connects each action of clicking that button to the function as to what the action should do
        button_add.clicked.connect(self.onAddClicked) 
        button_edit.clicked.connect(self.onEditClicked)
        button_delete.clicked.connect(self.onDeleteClicked)
        button_load.clicked.connect(self.onLoadClicked)
        button_save.clicked.connect(self.onSaveClicked)

        hbox = QHBoxLayout()
        hbox.addWidget(button_add)
        hbox.addWidget(button_edit)
        hbox.addWidget(button_delete)
        hbox.addWidget(button_load)
        hbox.addWidget(button_save)

        vbox = QVBoxLayout()
        vbox.addWidget(self.list)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Subject List')
        self.show() #displays it on the window
        """
        This function first clears the whole data in the self.list and then repopulates it with names of the subjects
        we clear it first because when we update the widget which may have new data, we dont want the old data to be repeated again
        """
    def updateList(self):
        self.list.clear() #it is important to clear the contents before updating them because then they will duplicate themselves after clicking ok 
        for subject in self.data:
            self.list.addItem(subject[0]) #the 1st element in every list (the name) is used to display. addItem adds the clickable boxes containing the data and addItem takes in 1 string argument which should represent the name of the clickable box
        """
        When u click the add button, button_add.clicked.connect(self.onAddClicked)  gets triggered and then it runs this program
        it first opens the dialog box (defined in the above class) and then u can interact with the box. 
        it doesnt close the dialog box until ok or cancel is clicked. 
        If ok is clicked, it gets the data in the form of list (using getData) and then appends the list to the self.data. 
        Then later we update the data 
        """
    def onAddClicked(self):
        dlg = SubjectDialog(self) #opens the diaogue box which we defined above (creates an instance of the SubjectDialog dialog box) here the parameter is self i.e parent listWindow
                                    #this establishes a relationship between the ListWindow and the DialogBox ensuring that the diualog box behaves like a child window (it will stay on top of the ListWindow and close with it).
        if dlg.exec_() == dlg.Accepted:         #this displays the subjectDialog to the user and waits for them to interact with it. 
                                                #dlg.exec_() opens dialog box in modal state (blocks interaction with the LisWindow until the dialog box is closed)
                                                #the if statement Checks if the dialog was closed using the "OK" button (dlg.accept() was triggered).
            self.data.append(dlg.getData()) #go to the getData function to understand this. 
            self.updateList() #we have to update because new data was added. see the updateList() function to understand how new data is added
        """
        This function 1st verifies which data is being clicked by currentRow() or data is even clicked or not
        then it opens that data and displays it because of the line if data: self.setData(data) in the SubjectDialog class 
        if we click ok then the new data entered is captured using getData (which is a list) and now this new list is replaced by the old one 
        then update
        """
    def onEditClicked(self):
        current_row = self.list.currentRow() #this checks which row is currently selected and assigns it to current_row. self.list.currentRow() returns 0 if 1st item is selected, 1 if 2nd is selected
        if current_row < 0: #these two lines ensure that if now row is selected and we click the button, the function exits. No row selected returns -1 and is less than 0
            return

        dlg = SubjectDialog(self, self.data[current_row]) #if 2nd item was selected then current_row = 1 and self.data[1] will give the list ['Other Dummy Name', 1970, 'f', 'other symptoms']
        if dlg.exec_() == dlg.Accepted:
            self.data[current_row] = dlg.getData() 
            self.updateList()
        """
        This function checks which cell is selected and then deletes it and then updates the list
        """
    def onDeleteClicked(self):
        current_row = self.list.currentRow() #self.list.currentRow() returns 0 if 1st item is selected, 1 if 2nd is selected
        if current_row < 0:
            return

        del self.data[current_row] 
        self.updateList()
        """
        the QFileDialog opens a dialog box that allows the user to choose file from their system
        getOpenFileName gets the name of the file and then this function gets the data and saves the data in self.data
        updateList() then adds the data content to the screen (remember that updateList also has addIem function to show the data on the screen in the widget)
        """
    def onLoadClicked(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Load File") #the syntax: .getOpenFileName(parent, caption, directory='', filter=''). 
                                                                        #Passing self makes the dialog modal i.e it blocks interaction with parent window until everything is closed
                                                                        #caption is displayed on top left of the dialog window
                                                                        # if directory path is given, it opens that directly
                                                                        # filter is a string that specifies which type of files to be displayed for eg: filter="Text Files (*.txt);;All Files(*)"
                                                                        # since this all returns a tuple which is ('file path', 'the filter used')
                                                                        #in this case we receive the tuple ('path file', '') and we unpack it and we assign the '' to a placeholder _
        if filename:                                                    
            with open(filename, 'r') as f:
                self.data = [line.strip().split(',') for line in f.readlines()] #there can be multiple lines in the same file
                for subject in self.data:
                    subject[1] = int(subject[1])  # Convert year of birth to int cause it is in str form when previously saved
                self.updateList()

        """
        getSaveFileName helps u to save a file in ur pc. "Save File is the name u give to the dialog box
        we write the data in the following manner: name,YOB,symptoms,gender
        """
    def onSaveClicked(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save File")
        if filename:
            with open(filename, 'w') as f:
                for subject in self.data:
                    f.write(','.join(map(str, subject)) + '\n') 
    """
    Helps in drag and drop of the data hence rearranging them. After dragging and dropping data
    their arrangement needs to be updated in the self.data for which this function is created     
    """
    def onRowsMoved(self, parent, start, end, destination, row):
        moved_items = self.data[start:end + 1]
        del self.data[start:end + 1]
        self.data[row:row] = moved_items

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ListWindow()
    app.exec_()       
        