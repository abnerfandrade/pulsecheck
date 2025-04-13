FROM python:3.12.10-slim

# Define variáveis de ambiente padrão
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências básicas
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia requirements e instala dependências
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia o código para dentro do container
COPY . .

# Da permissão de execução para o script wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Expõe a porta padrão do FastAPI/Uvicorn
EXPOSE 8000

# Comando de inicialização
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
