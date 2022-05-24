from decimal import setcontext
import functools
import operator
import time
import os
from turtle import width
from xml.dom import UserDataHandler
from xml.etree.ElementTree import tostring
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from matplotlib import widgets
from PyQt5.QtWidgets import *       #Importing all of the Libraries 
from PyQt5.QtGui import QPixmap     #that are needed for this project
#from show_events import show_events
import re
from datetime import datetime 

class CalendarAssistantGui(QMainWindow):
 
    def __init__(self, w, h) -> None: #double underscore means prewritten function, to not be confused with functions that i wrote myself
        super().__init__()  #single undersocre means selfwritten function

        self.setWindowTitle("CAGE")              #Title of the window appearing in the left hand corner
        self.setWindowIcon(QIcon("icon.png"))    #Icon of the window appearing in the left hand corner
        
                
        self.height = h
        self.width = w
        
        #building gui
        self.setGeometry(100, 100, self.width, self.height)
        self.setFixedSize(w, h)
        self.center_window()                  
        self.eventbox = QTextEdit(self) 
        self.closeCoursework(self.eventbox)
        self.updateDeadline(self.deadlineBox)
        self.show()
    
    #Using date and time to establish current week
    def same_week(self,dateString):
        last_on = dateString.rfind(' on ')
        last_at = dateString.rfind(' at ')
        last_by = dateString.rfind(' by ')
        date1 = dateString[last_on+4:last_at]
        time1 = dateString[last_at+4:last_by] 
        datetime2 = "{} {}".format(date1, time1)     
        '''returns true if a dateString in %Y%m%d format is part of the current week'''
        d1 = datetime.strptime(datetime2,'%d/%m/%Y %H:%M')
        d2 = datetime.today()
        return d1.isocalendar()[1] == d2.isocalendar()[1] \
                and d1.year == d2.year       
    
    #Using function above to establish current weeks deadlines 
    def updateDeadline(self, deadlineBox):
        self.deadlineBox.clear()
        counter = 0
        with open('userdata.txt') as f:
                alllines = f.readlines()
        sortedLines = self.sortDates(alllines)
        for line in sortedLines:
            if self.same_week(line):
                counter = counter + 1
        self.deadlineBox.append("You have {} deadlines this week!".format(counter))
    
        
    #reading deadline database stored in a .txt file
    #to populate eventbox 
    #with the nearest 5 deadlines
    def closeCoursework(self,eventbox):
        self.eventbox.clear()
        alllines = []
        with open('userdata.txt') as f:
                alllines = f.readlines()
        sortedLines = self.sortDates(alllines)
        firstfivelines = sortedLines[:5]
        for line in firstfivelines:  
             self.eventbox.append(line)
        self.drawComponents(self.eventbox)  
    

    #data selection algorithm
    #uses hard coded keywords 
    #to split user input string to populate data base with added deadlines
    
    def sortDates(self,alllines):
        # We go through the list as many times as there are elements
        for i in range(len(alllines)):
            # We want the last pair of adjacent elements to be (n-2, n-1)
            for j in range(len(alllines) - 1):
                last_on = alllines[j].rfind(' on ')
                last_at = alllines[j].rfind(' at ')
                last_by = alllines[j].rfind(' by ')
                date1 = alllines[j][last_on+4:last_at]
                time1 = alllines[j][last_at+4:last_by]
                last_on = alllines[j+1].rfind(' on ')
                last_at = alllines[j+1].rfind(' at ')
                last_by = alllines[j+1].rfind(' by ')
                date2 = alllines[j+1][last_on+4:last_at]
                time2 = alllines[j+1][last_at+4:last_by]                
                if self.soonerDate(date1,time1,date2,time2):
                    # Swap
                    alllines[j], alllines[j+1] = alllines[j+1], alllines[j]
        return alllines
            
    #going through submission dates to arrange 
    #nearest deadlines in the eventbox
    def soonerDate(self,date1,time1,date2,time2):
        global datetime_object2,datetime_object1
        datetime1 = "{} {}".format(date1, time1)
        datetime2 = "{} {}".format(date2, time2)
        print(datetime1,datetime2)
        datetime_object1 = datetime.strptime(datetime1, '%d/%m/%Y %H:%M')
        datetime_object2 = datetime.strptime(datetime2, '%d/%m/%Y %H:%M')

        return datetime_object1 > datetime_object2        

    
     #building gui parameters (location of objects on screen)  
    def drawComponents(self,eventbox):
        
       #template for accessibility
        instructional_text ='Please enter an event in this format: <Description> on <DD/MM/YY> at <HH:MM> by <NAME/SURNAME>'

        self.input_bar = QLineEdit(self)

        self.input_bar.setPlaceholderText(instructional_text)
        self.addbtn = QPushButton("Add event", self)
        self.showbtn = QPushButton("Show events", self)
        
        # creating label
        self.label = QLabel(self)
        self.deadlineBox = QTextEdit(self)
        self.deadlineBox.setStyleSheet("background-color: red")                             
        
        self.deadlineBox.setGeometry(self.width*0.63, self.height*0.65, 200,150)
        #self.deadlineBox.setTextColor("color: white")
        #self.deadlineBox.setStyleSheet("color: white(255, 255, 255);")
 
        
        # loading image
        self.pixmap = QPixmap('Searchbar.png')
 
        # adding image to label
        self.label.setPixmap(self.pixmap)
 
        # Optional, resize label to image size
        self.label.setGeometry(self.width*0.43, self.height*0.15, self.width*0.5, 50)
 
        self.eventbox.setGeometry(self.width*0.2, self.height*0.65, 500, 150)
       
        self.input_bar.setGeometry(self.width*0.2, self.height*0.3, self.width*0.6, 40)
        self.addbtn.setGeometry(self.width*0.33, self.height*0.45, self.width*0.15, 40)
        self.showbtn.setGeometry(self.width*0.53, self.height*0.45, self.width*0.15, 40)
        
        self.addbtn.clicked.connect(self.add_event)
        self.showbtn.clicked.connect(self.show_event)
        
        

    #opening the database to display all valid entries
    def show_event(self):
     print("pressed")
     if(len(self.input_bar.text()) > 1):
        print(self.input_bar.text())
        self.input_bar.setText('')
        with open("userdata.txt", "r") as f:
            lines = f.readlines()
    
    #user input validation based on keywords
    #if invalid input detected deletes input
    def checkValid(self):
        entry = self.input_bar.text()
        if(len(entry) < 15): # unreasonably small entry considering keywords length
            return False # not valid
        if not (' on ' in entry and ' at ' in entry and ' by ' in entry): # necessary keyword
            return False
    
        last_on = entry.rfind(' on ')
        last_at = entry.rfind(' at ')
        last_by = entry.rfind(' by ')
        description = entry[:last_on]
        date = entry[last_on+4:last_at]
        inputdate = datetime.strptime(date, "%d/%m/%Y")
        present = datetime.now()
        if inputdate.date() < present.date():
            return False
        if(date):
            time= entry[last_at+4:]
        return True
        
        
    #calls checkValid with user input string
    #to validate entry
    #if checkValid returns true
    #user entry is added to the database
    def add_event(self,eventbox):
        entry = self.input_bar.text()
        entry.upper()
        if self.checkValid():
            with open('userdata.txt', 'a+') as f:
                f.write(entry + "\n")
        self.input_bar.setText('')
        self.closeCoursework(self.eventbox)
        self.updateDeadline(self.deadlineBox)
 
   #sopens text file after 1 second delay to make transition smoother
    def show_event(self): 
        time.sleep(0.1)
        os.system("start "+"userdata.txt")

     #when program runs 
     #gets opened in the centre of the screen
    def center_window(self):
        current_position = self.frameGeometry()
        center_of_desktop = QDesktopWidget().availableGeometry().center()
        current_position.moveCenter(center_of_desktop)
        self.move(current_position.topLeft())
        
        

# ' '.join(text.split())
