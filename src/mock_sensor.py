import requests
import time
import random
import json

URL = 'http://localhost:5000/leituras'

def gerar_dados_mock():
    return {
        "temperatura": round(random.uniform(20.0, 35.0), 2),
        "umidade": round(random.uniform(40.0, 80.0), 2),
        "pressao": round(random.uniform(1000.0, 1025.0), 2),
        "localizacao": "Simulador"
    }

def iniciar_simulacao():
    print("Iniciando simulador de sensor (Mock)... Pressione Ctrl+C para parar.")
    while True:
        dados = gerar_dados_mock()
        try:
            resposta = requests.post(URL, json=dados)
            if resposta.status_code == 201:
                print(f"[{time.strftime('%H:%M:%S')}] Dados enviados com sucesso: {dados}")
            else:
                print(f"Erro ao enviar: Status {resposta.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão: Servidor Flask está rodando? Detalhe: {e}")
        
        time.sleep(5) 

if __name__ == '__main__':
    iniciar_simulacao()