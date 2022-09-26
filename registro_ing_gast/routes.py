from flask import render_template, request, redirect, url_for
import csv
from config import MOVIMIENTOS_FILE, NEW_FILE, LAST_ID_FILE
from registro_ing_gast import app
from registro_ing_gast.models import select_all, select_by, delete_by, insert, update_by
from datetime import date
import os #Es para poder Borrar (delete) y renombrar (rename)


@app.route("/index")
def index(): #Viene de models.py (from registro_ing_gast.models import select_all)
    return render_template("index.html", pageTitle="Lista", movements=select_all())


@app.route("/nuevo", methods=["GET", "POST"]) #Se indican los métodos de html para poder leer o publicar en la página web

#def nuevo(): Esto es solo para validar el formulario de fecha
#    if request.method == "GET":
#       return render_template("new.html", pageTitle="Alta") #Si el método es GET, muestra la página web de añadir datos (/nuevo)
#   else:
#       #Hacer validación --> librería datetime
#       if validaFecha(request.form['date']): #1º validar que request.form.date <= hoy
#           fichero = open(MOVIMIENTOS_FILE, 'a', newline='') #Si no, añade una línea más
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
#El dataForm va la html new.html y sirve para indicar un diccionario vacío para que dejemos el dato correcto en el campo que habíamos escrito
    else:
        #Hacer validación para todos los formularios
        """
        1º Validar el formulario
        Fecha válida y <= hoy
        2º Concepto no sea vacío
        3º Cantidad no sea 0 o vacía
        """
        #ERRORES --- ES MUY IMPORTANTE -- ANOTAR PARA POSTERIORES OCASIONES
        errores = validaFormulario(request.form)
        if not errores: #Viene de models.py (from registro_ing_gast.models import insert(registro))
            insert([request.form['date'],
                    request.form['description'],
                    request.form['quantity']])
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

def form_to_list(id, form): #En vez de escribir tantas veces la lista, lo devolvemos en forma de función, pasa el id y el formulario
    return [id, form['date'], form['description'], form['quantity']]

@app.route("/modification/<int:id>", methods=["GET", "POST"])
def modificacion(id):
    if request.method == "GET":
        """
        1º Consultar en movimientos.txt y recuperar el registro con id al de la petición
        2º Devolver el formulario html con los datos de mi registro
        """
        registro_definitivo = select_by(id) #1º Consultar en movimientos.txt y recuperar el registro con id al de la petición

        if registro_definitivo:
            return render_template("mod.html", registro=registro_definitivo, pageTitle="Actualizar/Modificar") #2º Devolver el formulario html con los datos de mi registro
        else:
            return redirect(url_for("index")) #Si no, llévame a index
    else:
        """
        1º Validar registro de entrada
        2º Si el registro es correcto, lo sustituyo en movimientos.txt. La mejor manera es copiar registro a registro en fichero nuevo y dar el cambiazo
        3º Redirect
        4º Si el registro es incorrecto, la gestión de errores que conocemos
        """
        errores = validaFormulario(request.form) #1º Validar registro de entrada
        
        if not errores:
            update_by(form_to_list(id, request.form)) #Viene de la función form_to_list
            #2º Si el registro es correcto, lo sustituyo en movimientos.txt (con la función que viene de models.py: update_by(id)).
            #La mejor manera es copiar registro a registro en fichero nuevo y dar el cambiazo

            return redirect(url_for("index")) #3º Redirect
        else:
            return render_template("mod.html", pageTitle="Actualizar/Modificar", msgErrors=errores,
             registro=form_to_list(id, request.form)) #Viene de la función form_to_list
             #4º Si el registro es incorrecto, la gestión de errores que conocemos
        

@app.route("/delete/<int:id>", methods=["GET", "POST"])
def eliminar(id):
    if request.method == "GET":
        """
        1º Consultar en movimientos.txt y recuperar el registro con id al de la peticion
        2º Devolver el formulario html con los datos de mi registro, no modificables
        3º Tendrá un botón que diga confirmar
        """
        #1º Consultar en movimientos.txt y recuperar el registro con id al de la peticion
        registro_definitivo = select_by(id) #Viene de models.py (from registro_ing_gast.models import select_by)
        if registro_definitivo:
            return render_template("delete.html", registro=registro_definitivo)
        else:
            return redirect(url_for("index")) #url_for(def index) entre comillas se transforma en "/"

        
    else:
        """
        Borrar el registro
        1. Abrir fichero movimientos.txt en lectura
        2. abrir fichero new_movimiento.txt en escritura
        3. copiar todos los registros uno a uno en su orden exceptuando el que queremos borrar
        4. borrar movimientos.txt
        5. renombrar nmovimientos.txt a movimientos.txt
        """
        delete_by(id) #Viene de models.py (from registro_ing_gast.models import delete_by(id))
        return redirect(url_for("index"))
        

    

