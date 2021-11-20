import cv2
#Toma foto
def captura(scale):
    camera = cv2.VideoCapture(0)
    
    for i in range(5):                           #Tiempo de apertura de la camara 
        return_value, image = camera.read()    
    cv2.imwrite('/home/jetson/VisionArtificial/ProyectoFinal/captura.png', image)
    zoom(image,scale)
    del(camera)
    return

#ZOOM
def zoom(image,scale):
    height, width, channels = image.shape       #medir dimensión de la imagen
    centerX,centerY=int(height/2),int(width/2)  #centro de la imagen
    radiusX,radiusY= int(scale*height/100),int(scale*width/100) #radio de la imagen

    minX,maxX=centerX-radiusX,centerX+radiusX   #Marco de la imagen recortada
    minY,maxY=centerY-radiusY,centerY+radiusY

    cropped = image[minX:maxX, minY:maxY]       #Imagen original solo mostrando el marco 
    imagen_zoom = cv2.resize(cropped, (width, height)) 
    imagen_gris=grises(imagen_zoom)
    cv2.imwrite('/home/jetson/VisionArtificial/ProyectoFinal/capturazoomgris.png', imagen_gris)
    
#Escala de grises 
def grises(imagen_zoom):
    imagen_gris = cv2.cvtColor(imagen_zoom, cv2.COLOR_BGR2GRAY)
    return imagen_gris

#ORB
def ORB_nano(tolerancia):
    img1=cv2.imread('/home/jetson/VisionArtificial/ProyectoFinal/capturazoomgris.png')
    img2=cv2.imread('/home/jetson/VisionArtificial/ProyectoFinal/capturabase.png')
    #ORB descriptor
    orb = cv2.ORB_create()
    #Encuentra los descriptores con ORB
    kp1, des1 = orb.detectAndCompute(img1,None)
    kp2, des2 = orb.detectAndCompute(img2,None)
    #Encuentra los descriptores comunes entre ambas imagenes
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2,k=2)
    #Distancia entre descriptores tolerada
    good = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:      #Lowe ratio
            good.append([m])
    #impresion del resultado
    matchesorb = (len(good))
    if matchesorb>=tolerancia:
        PC=1
        NC=0
    else:
        NC=1
        PC=0

    img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    cv2.imwrite('/home/jetson/VisionArtificial/ProyectoFinal/comparacion.png', img3)
    
    return NC, PC, matchesorb

if __name__ == '__main__':

    captura(scale)
    zoom()
    grises()
    ORB_nano()

