# API REST - Biblioteca Virtual

API REST completa para gestionar una Biblioteca Virtual desarrollada con FastAPI, PostgreSQL y Docker.

## Tecnologías
- FastAPI + SQLAlchemy
- PostgreSQL 15
- Docker + Docker Compose
- JWT (access + refresh tokens)
- Alembic (migraciones)

## Requisitos
- Docker Desktop
- Docker Compose

## Instalación y ejecución

### 1. Clonar el repositorio
```bash
git clone git@github.com:clauck89/API-REST-BIBLIOTECA-VIRTUAL.git
cd API-REST-BIBLIOTECA-VIRTUAL
```

### 2. Crear el archivo de variables de entorno
```bash
cp .env.example .env
```
Edita `.env` con tus valores si es necesario.

### 3. Levantar el proyecto
```bash
docker compose up --build
```

### 4. Acceder a la documentación
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints principales

### Autenticación
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | /api/auth/register | Registro de usuario |
| POST | /api/auth/token | Login (obtener JWT) |
| POST | /api/auth/token/refresh | Refrescar token |

### Autores, Categorías, Libros
| Método | Endpoint | Descripción | Acceso |
|--------|----------|-------------|--------|
| GET | /api/autores/ | Listar autores | Público |
| POST | /api/autores/ | Crear autor | Admin |
| PUT | /api/autores/{id} | Actualizar autor | Admin |
| DELETE | /api/autores/{id} | Eliminar autor | Admin |

### Préstamos
| Método | Endpoint | Descripción | Acceso |
|--------|----------|-------------|--------|
| GET | /api/prestamos/ | Listar todos | Admin |
| POST | /api/prestamos/ | Crear préstamo | Autenticado |
| POST | /api/prestamos/{id}/devolver | Devolver libro | Autenticado |
| GET | /api/mis-prestamos/ | Mis préstamos | Autenticado |

## Crear usuario administrador
```bash
docker compose exec web python -c "
from app.database import SessionLocal
from app.models.user import User
from app.auth.jwt_utils import hash_password
db = SessionLocal()
admin = User(username='admin', email='admin@biblioteca.com', hashed_password=hash_password('admin123'), is_admin=True)
db.add(admin)
db.commit()
print('Admin creado')
"
```

## Variables de entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| SECRET_KEY | Clave para firmar JWT | - |
| DB_NAME | Nombre de la base de datos | biblioteca_db |
| DB_USER | Usuario PostgreSQL | postgres |
| DB_PASSWORD | Contraseña PostgreSQL | postgres123 |
| DB_HOST | Host de PostgreSQL | db |
| DB_PORT | Puerto PostgreSQL | 5432 |