import speedtest
import csv
from datetime import datetime
import time
import requests
import socket
import pandas as pd
import matplotlib.pyplot as plt

ARQUIVO_SAIDA = "velocidade_internet.csv"
INTERVALO = 30  # segundos entre medições
MAX_MEDICOES = 5  # número máximo de medições
CAMPOS = ['timestamp', 'ip', 'ping_ms', 'download_Mbps', 'upload_Mbps']

ultima_download = None
media_download_acumulada = 0
medicoes_realizadas = 0
ip = None  # IP será detectado apenas uma vez

def tem_conexao():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

# Cria o CSV se não existir
try:
    with open(ARQUIVO_SAIDA, 'x', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(CAMPOS)
    print(f"[INFO] Arquivo '{ARQUIVO_SAIDA}' criado com cabeçalhos.")
except FileExistsError:
    print(f"[INFO] Arquivo '{ARQUIVO_SAIDA}' já existe.")

for i in range(MAX_MEDICOES):
    try:
        print(f"\n[INFO] Medição {i + 1}/{MAX_MEDICOES}")
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if not tem_conexao():
            print("[ALERTA] Sem conexão com a internet.")
            time.sleep(INTERVALO)
            continue

        if ip is None:
            ip = requests.get("https://api.ipify.org").text
            print(f"[INFO] IP externo detectado: {ip}")

        s = speedtest.Speedtest()
        s.get_best_server()

        download = s.download() / 1_000_000  # bits para megabits
        upload = s.upload() / 1_000_000
        ping = s.results.ping

        # Cálculo de variação
        if ultima_download is not None:
            variacao = download - ultima_download
            print(f"[INFO] Variação de download: {variacao:.2f} Mbps")
        ultima_download = download

        # Média acumulada para alerta
        medicoes_realizadas += 1
        media_download_acumulada += download
        media_anterior = media_download_acumulada / medicoes_realizadas

        if download < media_anterior * 0.5:
            print("[ALERTA] Queda significativa na velocidade de download!")

        # Salva no CSV
        with open(ARQUIVO_SAIDA, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, ip, round(ping, 2), round(download, 2), round(upload, 2)])

        print(f"[{timestamp}] Ping: {ping:.2f} ms | Download: {download:.2f} Mbps | Upload: {upload:.2f} Mbps")
        print(f"[INFO] Aguardando {INTERVALO} segundos...")

    except Exception as e:
        print(f"[ERRO] Falha durante o teste: {e}")
    time.sleep(INTERVALO)

# Gera gráfico ao final
try:
    df = pd.read_csv(ARQUIVO_SAIDA)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.plot(x='timestamp', y=['download_Mbps', 'upload_Mbps'], title="Histórico de Velocidade")
    plt.ylabel("Mbps")
    plt.xlabel("Horário")
    plt.tight_layout()
    plt.savefig("grafico_velocidade.png")
    print("[INFO] Gráfico gerado em 'grafico_velocidade.png'")
except Exception as e:
    print(f"[ERRO] Ao gerar gráfico: {e}")
