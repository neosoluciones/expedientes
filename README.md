# SGDE - Sistema de Gestión Documental de Expedientes

Sistema para extraer, procesar y visualizar datos de expedientes judiciales desde archivos PDF.

## Stack Tecnológico

- **Backend**: FastAPI + MongoDB
- **Frontend**: HTML5 + JavaScript (Vanilla)
- **Procesamiento PDF**: pypdf

## Estructura del Proyecto

```
SGDE/
├── backend/
│   ├── api.py              # API REST con FastAPI
│   ├── db.py               # Conexión a MongoDB
│   └── extractor_pdf.py    # Extracción de datos de PDFs
├── frontend/
│   └── index.html          # Interfaz web
├── data/
│   └── input_pdfs/         # PDFs a procesar
├── requirements.txt        # Dependencias Python
└── .env                    # Variables de entorno
```

## Instalación

### Prerrequisitos
- Python 3.8+
- MongoDB (instalado localmente o en servidor)

### Pasos

1. **Clonar el repositorio**
   ```bash
   git clone <repo-url>
   cd SGDE
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Linux/Mac
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   ```bash
   # Crear archivo .env con:
   MONGODB_URI=mongodb://localhost:27017/
   DB_NAME=expedientes_pdf
   COLLECTION_NAME=expedientes
   CORS_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
   ```

5. **Iniciar MongoDB**
   ```bash
   # Si está instalado localmente
   mongod
   ```

## Uso

### Procesar PDFs

Coloca los archivos PDF en `data/input_pdfs/` y ejecuta:

```bash
cd backend
python extractor_pdf.py
```

Esto extraerá los datos y los guardará en MongoDB.

### Iniciar API

```bash
cd backend
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en `http://localhost:8000`

### Endpoints

- `GET /expedientes` - Listar todos los expedientes
- `GET /expedientes/{numero}` - Obtener expediente por número

### Visualizar Frontend

Abre `frontend/index.html` en un navegador web.

## Datos Extraídos

El sistema extrae de cada PDF:
- Número de expediente
- CUIJ
- Carátula
- Tribunal
- Fecha de inicio
- Estado procesal
- Partes (actor/demandado)
- Objeto del proceso
- Normativa aplicada
- Actuaciones (timeline)

## Desarrollo

### Agregar nuevos campos de extracción

Editar `backend/extractor_pdf.py` en la función `parsear_expediente()`.

### Modificar frontend

Editar `frontend/index.html`. El JavaScript carga datos dinámicamente desde la API.

## Seguridad

- CORS configurado para orígenes específicos (ver `.env`)
- Validación de datos en endpoints
- Manejo de errores en backend

## Licencia

Proyecto desarrollado para gestión documental judicial.
