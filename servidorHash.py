from flask import Flask, request, jsonify
import sqlite3
import hashlib

app = Flask(__name__)

# Conectando ao banco seguro
def conectar_banco_seguro():
    return sqlite3.connect('banco_seguro.db')

# Função para gerar o hash da senha
def gerar_hash_senha(senha, salt):
    return hashlib.sha256((senha + salt).encode()).hexdigest()

# Função para verificar se a senha é correta
def verificar_senha(usuario, senha):
    conn = conectar_banco_seguro()
    cursor = conn.cursor()

    # Consulta vulnerável a SQL Injection
    query = f"SELECT * FROM usuarios WHERE usuario = '{usuario}'"
    cursor.execute(query)
    user = cursor.fetchone()  # Retorna o primeiro resultado da consulta
    conn.close()

    if user:
        id, usuario_db, senha_hash, salt = user
        if gerar_hash_senha(senha, salt) == senha_hash:
            return True, user  # Retorna True e os dados do usuário
    return False, None  # Retorna False e nenhum dado

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
    sucesso, dados_usuario = verificar_senha(usuario, senha)
    if sucesso:
        return jsonify({
            "status": "OK",
            "message": "Login bem-sucedido!",
            "data": dados_usuario  # Retorna os dados do usuário
        })
    else:
        return jsonify({"status": "ERROR", "message": "Usuário ou senha inválidos!"}), 200

if __name__ == '__main__':
    # Rodando o servidor
    app.run(debug=True)
