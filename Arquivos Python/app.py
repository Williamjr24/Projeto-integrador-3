from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime
from flask_cors import CORS

# Cria a aplicação Flask
app = Flask(__name__)
CORS(app)

# Configuração do banco de dados MySQL
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='**********',
    database='iluminacao'
)

# Rota para salvar o estado enviado pelo ESP32
@app.route('/sensor', methods=['POST'])
def salvar_estado():
    try:
        # Obtém os dados enviados pelo ESP32
        data = request.get_json()
        estado = data['estado']

        # Obtém a data e hora atuais no momento da requisição
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor = db.cursor()

        if estado == "Ligada":
            sql = "INSERT INTO sensores (Ligado) VALUES (%s)"
            cursor.execute(sql, (agora,))
        elif estado == "Desligada":
            sql = "UPDATE sensores SET Desligado = %s WHERE Ligado IS NOT NULL AND Desligado IS NULL ORDER BY ID DESC LIMIT 1"
            cursor.execute(sql, (agora,))

        db.commit()
        cursor.close()

        return "Estado salvo no banco de dados!", 200

    except Exception as e:
        return f"Erro ao salvar estado: {e}", 500

# Rota para fornecer os dados do banco em formato JSON
@app.route('/dados', methods=['GET'])
def obter_dados():
    try:
        cursor = db.cursor(dictionary=True)  # Retorna os dados como dicionário
        cursor.execute("""
            SELECT
                ID,
                Ligado,
                Desligado,
                TIMESTAMPDIFF(SECOND, Ligado, Desligado) AS Tempo_Ligado,
                TIMESTAMPDIFF(SECOND, Ligado, Desligado) * 0.00763488 / 3600 AS Custo
            FROM sensores
            WHERE Desligado IS NOT NULL
        """)
        dados = cursor.fetchall()
        cursor.close()

        # Formatar as datas para melhor apresentação
        for row in dados:
            row['Ligado'] = row['Ligado'].strftime("%d/%m/%Y - %H:%M:%S") if row['Ligado'] else None
            row['Desligado'] = row['Desligado'].strftime("%d/%m/%Y - %H:%M:%S") if row['Desligado'] else None
            row['Tempo_Ligado'] = row['Tempo_Ligado'] if row['Tempo_Ligado'] is not None else 0
            row['Custo'] = row['Custo'] if row['Custo'] is not None else 0

        return jsonify(dados), 200

    except Exception as e:
        return f"Erro ao obter dados: {e}", 500

# Inicialização da aplicação Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)