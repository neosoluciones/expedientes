import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# conexión a MongoDB desde variables de entorno
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "expedientes_pdf")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "expedientes")

try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    # Verificar conexión
    client.server_info()
    print("Conexion a MongoDB exitosa")
except (ConnectionFailure, ServerSelectionTimeoutError) as e:
    print(f"Error de conexion a MongoDB: {e}")
    raise

# base de datos
db = client[DB_NAME]

# colección
col = db[COLLECTION_NAME]