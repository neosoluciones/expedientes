from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import col

app = FastAPI()

# ✅ CORS LIBRE (soluciona el error de conexión)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ROOT (para test)
@app.get("/")
def root():
    return {"status": "ok"}

# GET EXPEDIENTES (CORREGIDO)
@app.get("/expedientes")
def listar_expedientes():
    try:
        data = list(col.find({}, {"_id": 0}))
        for e in data:
            e["tipo_proceso"] = e.get("tipo_proceso", "Proceso judicial")
            e["compilacion"] = e.get("compilacion", "")
            e["paginas"] = e.get("paginas", 0)
            e["anios_tramite"] = e.get("anios_tramite", 0)
            e["organismos"] = e.get("organismos", 0)
            e["causas_conexas"] = e.get("causas_conexas", 0)
            e["ultimo_estado"] = e.get("ultimo_estado", "")
            e["hitos_clave"] = e.get("hitos_clave", [])
            e["inmueble"] = e.get("inmueble", {})
            e["palabras_clave"] = e.get("palabras_clave", [])
        return data
    except Exception as e:
        return {"error": str(e)}
