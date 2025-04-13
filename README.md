# 🚀 PulseCheck API

Internal Services Monitoring Platform built with **Python**, **FastAPI**, **PostgreSQL**, **MongoDB**, **RabbitMQ**, and **Docker**.

---

## 📦 Tech Stack

- **Python 3.12**
- **FastAPI**
- **SQLAlchemy (async)**
- **Alembic**
- **PostgreSQL**
- **MongoDB**
- **RabbitMQ**
- **Docker + Docker Compose**

---

## 📖 How to Run the Project

### 🔧 Requirements

- Docker
- Docker Compose

---

### 📦 Start the Containers

```bash
docker-compose up -d
```

This will start:

- FastAPI API (port `8000`)
- PostgreSQL (port `5432`)
- MongoDB (port `27017`)
- RabbitMQ + Management UI (ports `5672` and `15672`)
- Health Check Worker
- Dispatcher Worker

---

### 🗄️ Run Database Migrations

#### 📌 Create a New Migration (optional)

```bash
docker exec pulsecheck_api alembic revision --autogenerate -m "migration description"
```

#### 📌 Apply Migrations

```bash
docker exec pulsecheck_api alembic upgrade head
```

---

## 🚀 Access the API

Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

To view the interactive Swagger documentation.

---

## 🐰 Access RabbitMQ Management UI

Visit: [http://localhost:15672](http://localhost:15672)  
Login: `guest`  
Password: `guest`

---

## 📖 Available Workers

- **Health Check Worker**: Listens to the `health_checks` queue and performs HTTP health checks for services.
- **Dispatcher Worker**: Periodically queries services from PostgreSQL and dispatches health check tasks to the queue based on each service’s configured frequency.

---

## 📝 Environment Variables to use local with docker

Example `.env` file:

```env
DATABASE_URL=postgresql+asyncpg://pulseuser:pulsepass@postgres:5432/pulsecheckdb
MONGO_URL=mongodb://mongo:27017
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
PROJECT_NAME=PulseCheck
API_PREFIX=/api
QUEUE_HEALTH_CHECK=health_checks
```

---

## 📌 Useful Commands

### 📄 View Application Logs

```bash
docker-compose logs -f api
```

### 📦 Stop Containers

```bash
docker-compose down
```

---

## ✨ Author

Made by [Abner Ferreira de Andrade](https://github.com/abnerfandrade) 🚀
