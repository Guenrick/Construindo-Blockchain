FROM python:3.12-slim

WORKDIR /app

# Copia os arquivos do projeto para dentro do container
COPY blockchain.py .

# Instala o pacote necessário
RUN pip install ecdsa

# Comando padrão ao rodar o container
CMD ["python", "blockchain.py"]
