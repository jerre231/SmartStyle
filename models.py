import sqlite3

global error

#função para conectar a database:
def conectar_bd():
    return sqlite3.connect('database.db')

#inicializando a table "roupas" (database), procedimento realizado nessa linha segue para cada alteração feita na base de dados a seguir.
conn = conectar_bd()
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS roupas (
               id INTEGER PRIMARY KEY,
               tipo TEXT,
               tamanho TEXT,
               cor TEXT,
               temporada TEXT       
    )
''')
conn.commit()
conn.close()

#inicializando a table "usuarios" (dabatase)
conn = conectar_bd()
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios(
               id INTEGER PRIMARY KEY,
               username TEXT,
               password TEXT,
               nome TEXT
    )
''')
conn.commit()
conn.close()

#função para verificar se usuário já existe na db
def usuario_existe(username):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM usuarios WHERE username = ?", (username,))
    resultado = cursor.fetchone()
    conn.close()

    # Verifica se um usuário foi encontrado
    return resultado is not None

# Autenticação de usuário para login, caso usuario nao exista ou senha errada retonar falso, caso esteja tudo certo retorna true
def autenticar(nome, senha):
    if usuario_existe(nome):
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM usuarios WHERE username=?", (nome,))
        temp_pass_tuple = cursor.fetchone()
        conn.close()

        if temp_pass_tuple is not None:
            temp_pass = temp_pass_tuple[0]

            if senha == temp_pass:
                return True
            else:
                error = "Senha incorreta"
                return False
        else:
            error = "Usuário não encontrado"
            return False
    else:
        error = "Usuário inexistente"
        return False


#definindo cada classe:

class Roupa:
    def __init__(self, tipo, tamanho, cor, temporada, nome):
        self.tipo = tipo
        self.tamanho = tamanho
        self.cor = cor
        self.temporada = temporada
        self.nome = nome

        self.insert = self.tipo, self.tamanho, self.cor, self.temporada, self.nome

    def inserir(self):
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO roupas (tipo, tamanho, cor, temporada) VALUES (?, ?, ?, ?)", (self.insert))
        conn.commit()
        conn.close()

    def editar(self):
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM roupas WHERE tipo = ?", (self.nome))
        id = cursor.fetchone()
        cursor.execute("UPDATE roupas SET tipo=?, tamanho=?, cor=?, temporada=?, nome=? WHERE id=?", (self.insert, id))
        conn.commit()
        conn.close()

class Usuario:
    def __init__(self, us, pw):
        self.username = us
        self.password = pw

    def cadastrar(self):
        if not usuario_existe(self.username):
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (self.username, self.password))
            conn.commit()
            conn.close()
        else:
            print("usuário já existente")                                      #TODO: printar erro "usuário existente" no site usando jsonify ou algo do tipo.

    def remover(self):
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE username = ?", (self.username))
        conn.commit()
        conn.close()
