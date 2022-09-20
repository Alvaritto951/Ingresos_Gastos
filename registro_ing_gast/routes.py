from flask import render_template, request, redirect
import csv
from registro_ing_gast import app
from datetime import date


@app.route("/index")
def index():
    fichero = open("data/movimientos.txt", "r", encoding='utf-8') #Abrir el fichero movimientos.txt desde la carpeta data --- Añadir encoding='utf-8' para que salgan las tíldes
    csvReader = csv.reader(fichero, delimiter=',', quotechar='"') #Transforma el contenido del archivo txt y lo procesa como si fuera un csv
    movimientos = [] #Creamos lista
    for movimiento in csvReader: #Dentro del archivo csv y cada uno de los datos,
        movimientos.append(movimiento) #Añadir dato a la lista [movimientos]
    
    # movimientos = [movimiento for movimiento in csvReader]  ---- list comprehension --- Es lo mismo que la lista movimientos -- L10, 11 & 12

    fichero.close()
    return render_template("index.html", pageTitle="Lista", movements=movimientos)


@app.route("/nuevo", methods=["GET", "POST"]) #Se indican los métodos de html para poder leer o publicar en la página web
#def nuevo(): Esto es solo para validar el formulario de fecha
#    if request.method == "GET":
#       return render_template("new.html", pageTitle="Alta") #Si el método es GET, muestra la página web de añadir datos (/nuevo)
#   else:
#       #Hacer validación --> librería datetime
#       if validaFecha(request.form['date']): #1º validar que request.form.date <= hoy
#           fichero = open("data/movimientos.txt", 'a', newline='') #Si no, añade una línea más
#           csvWriter = csv.writer(fichero, delimiter=",", quotechar='"') #Lee el archivo txt y lo procesa de tal manera que se pueda escribir
#
#           csvWriter.writerow([request.form['date'], request.form['description'], request.form['quantity']]) #Se añade/escribe en el txt
#           fichero.close()
#
#           return redirect("/index") #Y lo redirige al documento index si es correcto.
#       else:
#           return render_template("new.html", pageTitle="Alta") #Si no es correcto, hay que volver a introducir los datos

#def validaFecha(fechaEntrada):
#    hoy = str(date.today())
#    #Alternativa: hoy = date.today().isoformat() -- Te hace una cadena
#    return fechaEntrada <=hoy

def nuevo():
    if request.method == "GET": #Si el método es GET, muestra la página web de añadir datos (/nuevo)
        return render_template("new.html", pageTitle="Alta", dataForm={})
#El dataForm va la html new.html y sirve para indicar un diccionario vacío para que dejemos el dato correcto que en el campo que habíamos escrito
    else:
        #Hacer validación para todos los formularios
        """
        1º Validar el formulario
        Fecha válida y <= hoy
        2º Concepto no sea vacío
        3º Cantidad no sea 0 o vacía
        """
        errores = validaFormulario(request.form)
        if not errores: #1º validar --- Si no hay errores, se añade línea
            fichero = open("data/movimientos.txt", 'a', newline='') #Si no, añade una línea más
            csvWriter = csv.writer(fichero, delimiter=",", quotechar='"') #Lee el archivo txt y lo procesa de tal manera que se pueda escribir

            csvWriter.writerow([request.form['date'], request.form['description'], request.form['quantity']]) #Se añade/escribe en el txt
            fichero.close()

            return redirect("/index") #Y lo redirige al documento index si es correcto.
        else:
            return render_template("new.html", pageTitle="Alta", msgErrors=errores, dataForm=dict(request.form)) #Si no es correcto, hay que volver a introducir los datos

def validaFormulario(camposFormulario):
    errores = [] #Se crea una lista vacía para ir añadiendo errores
    hoy = date.today().isoformat() #Se convierte en cadena con el formato ISO (YYYY-MM-DD)
    if camposFormulario['date'] > hoy: #Si los datos introducidos en el campo de formulario de fecha son mayores a hoy
        errores.append("La fecha introducida es el futuro, introduce la fecha actual o una anterior")
    
    if camposFormulario['description'] == "": #Si no escribes nada en el campo descripción
        errores.append("Introduce un concepto para la transacción.")
    
    if camposFormulario ['quantity'] == "" or float(camposFormulario['quantity']) == "0.0": #Si está vacío o es cero
        errores.append("Introduce una cantidad positiva o negativa")
    
    return errores



@app.route("/modification")
def modificacion():
    return render_template("mod.html", pageTitle="Modificación")

@app.route("/delete")
def eliminar():
    return render_template("delete.html", pageTitle="Eliminado")

