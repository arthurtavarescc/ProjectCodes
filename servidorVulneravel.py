from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Conectando ao banco vulnerável
def conectar_banco_vulneravel():
    return sqlite3.connect('banco_vulneravel.db')

# Função para verificar se a senha é correta
def verificar_senha(usuario, senha):
    conn = conectar_banco_vulneravel()
    cursor = conn.cursor()

    # Consulta vulnerável a SQL Injection
    query = f"SELECT * FROM usuarios WHERE usuario = '{usuario}' AND senha = '{senha}'"
    cursor.execute(query)
    user = cursor.fetchall()  # Retorna todos os resultados da consulta
    conn.close()
    return user  # Retorna os dados da consulta

@app.route('/login', methods=['POST'])
def login():
    # Verifica se os dados foram enviados como JSON ou form-data
    if request.is_json:
        data = request.get_json()
        usuario = data.get('usuario')
        senha = data.get('senha')
    else:
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

    # Tentando login
    dados_usuario = verificar_senha(usuario, senha)
    if dados_usuario:  # Se houver dados retornados
        return jsonify({
            "status": "OK",
            "message": "Login bem-sucedido (banco_vulneravel.db)!",
            "data": dados_usuario  # Retorna os dados da consulta
        })
    else:
        return jsonify({"status": "ERROR", "message": "Usuário ou senha inválidos!"}), 200

if __name__ == '__main__':
    # Rodando o servidor
    app.run(debug=True)
