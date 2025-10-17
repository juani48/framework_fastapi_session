Nutricion Web - development notes

Redis for sessions
------------------

This project uses Redis as the session store. Set the `REDIS_URL` environment variable (for example in a `.env` file) before running the app. Example:

	REDIS_URL=redis://localhost:6379/0

To run Redis locally (Linux), you can install and start it with your package manager, or use Docker:

	# using apt (Debian/Ubuntu)
	sudo apt update && sudo apt install redis-server
	sudo systemctl enable --now redis-server

	# or using docker
	docker run -p 6379:6379 -d --name redis-local redis:7-alpine

No changes to `pyproject.toml` are required if you already have `redis[async]` in the dependencies (it is included).

Usage in this project
---------------------

The Redis backend in `src/web/config.py` reads `REDIS_URL` and stores session objects under keys `session:<uuid>` as JSON.

----

# FastAPI Session Framework

Un framework de autenticación y gestión de sesiones con FastAPI, Redis, PostgreSQL y control de acceso basado en roles.

## 📋 Descripción

Este proyecto es una aplicación web desarrollada con FastAPI que implementa un sistema de autenticación, gestión de sesiones con Redis, y control de acceso basado en roles (RBAC). Incluye una arquitectura en capas con repositorios, servicios y controladores, siguiendo las mejores prácticas de desarrollo.

### Características principales

- ✅ **Autenticación segura** con cookies firmadas criptográficamente
- ✅ **Gestión de sesiones** con Redis como backend
- ✅ **Control de acceso basado en roles** (Admin, User)
- ✅ **Hash seguro de contraseñas** con Argon2 y Passlib
- ✅ **Base de datos PostgreSQL** con SQLModel y Alembic
- ✅ **Arquitectura en capas** (Model, Repository, Service, Controller)
- ✅ **Templates con Jinja2** para renderizado del lado del servidor
- ✅ **API REST** para operaciones asíncronas
- ✅ **Manejo de errores** centralizado con decoradores

## 🏗️ Arquitectura del Proyecto

```
src/
├── main.py                    # Punto de entrada de la aplicación
├── core/                      # Lógica de negocio central
│   ├── database.py           # Configuración de base de datos
│   ├── model/                # Modelos SQLModel
│   │   ├── user.py          # Modelo de usuario
│   │   └── role.py          # Modelo de roles
│   ├── repository/           # Capa de acceso a datos
│   │   ├── user_repo.py     # Repositorio de usuarios
│   │   ├── role_repo.py     # Repositorio de roles
│   │   └── admin_repo.py    # Repositorio de administración
│   └── service/              # Servicios y utilidades
│       ├── config.py        # Configuración de sesiones y Redis
│       ├── session.py       # Gestión de sesiones
│       ├── session_data.py  # Estructura de datos de sesión
│       ├── depends.py       # Dependencias de FastAPI
│       ├── decorators.py    # Decoradores personalizados
│       ├── hash.py          # Hashing de contraseñas
│       └── validator.py     # Validación de datos
└── web/                      # Capa de presentación
    ├── controllers/          # Controladores HTTP
    │   ├── default.py       # Rutas por defecto
    │   ├── auth/            # Autenticación
    │   │   ├── render.py   # Vistas HTML
    │   │   └── rest.py     # Endpoints API
    │   └── admin/           # Panel administrativo
    │       ├── render.py   # Vistas HTML
    │       └── rest.py     # Endpoints API
    ├── entities/            # DTOs y schemas
    └── templates/           # Templates Jinja2
```

## 🚀 Instalación y Configuración

### Requisitos previos

- Python 3.12 o superior
- PostgreSQL
- Redis
- Poetry (recomendado) o pip

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd framework-fastapi-session
```

### 2. Instalar dependencias

```bash
# Con Poetry
poetry install
```

### 3. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Base de datos PostgreSQL
DATABASE_URL="tu-url-de-la-base-de-datos"

# Redis para sesiones
REDIS_URL="tu-url-de-redis"

# Clave secreta para firmar cookies (genera una segura)
API_KEY=tu-clave-secreta-muy-segura-aqui
```

### 4. Configurar Redis

#### Opción A: Instalación local (Linux)

```bash
# Usando apt (Debian/Ubuntu)
sudo apt update && sudo apt install redis-server
sudo systemctl enable --now redis-server
```

#### Opción B: Docker

```bash
docker run -p 6379:6379 -d --name redis-local redis:7-alpine
```

### 5. Configurar PostgreSQL

```bash
# Crear base de datos
createdb framework_fastapi_session_db

# O con psql
psql -U postgres
CREATE DATABASE framework_fastapi_session_db;
```

### 6. Inicializar la base de datos

```bash
# Las migraciones se ejecutan automáticamente al iniciar la app
# Se creará un usuario admin por defecto:
# Email: admin@example.com
# Password: admin123
```

## 🎯 Uso

### Ejecutar la aplicación

```bash
# Modo desarrollo
python -m src.main

# O con uvicorn directamente
uvicorn main:app --reload
```

La aplicación estará disponible en: `http://127.0.0.1:8000`

### Rutas principales

#### Páginas públicas
- `GET /` - Página de inicio
- `GET /user/login` - Formulario de inicio de sesión
- `GET /user/signin` - Formulario de registro

#### API de autenticación
- `POST /auth/register` - Registrar nuevo usuario
- `POST /auth/login` - Iniciar sesión
- `PUT /auth/logout` - Cerrar sesión

#### Panel administrativo (requiere rol admin)
- `GET /admin/panel` - Panel de administración
- `GET /admin/users` - Lista de usuarios
- `GET /admin/users/form` - Formulario de creación de usuario
- `POST /admin/users` - Crear nuevo usuario
- `PUT /admin/users/{user_id}` - Actualizar usuario
- `DELETE /admin/users/{user_id}` - Eliminar usuario

## 🔐 Sistema de Autenticación

### Flujo de autenticación

1. **Login/Register**: El usuario envía credenciales
2. **Validación**: Se valida el usuario contra la base de datos
3. **Creación de sesión**: Se genera un UUID y se almacena en Redis
4. **Cookie firmada**: Se envía una cookie HTTP-only con el session_id

### Dependencias de FastAPI

El sistema utiliza cuatro meotdos en los endpoints:

#### 1. `get_session` - Sesión opcional
```python
async def render_index(
    request: Request, 
    session: Optional[SessionData] = Depends(get_session)
)
```
Retorna la sesión si existe, `None` en caso contrario. Útil para páginas que cambian según el estado de autenticación.

#### 2. `cookie` - Solo validación de cookie
```python
@router.get("/panel", dependencies=[Depends(cookie)])
```
Lee y valida la cookie (firma criptográfica) sin recuperar los datos de sesión. Actúa como filtro de autenticación básico.

#### 3. `verifier` - Sesión requerida
```python
async def render_admin_form_users(
    request: Request, 
    session: SessionData = Depends(verifier)
)
```
El verificador:
1. Ejecuta la dependencia `cookie` para obtener el `session_id`
2. Busca los datos de sesión en Redis
3. Crea un objeto `SessionData` con la información del usuario
4. Pasa el objeto como argumento a la función principal

Si no hay sesión válida, retorna un error 403.

#### 4. `require_role` - Control de acceso por roles
```python
async def admin_panel(
    request: Request, 
    session: SessionData = Depends(require_role([RoleEnum.ADMIN]))
)
```
Verifica que el usuario tenga uno de los roles autorizados. Combina verificación de sesión con control de acceso.

## 🗄️ Gestión de sesiones con Redis

### Backend Redis personalizado

El proyecto implementa un backend personalizado para almacenar sesiones en Redis:

```python
class RedisBackend:
    async def create(session_id: UUID, data: SessionData) -> None
        # Almacena sesión como JSON con clave: "session:<uuid>"
    
    async def read(session_id: UUID) -> Optional[SessionData]
        # Recupera y deserializa la sesión
    
    async def delete(session_id: UUID) -> None
        # Elimina la sesión
```

### Estructura de SessionData

```python
class SessionData(BaseModel):
    name: str
    email: str
    role: str  # Ejemplo: "admin", "user"
```

Las sesiones se almacenan en Redis con claves del formato: `session:<uuid>`

## 🔧 Tecnologías utilizadas

### Backend
- **FastAPI** (0.119.0) - Framework web moderno y rápido
- **Uvicorn** - Servidor ASGI
- **SQLModel** (0.0.27) - ORM basado en Pydantic y SQLAlchemy
- **Asyncpg** - Driver PostgreSQL asíncrono
- **Alembic** - Migraciones de base de datos

### Autenticación y seguridad
- **fastapi-sessions** (0.3.2) - Gestión de sesiones
- **redis[async]** (6.4.0) - Almacenamiento de sesiones
- **Passlib[bcrypt]** - Hashing de contraseñas
- **Argon2-cffi** - Algoritmo de hashing adicional

### Frontend
- **Jinja2** - Motor de templates
- **python-multipart** - Manejo de formularios

### Utilidades
- **python-dotenv** - Variables de entorno

## 📦 Estructura de datos

### UserModel
```python
class UserModel(SQLModel, table=True):
    id: int
    name: str
    last_name: str
    email: str (único)
    hashed_password: str
    role_id: int (FK a RoleModel)
```

### RoleModel
```python
class RoleModel(SQLModel, table=True):
    id: int
    name: str
```
### RoleEnum
```python
class RoleEnum(enum.Enum):
    ADMIN = "ADMIN"
    CONFIGURATOR = "CONFIGURATOR"
    USER = "USER"
```

## 🛡️ Seguridad

- **Contraseñas hasheadas** con Argon2
- **Cookies HTTP-only** para prevenir XSS
- **Cookies con SameSite=Lax** para protección CSRF
- **Cookies firmadas** criptográficamente
- **Sesiones en Redis** con expiración configurable
- **Control de acceso basado en roles**

## 🧪 Testing

```bash
# Ejecutar tests
pytest tests/
```

## 📝 Usuario por defecto

Al inicializar la base de datos, se crea un usuario administrador:

- **Email**: `admin@example.com`
- **Password**: `admin123`
- **Rol**: Admin

⚠️ **Importante**: Cambia estas credenciales en producción.

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 👤 Autor

**Juani** - jibyrab@gmail.com

## 🔮 Roadmap

- [ ] Implementar refresh tokens
- [ ] Agregar autenticación OAuth2
- [ ] Tests unitarios y de integración
- [ ] Documentación OpenAPI mejorada
- [ ] Docker Compose para desarrollo
- [ ] CI/CD pipeline