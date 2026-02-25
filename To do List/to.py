import sqlite3
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "todo.db")
DB_NAME = "todo.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            concluida INTEGER DEFAULT 0
        
        )
    """)
    conexao.commit()
    conexao.close()

def mostrar_tarefas(tarefas):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT descricao FROM tarefas")
    tarefas_db = cursor.fetchall()
    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
    else:
        print("Tarefas:")
        for tarefa in tarefas_db:
             print(f"- {tarefa[0]}")
        for i, tarefa in enumerate(tarefas, start=1):
            print(f"{i}. {tarefa}")
    conexao.close()


def adicionar_tarefa(tarefas):
    nova_tarefa = input("Digite a nova tarefa: ")
    tarefas.append(nova_tarefa)
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO tarefas (descricao) VALUES (?)", (nova_tarefa,))
    conexao.commit()
    conexao.close()
    print("Tarefa adicionada com sucesso!")

def remover_tarefa(tarefas):
    mostrar_tarefas(tarefas)
    if tarefas:
        try:
            indice = int(input("Digite o número da tarefa a ser removida: "))
            if 1 <= indice <= len(tarefas):
                tarefa_removida = tarefas.pop(indice - 1)
                conexao = conectar()
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM tarefas WHERE descricao=?", (tarefa_removida,))
                conexao.commit()
                conexao.close()
                print(f"Tarefa '{tarefa_removida}' removida com sucesso!")
            else:
                print("Número inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")

def tarefa_concluida(tarefas):
    mostrar_tarefas(tarefas)
    if tarefas:
        try:
            indice = int(input("Digite o número da tarefa concluída: "))
            if 1 <= indice <= len(tarefas):
                tarefa_concluida = tarefas.pop(indice - 1)
                conexao = conectar()
                cursor = conexao.cursor()
                cursor.execute("UPDATE tarefas SET concluida=1 WHERE descricao=?", (tarefa_concluida,))
                conexao.commit()
                conexao.close()
                print(f"Tarefa '{tarefa_concluida}' marcada como concluída!")
            else:
                print("Número inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")

def tarefas_concluidas(tarefas):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT descricao FROM tarefas WHERE concluida=1")
    tarefas_concluidas_db = cursor.fetchall()
    if  tarefas_concluidas_db:
        print("Tarefas Concluídas:")
        for tarefas in tarefas_concluidas_db:
            print(f"- {tarefas[0]}")
    else:
        print("nenhuma tarefa concluida") 

def main():
    tarefas = []
    while True:
        print("\n---TO DO LIST---")
        print("1. Mostrar tarefas")
        print("2. Adicionar tarefa")
        print ("3. Remover tarefa")
        print("4. Marcar tarefa como concluída")
        print("5. Mostrar tarefas concluídas")
        print("6. Sair")

        escolha = input("escolha uma opção:")

        if escolha == "1":
            mostrar_tarefas(tarefas)
        elif escolha == "2":
            adicionar_tarefa(tarefas)
        elif escolha == "3":
            remover_tarefa(tarefas)
        elif escolha == "4":
            tarefa_concluida(tarefas)
        elif escolha == "5":
            tarefas_concluidas(tarefas)
        elif escolha == "6":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    criar_tabela()
    main()