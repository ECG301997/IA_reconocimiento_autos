import math

#---------------- Clase Rastreador-----------------#
class Rastreador:
    
    def __init__(self):
        # almacenamiento de posiciones
        self.centro_puntos= {}
        # contador de objetos
        self.id_count = 1
        
    def rastreo(self,objetos):
        # Almacenamiento de objetos identificados
        objetos_id = []
        
        #Obtener punto central del nuevo objeto
        for rect in objetos:
            x, y, w, h = rect
            cx = (x + x + w ) // 2
            cy = (y + y + h ) // 2
            
            # Verificamos si el objeto ya fue detectado      
            objeto_det = False
            for id, pt in self.centro_puntos.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])
                
                if dist < 25:
                    self.centro_puntos[id] = (cx , cy)
                    print(self.centro_puntos)
                    objetos_id.append([x, y, w, h, id])
                    objeto_det = True
                    break
                
            # Asignación id de objeto
            if objeto_det is False:
                self.centro_puntos[self.id_count] = (cx , cy) # Almacenamos coordenada x, y
                objetos_id.append([x, y, w, h, self.id_count]) # Agregamos el objeto con ID
                self.id_count = self.id_count + 1 # Aumentamos el ID   
                
        # Limpiamos la lista de puntos centrales para eliminar los ID que no se usan
        new_center_points = {}
        for obj_bb_id in objetos_id:
            _, _, _, _, object_id = obj_bb_id
            center = self.centro_puntos[object_id]
            new_center_points[object_id] = center
            
        # Actualizar lista con ID no usados eliminados
        self.centro_puntos = new_center_points.copy()
        return objetos_id
            
            
        