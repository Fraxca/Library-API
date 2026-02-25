import sqlite3
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "biblioteca.db")
#Banco de dados
DB_NAME = "biblioteca.db"
def conectar() -> sqlite3.Connection:
    #Cria e retorna uma conexão com o banco de dados SQLite.
    return sqlite3.connect(DB_NAME)
def criar_tabelas() -> None:
    
    #Cria todas as tabelas necessárias para o sistema, caso não existam.
    
    conexao = conectar()
    cursor = conexao.cursor()

    # Tabela de livros
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL
    )
    """)

    conexao.commit()
    conexao.close()



livors = [{
    "id": 1,
    "title": "O Senhor dos Anéis",
    "author": "J.R.R. Tolkien",
    },
    {
    "id": 2,
    "title": "Harry Potter e a Pedra Filosofal",
    "author": "J.K. Rowling",
    },
    {
    "id": 3,
    "title": "O Código Da Vinci",
    "author": "Dan Brown",
    },
]
#Consultar todos
@app.route("/livros", methods=["GET"])
def get_livros():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, title, author FROM livros")
    livros_db = cursor.fetchall()
    conexao.close()
    # Converte a lista de tuplas em lista de dicionários para o JSON ficar bonito
    resultado = [{"id": l[0], "title": l[1], "author": l[2]} for l in livros_db]
    return jsonify(resultado)

#Consultar por id
@app.route("/livros/<int:id>", methods=["GET"])
def get_livro(id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, title, author FROM livros WHERE id = ?", (id,))
    livro = cursor.fetchone()
    conexao.close()
    if livro:
        return jsonify({"id": livro[0], "title": livro[1], "author": livro[2]})
    return jsonify({"message": "Livro não encontrado"}), 404

#Editar
@app.route("/livros/<int:id>", methods=["PUT"])
def edit_livro(id):
    conexao = conectar()
    cursor = conexao.cursor()
    dados = request.get_json()
    cursor.execute("UPDATE livros SET title = ?, author = ? WHERE id = ?", 
                   (dados["title"], dados["author"], id))
    conexao.commit()
    if cursor.fetchone() is None:
        conexao.close()
        return jsonify({"message": "Livro não encontrado"}), 404

@app.route("/livros", methods=["POST"])
def create_livro():
    novo_livro = request.get_json()
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO livros (title, author) VALUES (?, ?)", (request.json["title"], request.json["author"]))
    conexao.commit()
    if cursor.rowcount == 0:
        conexao.close()
        return jsonify({"message": "Erro ao criar livro"}), 500
    novo_id = cursor.lastrowid
    conexao.close()
    novo_livro = request.get_json()
    novo_livro["id"] = novo_id
    livors.append(novo_livro)
    return jsonify(novo_livro)
#Deletar
@app.route("/livros/<int:id>", methods=["DELETE"])
def delete_livro(id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM livros WHERE id = ?", (id,))
    conexao.commit()
    if cursor.rowcount == 0:
        conexao.close()
        return jsonify({"message": "Livro não encontrado"}), 404
    conexao.close()
    return jsonify({"message": "Livro deletado com sucesso"})


if __name__ == "__main__":
    criar_tabelas()
    app.run(port=5000, debug=True, host="localhost")