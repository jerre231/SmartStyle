from flask import *
from models import *
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'  # Nome da pasta onde as imagens serão salvas
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/", methods=['GET', 'POST'])
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
        return redirect(f"/inserir_roupa/{user}")
    elif "exibir" in request.form:
        return redirect(f"/armario/{user}")

    return render_template("/home.html")

@app.route("/armario/<user>")
def armario(user):
    return render_template("armario.html")

@app.route("/inserir_roupa/<user>", methods=['GET', 'POST'])
def inserir_roupa(user):
    global red_user
    red_user = user
    return render_template("inserir_roupa.html")
        
@app.route("/planejador/<user>")
def planejador(user):
    return render_template("planejador.html")

@app.route("/upload", methods=['POST'])
def upload_file():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    if 'imagem' not in request.files:
        return redirect(request.url)

    file = request.files['imagem']

    if file.filename == '':
        return redirect(request.url)

    if file:
        unique_filename = str(uuid.uuid4()) + "_" + file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
        image_path = f"uploads/{unique_filename}"
        roupa = Roupa("admin", "tatu", image_path)
        roupa.inserir()

        return redirect(f"/inserir_roupa/{red_user}")
    
if __name__ == '__main__':
    app.run(debug=True)
