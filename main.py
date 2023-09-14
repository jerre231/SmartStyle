from flask import Flask, render_template, request, redirect
from classes import *

app = Flask(__name__)

@app.route("/")
def redirecionador():
    return redirect("/login")

@app.route("/login", methods=['GET', 'POST'])
def login():        
    if "login" in request.form:
        user = request.form.get("name")
        passw = request.form.get("password")

        if autenticar(user, passw):
            return redirect(f"/home/{user}")
        
        else:
            return redirect("/login")                          #TODO: adicionar mensagem de erro ao logar (ao invés de print)
        
    if "cadastro" in request.form:
        return redirect("/cadastro")
    
    return render_template("login.html")

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if "cadastrar" in request.form:
        user = request.form.get("name_c")
        passw = request.form.get("passw_c")
        user_add = Usuario(user, passw)
        user_add.cadastrar()
        
        return redirect("/login")

    if "Voltar" in request.form:
        return redirect("/login")

    return render_template("cadastro.html")


@app.route("/home/<user>")
def home(user):
    return render_template("/home.html")

@app.route("/armario")
def armario(user):
    return render_template("armario.html")

@app.route("/inserir")
def inserir_roupa(user):
    return render_template("inserir_roupa.html")
        
@app.route("/planejador")
def planejador(user):
    return render_template("planejador.html")

if __name__ == '__main__':
    app.run(debug=True)
