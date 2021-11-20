import Jetson.GPIO as GPIO
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
    return
# funcion falla 
def falla():
    
    BS=GPIO.input(31)     #Lectura pin sensor BS
    BS_paro=0             #Indicador de BS activo por mas de 10s
    if  BS==1 :
        BS=31
        BS=GPIO.wait_for_edge(BS,GPIO.FALLING,timeout=10000) #Espera de cambio de 1 a 0
        if BS==None:
            BS_paro=1
        else:
            BS_paro=0

    PE=GPIO.input(35)     #Lectura pin Boton de paro de emergencia
    
    if PE==1 or BS_paro==1 :
        falla_activa=1
    else :
        falla_activa=0   
    return falla_activa  #Indicador de paro por PE o BS
#Secuencia de Emergencia
def secuencia_emergencia():
    GPIO.output(36,1)
    GPIO.output(22,1) #YL3 (Rojo) on 
    GPIO.output(26,0) #YL1 (VERDE) off
    return
#Secuencia A
def secuencia_A():
    GPIO.output(26,1)                           #YL1 (VERDE) on
    
    estado=0
    falla_activa=0
    
    while estado==0 and falla_activa==0:         #YC1- (NA)
        SA1=GPIO.input(7)
        SC2=GPIO.input(21)
        LS1=GPIO.input(33)
        falla_activa=falla()
        if SA1==1 and SC2==1 and LS1==1 and falla_activa==0:
            GPIO.output(36,1)
            estado=GPIO.input(36)               #Estado de la salida YC1
    
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
    if falla_activa==1:
        secuencia_emergencia()
        return falla_activa
    GPIO.output(26,0)                         #YL1 (VERDE) off
    return falla_activa
#Secuencia B
def secuencia_B():
    GPIO.output(24,1)                        #YL2 (AMARILLO) on
    
    estado=0
    falla_activa=0
    while estado==0 and falla_activa==0:         #YB1+
        
        SB1=GPIO.input(13)
        SC2=GPIO.input(21)
        falla_activa=falla()
        if SB1==1 and SC2==1 and falla_activa==0:
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
            
    if falla_activa==1:
        secuencia_emergencia()
        return falla_activa 
    return falla_activa

#Reinicio 
def reiniciogpio():
    GPIO.output(40,0) #YA1
    GPIO.output(38,0) #YB1
    GPIO.output(36,0) #YC1
    GPIO.output(32,0) #YD1
    GPIO.output(26,0) #YL1 (VERDE)
    GPIO.output(24,0) #YL2 (AMARILLO)
    GPIO.output(22,0) #YL3 (ROJO)
    return
if __name__ == '__main__':
    conf_init_gpio()
    falla()
    secuencia_emergencia()
    secuencia_A(PC)
    secuencia_B(NC)
    reiniciogpio()