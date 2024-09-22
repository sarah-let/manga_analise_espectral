from flask import Flask, request, jsonify, send_file
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

app = Flask(__name__)
cors(app)

def snv(input_data):
    mean = np.mean(input_data, axis=1, keepdims=True)
    std_dev = np.std(input_data, axis=1, keepdims=True)
    snv_data = (input_data - mean) / std_dev
    return snv_data

@app.route('/get-chart', methods=['POST'])
def get_chart():
    data = request.json
    pretratamento = data.get('pretratamento')
    metodo_estatistico = data.get('metodo_estatistico')

    if pretratamento == "snv" and metodo_estatistico == "nenhum":
        file_path = './planilha_tommy.xlsx'
        fs_df = pd.read_excel(file_path)
        
        params = ['SST (°brix)', 'Firmeza (N)', 'AAC', 'ATT', '%UBS']
        fs_params = fs_df[params].dropna()
        
        fs_vars = fs_df.iloc[:, 8:].columns.to_list()
        dados_wl = fs_df[fs_vars].dropna()
        
        wl = np.array([float(col) for col in fs_vars])
        
        df_snv = snv(dados_wl.values)
        df_snv = pd.DataFrame(df_snv, columns=wl)
        
        plt.figure(figsize=(9, 5))
        plt.plot(wl, df_snv.T)
        plt.xlabel("Comprimento de onda (nm)", size=14)
        plt.ylabel("Refletância (AU)", size=14)
        plt.title("Correção SNV para o FieldSpec", size=18)
        plt.axhline(y=0, color='k', linewidth=1.5)
        plt.grid("on")
        
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        
        return send_file(img, mimetype='image/png')
    
    return jsonify({'error': 'Seleções inválidas'})

if __name__ == '__main__':
    app.run(debug=True)
