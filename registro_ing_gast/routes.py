from flask import render_template
from registro_ing_gast import app


@app.route("/index")
def index():
    return render_template("index.html", pageTitle="Lista", movimientos=[])


@app.route("/nuevo")
def nuevo():
    return render_template("new.html", pageTitle="Alta")