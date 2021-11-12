#!/usr/bin/env python
# coding: utf-8

# In[ ]:

# In[ ]:
from GPIOESLocales import *
from VisionArtificial import *

conf_init_gpio()
estado=0
while estado==0:
    iniciar=inicio()
    if iniciar==1 :
        captura(scale=30)
        NC,PC =ORB_nano()
        estado=1
        
if NC==1:
    secuencia_B(NC)
elif PC==1:
    secuencia_A(PC)