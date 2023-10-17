import pymongo

#função utilizada para facilitar o start do client da db
def start_client():
    client = pymongo.MongoClient("localhost", 27017)
    return client

def usuario_existe(username):
    client = start_client()
    db = client.get_database("smartStyle")
    usuarios = db.get_collection("usuarios")
    user = usuarios.find_one({"nome": username})

    if user:
        client.close()
        return True
    
    else:
        client.close
        return False
#função binária para autenticar usuario e senha
def autenticar(nome, senha):
    client = start_client() 
    db = client.get_database("smartStyle")
    usuarios = db.get_collection("usuarios")
    user = usuarios.find_one({"nome": nome})
    if user and user["senha"] == senha:
        client.close()
        return True
    else:
        client.close()
        return False
    

def exibir_roupas(username, tipo):
    client = start_client()
    db = client.get_database("smartStyle")
    roupas = db.get_collection("roupas")
    filtro = {"user": username, "tipo": tipo}

    fotos = roupas.find(filtro)

    imagens = [foto["imagem"] for foto in fotos]
    
    return imagens

def exibir_home(username, dia):
    client = start_client()
    db = client.get_database("smartStyle")
    dias = db.get_collection("dias")

    filtro = {"user": username, "dia": dia}

    dia_document = dias.find_one(filtro)

    if dia_document:
        acessorio = dia_document.get("acessorio")
        superior = dia_document.get("superior")
        inferior = dia_document.get("inferior")
        calcado = dia_document.get("calcado")

        return acessorio, superior, inferior, calcado
    else:
        return None

class Usuario:
    def __init__(self, us, pw):
        self.username = us
        self.password = pw

    def cadastrar(self):
        if not usuario_existe(self.username):
            client = start_client()
            db = client.get_database("smartStyle")
            usuarios = db.get_collection("usuarios")
            data = {"nome": self.username, "senha": self.password}
            usuarios.insert_one(data)
            client.close()

class Roupa:
    def __init__(self, user, tipo, imagem):
        self.username = user
        self.tipo = tipo
        self.img = imagem

    def inserir(self):
        client = start_client()
        db = client.get_database("smartStyle")
        roupas = db.get_collection("roupas")

        data = {"user": self.username, "tipo": self.tipo, "imagem": self.img}
        roupas.insert_one(data)
        client.close()

    def remover(self):
        pass

class Dia:
    def __init__(self, user, dia, acessorio, superior, inferior, calcado):
        self.dia = dia
        self.user = user
        self.data = {
            "user": user,
            "dia": dia,
            "acessorio": acessorio,
            "superior": superior,
            "inferior": inferior,
            "calcado": calcado
        }

    def inserir_editar(self):
        client = start_client()
        db = client.get_database("smartStyle")
        dias = db.get_collection("dias")
        filtro = {"user": self.user,"dia": self.dia}

        dias.update_one(filtro, {"$set": self.data}, upsert=True) #upsert=true garante que se o criterio nao for atendido o documento sera criado do mesmo jeito
        client.close()
        