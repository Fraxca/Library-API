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
        author TEXT NOT NULL,
        UNIQUE(title, author)
    )
    """)

    conexao.commit()
    conexao.close()

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
    query = "SELECT id, title, author FROM livros WHERE id = ?"
    params = []
    if title := request.args.get("title"):
        query += " AND title = ?"
        params.append(title)
    if author := request.args.get("author"):
        query += " AND author = ?"
        params.append(author)
    cursor.execute(query, (id, *params))
    livro_db = cursor.fetchone()
    conexao.close()
    resultado = {"id": livro_db[0], "title": livro_db[1], "author": livro_db[2]} if livro_db else None
    if resultado:
        return jsonify(resultado)
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
    conexao.close()
    return jsonify({"message": "Livro atualizado com sucesso"})

@app.route("/livros", methods=["POST"])
def create_livro():
    """
    Tutorial de uso - Criar um novo livro
    -------------------------------------
    Endpoint: POST /livros
    Cabeçalho: Content-Type: application/json
    Corpo da requisição (JSON):
        {
            "title": "O Senhor dos Anéis",
            "author": "J.R.R. Tolkien"
        }

    Resposta de sucesso (201):
        {
            "id": 1,
            "title": "O Senhor dos Anéis",
            "author": "J.R.R. Tolkien"
        }

    Possíveis erros:
    - 400: Livro já existe (violação da restrição UNIQUE)
    - 500: Erro inesperado no servidor
    """

    novo_livro = request.get_json()
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "INSERT INTO livros (title, author) VALUES (?, ?)",
            (novo_livro["title"], novo_livro["author"])
        )
        conexao.commit()
        novo_id = cursor.lastrowid
        conexao.close()
        novo_livro["id"] = novo_id
        return jsonify(novo_livro), 201
    except sqlite3.IntegrityError as e:
        conexao.close()
        return jsonify({"message": f"Erro de integridade: {str(e)}"}), 400
    except Exception as e:
        conexao.close()
        return jsonify({"message": f"Erro inesperado: {str(e)}"}), 500
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