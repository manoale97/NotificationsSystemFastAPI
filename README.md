# Notifications System API

Scaffolding inicial de una API con FastAPI, SQLite y una arquitectura limpia ligera. La única entidad del ejemplo es `User`.

## Fase 1: preparar el entorno

Requiere Python 3.10 o superior. Desde la carpeta del proyecto, crea un entorno virtual e instala las dependencias:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

Opcionalmente, copia `.env.example` a `.env` y ajusta `DATABASE_URL`. Para cargar ese archivo, inicia Uvicorn con `--env-file .env`; si no defines la variable, la aplicación usa `./app.db`.

## Fase 2: iniciar FastAPI

```powershell
python -m uvicorn app.main:app --reload
```

Abre <http://127.0.0.1:8000/docs> para explorar y probar la API interactiva de Swagger. FastAPI genera esta documentación desde las rutas y los modelos Pydantic.

Si configuraste `.env`, usa:

```powershell
python -m uvicorn app.main:app --reload --env-file .env
```

## Fase 3: recorrer una petición

Al crear un usuario con `POST /users`, el flujo es:

1. `app/api/routes/users.py` recibe la petición y valida el JSON con `UserCreate`.
2. FastAPI resuelve `get_user_service` como dependencia; esta obtiene una sesión SQLAlchemy.
3. `UserService` aplica las reglas del caso de uso, como comprobar que el email no exista.
4. `SqlAlchemyUserRepository` convierte la entidad a una fila de SQLite y la guarda.
5. La ruta devuelve `UserRead`; FastAPI valida y serializa la respuesta JSON.

La misma ruta funciona con `TestClient` en las pruebas, sin levantar un servidor.

## Fase 4: probar el CRUD

Usa `/docs` o `curl.exe`:

```powershell
curl.exe -X POST http://127.0.0.1:8000/users -H "Content-Type: application/json" -d '{"name":"Ada Lovelace","email":"ada@example.com"}'
curl.exe http://127.0.0.1:8000/users
curl.exe http://127.0.0.1:8000/users/1
curl.exe -X PUT http://127.0.0.1:8000/users/1 -H "Content-Type: application/json" -d '{"name":"Ada","email":"ada@example.com","is_active":true}'
curl.exe -X DELETE http://127.0.0.1:8000/users/1
```

El email es único. Un email inválido produce `422`, un usuario inexistente `404` y un email duplicado `409`.

## Fase 5: ejecutar pruebas

```powershell
python -m pytest
```

Las pruebas usan una base SQLite temporal en memoria y cubren creación, lectura, actualización, eliminación y errores comunes.

## Estructura y responsabilidades

```text
app/
  api/routes/          Endpoints HTTP y dependencias
  application/         Casos de uso de users
  domain/              Entidad, errores y contrato del repositorio
  infrastructure/      SQLAlchemy, conexión y repositorio SQLite
  schemas/              Modelos de entrada y salida HTTP (Pydantic)
  main.py               Aplicación FastAPI y ciclo de vida
tests/                  Pruebas de API
```

La dirección de dependencias importa: las rutas usan el servicio; el servicio conoce el contrato del repositorio, no SQLAlchemy; infraestructura implementa ese contrato. Esto mantiene el diseño sencillo sin añadir una capa por cada operación.

## Próximos pasos de aprendizaje

1. Cambia `GET /users` para añadir paginación con `limit` y `offset`.
2. Añade una nueva regla de negocio en `UserService` y una prueba.
3. Cambia el repositorio para PostgreSQL manteniendo las rutas y el servicio.
4. Estudia migraciones con Alembic antes de evolucionar el esquema en un entorno persistente.

## Configuración

`DATABASE_URL` acepta una URL SQLAlchemy. Ejemplo SQLite: `sqlite:///./app.db`. El archivo de base de datos se crea al iniciar la aplicación.
