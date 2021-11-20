import Jetson.GPIO as GPIO
import sys
from PyQt5 import uic, QtWidgets, QtGui, QtCore 
from qtpy.QtCore import Qt, QFileSystemWatcher, QSettings, Signal
from GPIOESLocales import *
from VisionArtificial import *
import os


qtCreatorFile = "/home/jetson/VisionArtificial/ProyectoFinal/HMI.ui" # ruta del archivo HMI.ui aquí.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    event_detected = Signal(int)
    paro=Signal()
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        #Pantalla completa
        self.showFullScreen()
        
        #Botones HMI
        self.iniciar.clicked.connect(self.arranque)
        self.detener.clicked.connect(self.parohmi)
        self.close.clicked.connect(self.apagar)
        self.correccion.clicked.connect(self.correccion_hecha)
        
        #Boton LS
        GPIO.cleanup()
        conf_init_gpio()
        LS=33
        self.event_detected.connect(self.on_gpio_event)
        GPIO.add_event_detect(LS, GPIO.RISING, callback=self.event_detected.emit, bouncetime=80)
        
        self.paro.connect(self.parohmi)
        
    def arranque(self):
        self.state2.setPixmap(QtGui.QPixmap("/home/jetson/VisionArtificial/ProyectoFinal/verde.png"))
        global inicio
        inicio=1
        reiniciogpio()
            
    def on_gpio_event(self,LS):
        if inicio==1:
            tolerancia_box=self.tolerancia_box.value()
            tolerancia=51-51*tolerancia_box*.01
            scale1=self.scale_HMI.value()
            scale=50-49.9*scale1*.01
            resultado_malos=self.contador_NC.intValue()
            resultado_buenos=self.contador_PC.intValue()
            
            captura(scale)
            NC,PC,matchesorb=ORB_nano(tolerancia)
            
            self.ind_matches.display(matchesorb)
            self.comparacion_ventana.setPixmap(QtGui.QPixmap("/home/jetson/VisionArtificial/ProyectoFinal/comparacion.png"))
            if NC==0 and PC==1:
                self.state1.setPixmap(QtGui.QPixmap("/home/jetson/VisionArtificial/ProyectoFinal/pass.png"))
                resultado_buenos+=1
                self.contador_PC.display(resultado_buenos)
                # falla=secuencia_A()
                # if falla==1:
                #     self.paro.emit()
                    
            elif NC==1 and PC==0 :
                self.state1.setPixmap(QtGui.QPixmap("/home/jetson/VisionArtificial/ProyectoFinal/equis.png"))
                self.state3.setPixmap(QtGui.QPixmap("/home/jetson/VisionArtificial/ProyectoFinal/amarillo.png"))
                resultado_malos+=1
                self.contador_NC.display(resultado_malos)
                # falla=secuencia_B()
                # if falla==1:
                #     self.paro.emit()
    
    def apagar(self):
        quit()
        #os.system("shutdown now")
    
    def parohmi(self):
        self.state2.setPixmap(QtGui.QPixmap("/home/jetson/VisionArtificial/ProyectoFinal/rojo.png"))
        global inicio
        inicio=0
    
    def correccion_hecha(self):
        self.state3.setPixmap(QtGui.QPixmap("/home/jetson/VisionArtificial/ProyectoFinal/amarillo2.png"))
        GPIO.output(24,0)
        
if __name__ == "__main__":
    
    
    app =  QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())