import cv2

from Rastreador import *

import os

# Ruta de la carpeta que quieres comprobar
folder_path = "./video/"

# Comprueba si tienes permiso de lectura en la carpeta
if os.access(folder_path, os.R_OK):
    print("Tienes permiso de lectura en la carpeta")
else:
    print("No tienes permiso de lectura en la carpeta")
    
# Crear objeto de seguimiento
seguimiento = Rastreador()

# realizamos la lectura del video
cap = cv2.VideoCapture('./video/autos.mp4')
if not cap.isOpened():
    print('Error al abrir el archivo de video')
    exit()

# realizamos la deteccion de objetos con camara estable
# cambiando tamaño de historial podemos tener mejores resultados (camara estatica)
# Tambien modificamos el umbral, entre menor sea mpas deteccion tendremos (Falsos Positivos)
deteccion = cv2.createBackgroundSubtractorMOG2(history=100000, varThreshold= 12) # Extrae los objetos en movimiento de una camara estatica


while True:
    ret, frame = cap.read()
    try:
        frame = cv2.resize(frame, (1200 , 720)) # Redimensionamiento del video
    except Exception:
        print("no se puede cambiar el tamaño")
    
    # Elegimos una zona de interes para centrar el paso de autos
    zona = frame[530:720, 300:850]
    
    # Creamos una mascara a los fotogramas con el fin de que los objetos sean blancos y el fondo negro
    mascara = deteccion.apply(zona)
    _, mascara = cv2.threshold(mascara, 254, 255 , cv2.THRESH_BINARY) # con este umbral eliminamos los pixeles grises
    contornos, _ = cv2.findContours(mascara, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detecciones = [] # Lista donde vamos a almacenar la info
    
    # Dibujamos los contornos en frame, de azul claro con 2 de grosor  
    for cont in contornos:
        # Eliminamos los contornos pequeños
        area = cv2.contourArea(cont)
        if area > 3000: # sAjustamos el area para que no reconozca objetos pequeños
            # cv2.drawContours(zona,[cont], -1, (255,255,0),2)
            x, y, ancho, alto = cv2.boundingRect(cont)
            cv2.rectangle(zona,(x, y), (x + ancho, y + alto),(255,255,0),3) # Dibujamos el rectangulo
            detecciones.append([x, y, ancho, alto]) # Almacenamos la informacipon de las detecciones
            
    # Seguimiento de los objetos
    info_id = seguimiento.rastreo(detecciones)
    for inf in info_id:
        x, y, ancho, alto, id = inf
        cv2.putText(zona, str(id), (x, y -15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2)
        cv2.rectangle(zona, (x, y), (x + ancho, y + alto) , (255, 255, 0), 3) # Dibujamos el rectangulo
        
    print(info_id)
    cv2.imshow('Carretera', frame)
    cv2.imshow('Zona de Interes',zona)
    cv2.imshow('Mascara', mascara)

    if not ret or cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
    



