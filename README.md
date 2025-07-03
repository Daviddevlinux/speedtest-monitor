# 📶 Monitor de Velocidade da Internet

Este script em Python realiza testes periódicos de velocidade da internet, registra os resultados em um arquivo CSV e gera um gráfico com o histórico de medições.

## ⚙️ Funcionalidades

- Testa a velocidade de download, upload e o ping.
- Registra os dados em um arquivo CSV.
- Verifica se há conexão antes de testar.
- Detecta o IP público automaticamente.
- Alerta para quedas bruscas de velocidade.
- Gera gráfico com histórico de medições.

## 🧰 Tecnologias Utilizadas

- Python 3
- speedtest-cli
- pandas
- matplotlib
- requests
- socket

## 📦 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/monitor-velocidade.git
   cd monitor-velocidade
   ```
2. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Como Usar

Execute o script:

```bash
  python teste_velocidade.py
```

### Por padrão, ele:

- Faz 5 medições (MAX_MEDICOES = 5) Mas isso pode ser mudado de acordo com sua necessidade

- Espera 30 segundos entre cada medição (INTERVALO = 30) Mas isso pode ser mudado de acordo com sua necessidade

- Salva os dados no arquivo velocidade_internet.csv

- Gera um gráfico final grafico_velocidade.png com os resultados.

## 📈 Exemplo de Saída

```bash
[INFO] Medição 1/5
[INFO] IP externo detectado: 200.201.10.123
[2025-07-03 08:00:00] Ping: 12.34 ms | Download: 94.56 Mbps | Upload: 38.21 Mbps
...
[INFO] Gráfico gerado em 'grafico_velocidade.png'
```

## ⏳ Importante: Sobre o Tempo Entre Medições

O `speedtest-cli` pode levar **vários segundos** para completar uma medição de velocidade, especialmente em conexões instáveis ou com ping elevado.

> ⚠️ **Se o intervalo definido entre as medições (`INTERVALO`) for muito pequeno (como 5 ou 10 segundos), o script poderá acabar executando testes em sequência, sem pausa real, ou até sobrecarregar sua rede.**

Por isso, recomenda-se definir um intervalo de **pelo menos 30 segundos** para evitar conflitos ou sobreposição entre testes consecutivos:

```python
INTERVALO = 30  # Recomendado
```
