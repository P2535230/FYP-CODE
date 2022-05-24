from ast import Import
import sys
from PyQt5.QtWidgets import QApplication
from CalendarAssistantGui import CalendarAssistantGui
#calling callendarAssistantGui
#to run the application

if __name__ == '__main__': 

    App = QApplication(sys.argv)
    
    #hardsetting the screensize
    window = CalendarAssistantGui(1280, 720)
    
    sys.exit(App.exec())
    
    
