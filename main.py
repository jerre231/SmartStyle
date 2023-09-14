from flask import *
from classes import Roupa, Usuario

roupas = []
usuarios = []

teste_user = Usuario('teste', '123')
roupa1 = Roupa('calça', 'g', 'verde', 'inverno', 'calça1')
roupas.append(roupa1)
usuarios.append(teste_user)


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

@app.route("/armario")
def planejador(user):
    pass

@app.route("/inserir")
def inserir_roupa(user):
    pass
        
@app.route("/planejador")
def planejador(user):
    pass

if __name__ == "__main__":
    app.run(debug=True)
