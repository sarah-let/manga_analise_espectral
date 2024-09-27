from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Para liberar CORS e permitir que o front-end acesse o back-end

BASE_DIR = r'C:\Users\lenau\OneDrive\Documentos\manga_analise_espectral\SARAH_IC_GIT\Palmer_IC\PLSR_Palmer\graphs_sg'

@app.route('/get-chart', methods=['POST'])
def get_chart():
    # Receber os dados do front-end (pré-tratamento, método estatístico, etc.)
    data = request.json
    
    # Baseado nas seleções do front-end, definir o nome do gráfico que será enviado
    pretratamento = data.get('pretratamento')
    metodo_estatistico = data.get('metodo_estatistico')
    variedade = data.get('variedade')
    parametro = data.get('parametro')
    
    # Supondo que você nomeie os gráficos de acordo com a combinação selecionada
    if variedade.lower() == 'palmer' and metodo_estatistico.lower() == 'plsr' and pretratamento == 'savitzky-golay':
        if parametro.lower() == 'brix':
            chart_name = 'sst_predicted_vs_reference.png'
        else:
            chart_name = f'{parametro.lower()}sst_predicted_vs_reference.png'
    
    # Caminho completo do gráfico
    chart_path = os.path.join(BASE_DIR, chart_name)

    # Verificar se o arquivo existe e retornar
    if os.path.exists(chart_path):
        return send_file(chart_path, mimetype='image/png')
    else:
        return jsonify({"error": "Gráfico não encontrado"}), 404

if __name__ == '__main__':
    # Definir a porta manualmente (você pode mudar aqui para a porta que preferir)
    app.run(debug=True, port=5000)
