## 📄 `README.md`

````markdown
# 🚀 PulseCheck API

Plataforma de Monitoramento de Serviços Internos desenvolvida com **Python**, **FastAPI**, **PostgreSQL**, **MongoDB**, **RabbitMQ** e **Docker**.

---

## 📦 Stack

- **Python 3.12**
- **FastAPI**
- **SQLAlchemy (async)**
- **Alembic**
- **PostgreSQL**
- **MongoDB**
- **RabbitMQ**
- **Docker + Docker Compose**

---

## 📖 Como rodar o projeto

### 🔧 Pré-requisitos

- Docker
- Docker Compose

---

### 📦 Subir os containers

```bash
docker-compose up -d
```
````

Isso irá subir:

- API FastAPI (porta `8000`)
- PostgreSQL (porta `5432`)
- MongoDB (porta `27017`)
- RabbitMQ + UI (portas `5672` e `15672`)

---

### 🗄️ Rodar as migrations

#### 📌 Criar nova migration (opcional)

```bash
docker exec pulsecheck_api alembic revision --autogenerate -m "descrição da migration"
```

#### 📌 Aplicar migrations

```bash
docker exec pulsecheck_api alembic upgrade head
```

---

### 🚀 Acessar a API

Acesse: [http://localhost:8000/docs](http://localhost:8000/docs)

Para a documentação interativa via Swagger.

---

## 🐰 Acessar RabbitMQ Management

Acesse: [http://localhost:15672](http://localhost:15672)  
Login: `guest`
Senha: `guest`

---

## 📝 Variáveis de Ambiente

Exemplo do arquivo `.env`:

```env
DATABASE_URL=postgresql+asyncpg://username:password@host:port/database
MONGO_URL=mongodb://host:port
RABBITMQ_URL=amqp://username:password@host:port/
PROJECT_NAME=PulseCheck
API_PREFIX=/api
```

---

## 📌 Comandos úteis

### 📄 Ver logs da aplicação

```bash
docker-compose logs -f app
```

### 📦 Parar os containers

```bash
docker-compose down
```

---

## ✨ Autor

Feito por [Abner Ferreira de Andrade](https://github.com/abnerfandrade) 🚀

```

```
