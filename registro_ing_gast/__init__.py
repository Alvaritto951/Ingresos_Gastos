from flask import Flask #1º

app = Flask(__name__) #2º

from registro_ing_gast.routes import * #3º - De routes, impórtame todo (*)
