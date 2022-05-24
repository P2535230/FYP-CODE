#importing the same libraries that the rest of the code uses
from turtle import width
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from matplotlib import widgets 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap

#presetting show event

class show_events(QWindow):
    
    def showEvent(self, a0: QShowEvent) -> None:
        return super().showEvent(a0)
    
    
