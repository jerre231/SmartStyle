from flask import *
from models import *
import os
import datetime

#Bilbioteca utilizada para criar nomes específicos e diferentes para cada imagem, assim não há como sobreescreve-las
import uuid

app = Flask(__name__)

#Criando a pasta das imagens das roupas
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#Rota para o login, inicializa o site aqui
@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():

    #Inicializando a mensagem de erro como uma string vazia, para não aparecer caso não haja erro
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


#Rota para o cadastro
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
        return redirect(f"/inserir_roupa_categoria/{user}")
    elif "exibir" in request.form:
        return redirect(f"/armario/{user}")
    
    data_atual = datetime.datetime.now()
    dia_da_semana = data_atual.strftime("%A")

    mapeamento_dias = {
    "Monday": "segunda",
    "Tuesday": "terca",
    "Wednesday": "quarta",
    "Thursday": "quinta",
    "Friday": "sexta",
    "Saturday": "sabado",
    "Sunday": "domingo"
    }  

    nome_dia_abreviado = mapeamento_dias.get(dia_da_semana, dia_da_semana)

    resultado = exibir_home(user, nome_dia_abreviado)

    if resultado is not None:
        acessorio, superior, inferior, calcado = resultado
    else:
        acessorio, superior, inferior, calcado = None, None, None, None

    return render_template("/home.html", acessorio=acessorio, superior=superior, inferior=inferior, calcado=calcado, dia_da_semana=dia_da_semana)

@app.route("/armario/<user>", methods=['GET', 'POST'])
def armario(user):
    acessorios = exibir_roupas(user, "acessorio")
    superiores =  exibir_roupas(user, "superior")
    inferiores =  exibir_roupas(user, "inferior")
    calcados = exibir_roupas(user, "calcado")

    if request.method == 'POST':
        if "Submeter" in request.form:

            dia_semana = request.form.get("dia_semana")
  
            acessorio_selecionado = request.form.get("acessorio")
            superior_selecionado = request.form.get("superior")
            inferior_selecionado = request.form.get("inferior")
            calcado_selecionado = request.form.get("calcado")

            dia = Dia(
                dia_semana,
                acessorio_selecionado,
                superior_selecionado,
                inferior_selecionado,
                calcado_selecionado
            )

            dia.inserir_editar()
    
    if "home" in request.form:
        return redirect(url_for("home", user=user))
    
    return render_template("armario.html", cat1=acessorios, cat2=superiores, cat3=inferiores, cat4=calcados)

#Primeira etapa de adicionar roupa, escolhe a categoria
@app.route("/inserir_roupa_categoria/<user>", methods=['GET', 'POST'])
def inserir_roupa_categoria(user):
    if "enviar_categoria" in request.form:
        global tipo
        tipo = request.form.get("categoria")

        return redirect(url_for('inserir_roupa', user=user))
    
    elif "home" in request.form:
        return redirect(url_for('home', user=user))
    
    return render_template("inserir_roupa1.html")

#Segunda etapa de adicionar roupa, envia a imagem da roupa
@app.route("/inserir_roupa/<user>", methods=['GET', 'POST'])
def inserir_roupa(user):
    #definindo como global para poder repassar para o action do upload
    global red_user
    red_user = user
    return render_template("inserir_roupa.html")

#Action acionada pelo html, salva a imagem na pasta uploads e declara o objeto roupa usando como parametro as variaveis globais
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
        image_path = f"/static/{unique_filename}"
        roupa = Roupa(red_user, tipo, image_path)
        roupa.inserir()

        return redirect(url_for('home', user=red_user))
    
if __name__ == '__main__':
    app.run(debug=True)
    