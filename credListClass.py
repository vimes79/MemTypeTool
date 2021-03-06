from PyQt4.QtGui import *
from PyQt4.QtCore import *

class credItem(QWidget):
    """This class creates a credential item widget"""

    position = 0 #Position on the credential list
    upClicked = pyqtSignal(int)
    downClicked = pyqtSignal(int)
    deleteClicked = pyqtSignal(int)
    openClicked = pyqtSignal(int)

    #Constructor
    def __init__(self,crd):
        super(QWidget,self).__init__() #Call super class constructor

        #Create the elements of the credential
        self.crdLabel = QLabel(crd)
        self.dltIcon = QLabel()
        self.dltIcon.setPixmap(QPixmap("img/trashcan.png"))
        self.dltIcon.setAlignment(Qt.AlignRight)
        self.dltIcon.mousePressEvent = self.deletePressEvent
        self.upIcon = QLabel()
        self.downIcon = QLabel()
        self.upIcon.setPixmap((QPixmap("img/up.png")))
        self.upIcon.mousePressEvent = self.upPressEvent
        self.downIcon.setPixmap((QPixmap("img/down.png")))
        self.downIcon.mousePressEvent = self.downPressEvent

        #Create Arrow Layout
        self.posLayout = QVBoxLayout()
        self.posLayout.addWidget(self.upIcon)
        self.posLayout.addWidget(self.downIcon)

        #Create the main Layout
        self.crdLayout = QHBoxLayout()
        self.crdLayout.addLayout(self.posLayout)
        self.crdLayout.addWidget(self.crdLabel)
        self.crdLayout.addWidget(self.dltIcon)
        #Create the main widget
        self.mainWidget = QWidget()
        self.mainWidget.setStyleSheet("background-color:white;")
        self.mainWidget.setLayout(self.crdLayout)

        #Create the Self layout
        self.selfLayout = QVBoxLayout()
        self.selfLayout.addWidget(self.mainWidget)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.selfLayout)
        self.mainLayout.addStretch(1)
        self.setLayout(self.mainLayout)

    def mousePressEvent(self,event):
        self.openClicked.emit(self.position)
    def deletePressEvent(self,event):
        self.deleteClicked.emit(self.position)
    def upPressEvent(self,event):
        self.upClicked.emit(self.position)
    def downPressEvent(self,event):
        self.downClicked.emit(self.position)

class credList(QWidget):
    """This class creates the main credentials list"""


    newCredential = pyqtSignal()
    upClicked = pyqtSignal(int)
    downClicked = pyqtSignal(int)
    deleteClicked = pyqtSignal(int)
    openClicked = pyqtSignal(int)

    #Constructor
    def __init__(self,crdList=()):
        super(QWidget,self).__init__() #Call super class constructor

        #Create credList container widget
        self.credWidget = QWidget()
        #Create credList Layout
        self.credLayout = QVBoxLayout()
        #Add credentials to the layout
        for i,crd in enumerate(crdList):
            self.addCredential(crd.name,i)

        self.credWidget.setLayout(self.credLayout)


        #Scroll Area Properties
        self.scroll = QScrollArea()
        self.scroll.setAlignment(Qt.AlignTop)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setAlignment(Qt.AlignCenter)
        self.scroll.setWidget(self.credWidget)


        #Add new credential button
        self.newCred = QToolButton()
        self.newCred.setText("New")
        self.newCred.clicked.connect(self.addNewCredential)
        self.newCred.setIcon(QIcon("img/newcred.png"))

        #Scroll Area Layer add 
        self.vLayout = QVBoxLayout()
        self.vLayout.addWidget(self.scroll)
        self.vLayout.addWidget(self.newCred)
        self.setLayout(self.vLayout)

    def addNewCredential(self):
        self.newCredential.emit()

    def addCredential(self,crd,pos):
        """method to add a new credential to the list"""

        self.credential = credItem(crd)
        self.credential.position = pos
        self.credential.deleteClicked.connect(self.deletePress)
        self.credential.openClicked.connect(self.mousePress)
        self.credLayout.addWidget(self.credential)
        self.credWidget.adjustSize()


    def clearCredentials(self):
        """method for deleting all credentials in the list"""

        for i in reversed(range(self.credLayout.count())):
            self.credLayout.itemAt(i).widget().setParent(None)


    def mousePress(self,position):
        self.openClicked.emit(position)
    def deletePress(self,position):
        self.deleteClicked.emit(position)
    def upPress(self,position):
        self.upClicked.emit(position)
    def downPress(self,position):
        self.downClicked.emit(position)

