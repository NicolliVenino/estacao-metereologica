from flask import Flask, render_template, request, jsonify, redirect, url_for
import database

app = Flask(__name__)

database.init_db()

@app.route('/')
def index():
    leituras = database.listar_leituras(limite=10)
    return render_template('index.html', leituras=leituras)

@app.route('/historico')
def historico():
    leituras = database.listar_leituras(limite=100) 
    return render_template('historico.html', leituras=leituras)

@app.route('/editar/<int:id>', methods=['GET'])
def editar_page(id):
    leitura = database.buscar_leitura(id)
    if not leitura:
        return "Leitura não encontrada", 404
    return render_template('editar.html', leitura=leitura)

@app.route('/leituras', methods=['GET', 'POST'])
def leituras():
    if request.method == 'POST':
        dados = request.get_json()
        if not dados or 'temperatura' not in dados or 'umidade' not in dados:
            return jsonify({'erro': 'JSON inválido ou dados faltando'}), 400
        
        id_novo = database.inserir_leitura(
            dados['temperatura'], 
            dados['umidade'], 
            dados.get('pressao'),
            dados.get('localizacao', 'Lab')
        )
        return jsonify({'id': id_novo, 'status': 'criado'}), 201
    
    leituras = database.listar_leituras()
    return jsonify(leituras)

@app.route('/leituras/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def gerenciar_leitura(id):
    leitura = database.buscar_leitura(id)
    if not leitura:
        return jsonify({'erro': 'Leitura não encontrada'}), 404

    if request.method == 'GET':
        return jsonify(leitura)
        
    elif request.method == 'PUT':
        dados = request.get_json()
        database.atualizar_leitura(id, dados)
        return jsonify({'status': 'atualizado'})
        
    elif request.method == 'DELETE':
        database.deletar_leitura(id)
        return jsonify({'status': 'deletado'})

@app.route('/api/estatisticas', methods=['GET'])
def estatisticas():
    leituras = database.listar_leituras(limite=100)
    if not leituras:
        return jsonify({"erro": "Sem dados"}), 404
    
    temps = [l['temperatura'] for l in leituras]
    umids = [l['umidade'] for l in leituras]
    
    stats = {
        "temperatura": {
            "max": max(temps), "min": min(temps), "media": round(sum(temps)/len(temps), 2)
        },
        "umidade": {
            "max": max(umids), "min": min(umids), "media": round(sum(umids)/len(umids), 2)
        }
    }
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True, port=5000)