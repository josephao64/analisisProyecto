# 🧩 Inventory Control API (FastAPI + PostgreSQL + Alembic + Docker)

API REST para gestionar productos, ubicaciones, existencias y movimientos de inventario.

## 🏗 Tecnologías
- FastAPI, Uvicorn
- SQLAlchemy 2.0
- Alembic (migraciones)
- PostgreSQL 16
- Docker & Docker Compose
- Pydantic v2

## 🚀 Puesta en Marcha (Docker)
1. Copia `.env.example` a `.env` y ajusta variables si deseas.
2. Levanta los servicios:
   ```bash
   docker-compose up --build
   ```
   Esto ejecutará `alembic upgrade head` automáticamente y luego iniciará la API.
3. Documentación interactiva:
   - Swagger UI: http://localhost:8000/docs
   - Redoc: http://localhost:8000/redoc

## 🧪 Migraciones manuales
- Crear nueva migración:
  ```bash
  alembic revision --autogenerate -m "descripcion"
  ```
- Aplicar migraciones:
  ```bash
  alembic upgrade head
  ```

## 🔌 Endpoints principales
- `POST /products` | `GET /products` | `GET /products/{id}` | `PUT /products/{id}` | `DELETE /products/{id}`
- `POST /locations` | `GET /locations` | `GET /locations/{id}` | `PUT /locations/{id}` | `DELETE /locations/{id}`
- `GET /stocks` (filtros por `product_id`, `location_id`, `low_stock_only`)
- `POST /movements` (IN/OUT/ADJUST) | `GET /movements`
- `GET /health`

## 🧰 Reglas de negocio implementadas
- Unicidad de `products.sku` y `locations.code`
- Rango válido para cantidades/precios (no negativos)
- `active` por defecto en productos/ubicaciones
- No permitir stock negativo en OUT
- Todo ajuste de stock se registra en `movements`
- `stocks` es fuente de verdad para cantidad por (producto, ubicación)

## 📦 Datos de prueba (opcional)
Ejecuta interactivamente desde `/docs` para crear productos, ubicaciones y movimientos.

## 📁 Estructura
```text
app/
  core/ (configuración y DB)
  models/ (ORM SQLAlchemy)
  schemas/ (Pydantic)
  services/ (reglas de negocio: transacciones de inventario)
  api/
    routes/ (routers por recurso)
    router.py
  main.py
alembic/
  versions/ (migraciones)
Dockerfile
docker-compose.yml
requirements.txt
.env.example
```

## 📄 Licencia
MIT
