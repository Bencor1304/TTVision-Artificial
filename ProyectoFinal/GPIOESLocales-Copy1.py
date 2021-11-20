import Jetson.GPIO as GPIO
import time
from main import paroh

def conf_init_gpio():
    #Configuracion inicial 
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    #Entradas
    GPIO.setup(7,GPIO.IN)  # Sensor SA1
    GPIO.setup(11,GPIO.IN) # Sensor SA2
    GPIO.setup(13,GPIO.IN) # Sensor SB1
    GPIO.setup(15,GPIO.IN) # Sensor SB2
    GPIO.setup(19,GPIO.IN) # Sensor SC1
    GPIO.setup(21,GPIO.IN) # Sensor SC2
    GPIO.setup(23,GPIO.IN) # Sensor SD1
    GPIO.setup(29,GPIO.IN) # Sensor SD2
    GPIO.setup(31,GPIO.IN) # Sensor BS
    GPIO.setup(33,GPIO.IN) # Sensor LS1
    GPIO.setup(35,GPIO.IN) # Paro de emergencia
    # Salidas
    GPIO.setup(40,GPIO.OUT)  # Electrovalvula YA1
    GPIO.setup(38,GPIO.OUT)  # Electrovalvula YB1
    GPIO.setup(36,GPIO.OUT)  # Electrovalvula YC1
    GPIO.setup(32,GPIO.OUT)  # Electrovalvula YD1
    GPIO.setup(26,GPIO.OUT)  # Indicador Led YL1 (verde)
    GPIO.setup(24,GPIO.OUT)  # Indicador Led YL2 (amarillo)
    GPIO.setup(22,GPIO.OUT)  # Indicador Led YL3 (rojo)

# funcion falla 
def falla():
    BS=GPIO.input(31)
    BS_PARO=0
    timer_BS=0
    while BS==1 and BS_PARO==0:
        BS=GPIO.input(31)
        time.sleep(1)
        timer_BS=timer_BS+1
        if timer_BS>=10:
            BS_PARO=1
        else:
            BS_PARO=0
            
    PE=GPIO.input(35)
    
    if PE==1 or BS_PARO==1 or paroh==1:
        falla_activa=1
    else :
        falla_activa=0
    return falla_activa
    
#Secuencia de Emergencia
def secuencia_emergencia():
    GPIO.output(36,1)
    GPIO.output(22,1)

#Secuencia A
def secuencia_A(PC):
    estado=0
    falla_activa=0
    
    while estado==0 and falla_activa==0:         #YC1- (NA)
        print('Secuencia A')
        SA1=GPIO.input(7)
        SC2=GPIO.input(21)
        LS1=GPIO.input(33)
        falla_activa=falla()
        if PC==1 and SA1==1 and SC2==1 and LS1==1 and falla_activa==0:
            GPIO.output(36,1)
            estado=GPIO.input(36)
    
    estado=0
    while estado==0 and falla_activa==0:        #YA+
        
        SC1=GPIO.input(19)
        falla_activa=falla()
        if SC1==1 and falla_activa==0 :
            GPIO.output(40,1)
            estado=GPIO.input(40)
    
    estado=1
    while estado==1 and falla_activa==0:       #YA-
        
        SA2=GPIO.input(11)
        falla_activa=falla()
        if SA2==1 and falla_activa==0 :
            GPIO.output(40,0)
            estado=GPIO.input(40)
    
    estado=1
    while estado==1 and falla_activa==0:       #YC1+ (NA)
        
        SA1=GPIO.input(7)
        LS1=GPIO.input(33)
        falla_activa=falla()
        if SA1==1 and LS1==0 and falla_activa==0 :
            GPIO.output(36,0)
            estado=GPIO.input(36)
            
    return falla_activa,estado        

#Secuencia B
def secuencia_B(NC):
    estado=0
    falla_activa=0
    while estado==0 and falla_activa==0:         #YB1+
        
        SB1=GPIO.input(13)
        SC2=GPIO.input(21)
        falla_activa=falla()
        if NC==1 and SB1==1 and SC2==1 and falla_activa==0:
            GPIO.output(38,1)
            estado=GPIO.input(38)
    
    estado=0
    while estado==0 and falla_activa==0:        #YB1- YD1+
        
        SB2=GPIO.input(15)
        SD1=GPIO.input(23)
        falla_activa=falla()
        if SB2==1 and SD1==1 and falla_activa==0 :
            GPIO.output(38,0)
            GPIO.output(32,1)
            estado=GPIO.input(32)
    
    estado=1
    while estado==1 and falla_activa==0:         #YD1-
        
        SD2=GPIO.input(29)
        falla_activa=falla()
        if SD2==1 and falla_activa==0:
            GPIO.output(32,0)
            estado=GPIO.input(32)
            
    return falla_activa,estado     

#Reinicio 
def reiniciogpio():
    GPIO.output(40,0) #YA1
    GPIO.output(38,0) #YB1
    GPIO.output(36,0) #YC1
    GPIO.output(32,0) #YD1
    GPIO.output(26,0) #YL1 (VERDE)
    GPIO.output(24,0) #YL2 (AMARILLO)
    GPIO.output(22,0) #YL3 (ROJO)

#Inicio LS
def inicio():
    estado=0
    falla_activa=0
    while estado==0 and falla_activa==0:        #LS
        
        LS1=GPIO.input(33)
        falla_activa=falla()
        if LS1==1 and falla_activa==0 :
            LS1=1
            estado=1
    return LS1

if __name__ == '__main__':

    conf_init_gpio()
    falla()
    secuencia_emergencia()
    secuencia_A(PC)
    secuencia_B(NC)
    reiniciogpio()
    inicio()