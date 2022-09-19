from flask import render_template, request, redirect
import csv
from registro_ing_gast import app


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
def nuevo():
    if request.method == "GET":
        return render_template("new.html", pageTitle="Alta") #Si el método es GET, muestra la página web de añadir datos (/nuevo)
    else:
        fichero = open("data/movimientos.txt", 'a', newline='') #Si no, añade una línea más
        csvWriter = csv.writer(fichero, delimiter=",", quotechar='"') #Lee el archivo txt y lo procesa de tal manera que se pueda escribir

        #Hacer validación --> librería datetime
        #1º validar que request.form.date <= hoy
        #2º si date es > hoy, devolver form vacío

        csvWriter.writerow([request.form['date'], request.form['description'], request.form['quantity']]) #Se añade/escribe en el txt
        fichero.close()
        return redirect("/index") #Y lo redirige al documento index


@app.route("/modification")
def modificacion():
    return render_template("mod.html", pageTitle="Modificación")

@app.route("/delete")
def eliminar():
    return render_template("delete.html", pageTitle="Eliminado")

