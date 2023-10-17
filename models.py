import pymongo

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