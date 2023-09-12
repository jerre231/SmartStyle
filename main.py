from flask import Flask, render_template, request, redirect
from classes import *

app = Flask(__name__)

@app.route("/")
def redirecionador():
    return redirect("/login")

@app.route("/login", methods=['GET'])
def login():        
    if "login" in request.form:
        user = request.form.get("name")
        passw = request.form.get("senha")

        if autenticar(user, passw):
            return redirect(f"/home/{user}")
        
        else:
            print(error)
            return redirect("/login")                          #TODO: adicionar mensagem de erro ao logar (ao invés de print)
        
    return render_template("login.html")

@app.route("/cadastro", methods=['GET'])
def cadastro():
    if "cadastrar" in request.form:
        user = request.form.get("name_c")
        passw = request.form.get("senha_c")
        user_add = Usuario(user, passw)
        user_add.cadastrar()
        
        return redirect("/login")

    return render_template(cadastro.html)

@app.route("/home")
def home(user):
    pass

@app.route("/inserir")
def inserir_roupa(user):
    pass
        
@app.route("/planejador")
def planejador(user):
    pass

if __name__ == '__main__':
    app.run(debug=True)
