from config import MOVIMIENTOS_FILE, NEW_FILE, LAST_ID_FILE
import csv
import os

def select_all():
    """
    Devolverá una lista con todos los registros (lista vacía) del fichero MOVIMIENTOS_FILE
    """
    fichero = open(MOVIMIENTOS_FILE, "r", encoding='utf-8') #Abrir el fichero movimientos.txt desde la carpeta data --- Añadir encoding='utf-8' para que salgan las tíldes
    csvReader = csv.reader(fichero, delimiter=',', quotechar='"') #Transforma el contenido del archivo txt y lo procesa como si fuera un csv
    movimientos = [] #Creamos lista
    for movimiento in csvReader: #Dentro del archivo csv y cada uno de los datos,
        movimientos.append(movimiento) #Añadir dato a la lista [movimientos]
    
    # movimientos = [movimiento for movimiento in csvReader]  ---- list comprehension --- Es lo mismo que la lista movimientos -- L10, 11 & 12

    fichero.close()
    return movimientos
    

def select_by(id):
    """
    Devolverá un registro con el id de la entrada o vacío si no lo encuentra
    """
    fichero = open(MOVIMIENTOS_FILE, 'r', newline='') #Abre el txt
    csvReader = csv.reader(fichero, delimiter=",", quotechar='"')
    registro_definitivo = []
    for registro in csvReader: 
            if registro[0] == str(id): #Posición inicial es igual a string del id, que no acepta enteros
                registro_definitivo = registro
                break
    fichero.close()

    return registro_definitivo
    

def delete_by(id):
    """
    Borrará el registro cuyo id coincide con el de la entrada
    """
    fichero_old = open(MOVIMIENTOS_FILE, "r")
    fichero = open(NEW_FILE, "w", newline="")

    csvReader = csv.reader(fichero_old, delimiter=",", quotechar='"')
    csvWriter = csvWriter = csv.writer(fichero, delimiter=",", quotechar='"')          
    for registro in csvReader:
        if registro[0] != str(id):
            csvWriter.writerow(registro)
    
    fichero_old.close()
    fichero.close()

    os.remove(MOVIMIENTOS_FILE) 
    os.rename(NEW_FILE, MOVIMIENTOS_FILE) #Importado de la libreria os, que new_file pase a llamarse movimientos_file
    

def createId(): #Creará un id, el último registro creado.
    fichero = open(LAST_ID_FILE, 'r') #Se consulta el txt donde se encuentra el último registro
    registro = fichero.read() #Leer el documento
    id = int(registro) + 1 #Al último id se le añade una posición
    fichero.close()

def saveLastId(id): #Guarda el último id
    fichero = open(LAST_ID_FILE, "w")
    fichero.write(str(id))
    fichero.close()

def insert(registro): #Inserta el último registro y te suma uno más
    """
    Creará un nuevo registro, siempre y cuando registro sea compatible con el fichero.
    Asignará al registro un id único (acumulativo)
    """
    id = createId()
    fichero = open(MOVIMIENTOS_FILE, 'a', newline='') #Añade una línea más
    csvWriter = csv.writer(fichero, delimiter=",", quotechar='"') #Lee el archivo txt y lo procesa de tal manera que se pueda escribir

    #2. El nuevo id sera el id del último registro + 1
    csvWriter.writerow(["{}".format(id), registro[0], registro[1], registro[2]]) #Se añade/escribe en el txt
    #Otra forma: csvWriter.writerow([f"{id}] + registro)
    fichero.close()

    saveLastId(id)

