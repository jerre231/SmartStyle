from flask import *
from classes import *

app == Flask(__name__)

@app.route("/login")
def login():        
    pass

@app.route("/cadastro")
def cadastro():
    pass

@app.route("/home")
def cadastro(user):
    pass

@app.route("/inserir")
def inserir_roupa(user):
    pass
        
@app.route("/planejador")
def planejador(user):
    pass

if __name__ == "__main__":
    app.run(debug=True)
