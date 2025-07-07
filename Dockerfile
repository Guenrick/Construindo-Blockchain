FROM python:3.10-slim

# Todos os comandos a seguir serão executados a partir deste diretório
WORKDIR /app

COPY . .

CMD ["python", "blockchain.py"]