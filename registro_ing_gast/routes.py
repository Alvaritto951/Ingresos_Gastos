from registro_ing_gast import app


@app.route("/index")
def index():
    return "Servidor funcionando"