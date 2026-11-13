
import sqlite3
import csv
from pathlib import Path
from datetime import datetime

# Localiza a pasta principal do projeto
pasta_projeto = Path(__file__).resolve().parent.parent

# Caminho do banco de dados
caminho_banco = pasta_projeto / "banco" / "ocorrencias.db"

# Consulta as ocorrencias registradas
conexao = sqlite3.connect(caminho_banco)
cursor = conexao.cursor()

cursor.execute("""
    SELECT id, data_hora, epi_ausente, caminho_imagem
    FROM ocorrencias
    ORDER BY data_hora DESC
""")

ocorrencias = cursor.fetchall()
conexao.close()

# Nome do relatorio com data e hora
data_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
nome_arquivo = f"relatorio_epi_{data_atual}.csv"

caminho_relatorio = pasta_projeto / "relatorios" / nome_arquivo

# Cria o arquivo CSV
with open(caminho_relatorio, "w", newline="", encoding="utf-8-sig") as arquivo:
    escritor = csv.writer(arquivo, delimiter=";")

    escritor.writerow([
        "ID",
        "Data e Hora",
        "EPI Ausente",
        "Caminho da Evidencia"
    ])

    escritor.writerows(ocorrencias)

print("Relatorio gerado com sucesso!")
print(f"Arquivo: {caminho_relatorio}")
print(f"Total de ocorrencias: {len(ocorrencias)}")
