from flask import Flask, render_template, request, redirect
from models import *

app = Flask(__name__)

@app.route("/")
def redirecionador():
    return redirect("/login")

@app.route("/login", methods=['GET', 'POST'])
def login():

    error_message = ""

    if "login" in request.form:
        user = request.form.get("name")
        passw = request.form.get("password")

        if autenticar(user, passw):
            return redirect(f"/home/{user}")
        
        else:
            error_message = "Usuario ou senha invalidos, tente novamente ou cadastre-se."
        
    if "cadastro" in request.form:
        return redirect("/cadastro")
    
    return render_template("login.html", error_message=error_message)

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


@app.route("/home/<user>", methods=['GET', 'POST'])
def home(user):
    if "inserir" in request.form:
        return redirect(f"/inserir/{user}")
    elif "exibir" in request.form:
        return redirect(f"/armario/{user}")

    return render_template("/home.html")

@app.route("/armario/<user>")
def armario(user):
    return render_template("armario.html")

@app.route("/inserir/<user>")
def inserir_roupa(user):
    return render_template("inserir_roupa.html")
        
@app.route("/planejador")
def planejador(user):
    return render_template("planejador.html")

if __name__ == '__main__':
    app.run(debug=True)
