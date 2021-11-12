#!/usr/bin/env python
# coding: utf-8

# In[ ]:

# In[ ]:

# conf_init_gpio()
# estado=0
# while estado==0:
#     iniciar=inicio()
#     if iniciar==1 :
#         captura(scale=30)
#         NC,PC =ORB_nano()
#         estado=1
        
# if NC==1:
#     secuencia_B(NC)
# elif PC==1:
#     secuencia_A(PC)
import sys
from PyQt5 import uic, QtWidgets
from GPIOESLocales import *
from VisionArtificial import *

qtCreatorFile = "HMI.ui" # Nombre del archivo aquí.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.captura)
    def captura(self):
        captura(scale=30)
if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())