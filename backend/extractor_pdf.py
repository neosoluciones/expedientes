import os
import re
from datetime import datetime
from pypdf import PdfReader
from db import col

# rutas seguras
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(BASE_DIR, "data", "input_pdfs")


def extraer_texto(pdf_path):
    reader = PdfReader(pdf_path)
    texto = ""

    for page in reader.pages:
        contenido = page.extract_text()
        texto += contenido if contenido else ""

    return texto


def limpiar_descripcion(texto):
    texto = re.sub(r"^\d{2}/\d{2}/\d{4}\s*", "", texto)
    return texto.strip()


def parsear_expediente(texto, archivo):

    numero = None
    caratula = None
    actuaciones = []
    cuij = None
    tribunal = None
    fecha_inicio = None
    actor = None
    demandado = None
    objeto = None
    normativa = []
    estado_procesal = "EN PROCESO"

    # ✅ número desde archivo
    match_file = re.search(r"(\d+)", archivo)
    if match_file:
        numero = match_file.group(1)

    lineas = texto.split("\n")

    for linea in lineas:
        texto_linea = linea.strip()
        texto_upper = texto_linea.upper()

        # ✅ CUIJ
        match_cuij = re.search(r"(\d{2}-\d{7,}-\d)", texto_linea)
        if match_cuij:
            cuij = match_cuij.group(1)

        # ✅ carátula
        if " C/" in texto_upper:
            caratula = texto_linea

        # ✅ partes
        if caratula and not actor and not demandado:
            partes = caratula.split(" C/")
            if len(partes) == 2:
                actor = partes[0].strip()
                demandado = partes[1].strip()

        # ✅ tribunal
        if "JUZGADO" in texto_upper or "TRIBUNAL" in texto_upper:
            tribunal = texto_linea

        # ✅ objeto
        if "OBJETO" in texto_upper:
            objeto = texto_linea

        # ✅ normativa
        if "LEY" in texto_upper or "ART" in texto_upper:
            normativa.append(texto_linea)

        # ✅ fecha
        match_fecha = re.search(r"(\d{2}/\d{2}/\d{4})", texto_linea)

        if match_fecha:

            if "PORTAL DE GEST" in texto_upper:
                continue
            if "PÁGINA" in texto_upper:
                continue
            if len(texto_linea) < 15:
                continue

            fecha = match_fecha.group(1)
            descripcion = limpiar_descripcion(texto_linea)

            tipo = "OTRO"
            if "DECRETO" in texto_upper:
                tipo = "DECRETO"
            elif "ESCRITO" in texto_upper:
                tipo = "ESCRITO"
            elif "AUTO" in texto_upper:
                tipo = "AUTO"
            elif "SENTENCIA" in texto_upper:
                tipo = "SENTENCIA"
            elif "OFICIO" in texto_upper:
                tipo = "OFICIO"

            if "SENTENCIA" in texto_upper:
                estado_procesal = "FINALIZADO"
            elif "ARCHIVO" in texto_upper:
                estado_procesal = "ARCHIVADO"

            actuaciones.append({
                "fecha": fecha,
                "tipo": tipo,
                "descripcion": descripcion
            })

    # ✅ ordenar actuaciones
    def parse_fecha(f):
        try:
            return datetime.strptime(f, "%d/%m/%Y")
        except:
            return datetime.max

    actuaciones.sort(key=lambda x: parse_fecha(x["fecha"]))

    if actuaciones:
        fecha_inicio = actuaciones[0]["fecha"]

    return {
        "numero": numero,
        "cuij": cuij,
        "caratula": caratula,
        "tribunal": tribunal,
        "fecha_inicio": fecha_inicio,
        "estado_procesal": estado_procesal,
        "partes": {
            "actor": actor,
            "demandado": demandado
        },
        "objeto": objeto,
        "normativa": normativa,
        "actuaciones": actuaciones
    }


def procesar_pdfs():

    for archivo in os.listdir(INPUT_DIR):

        if archivo.endswith(".pdf"):

            ruta = os.path.join(INPUT_DIR, archivo)

            print("\n📄 Procesando:", archivo)

            texto = extraer_texto(ruta)

            expediente = parsear_expediente(texto, archivo)

            expediente["pdf"] = ruta
            expediente["file_name"] = archivo

            print("DEBUG:")
            print("Numero:", expediente["numero"])
            print("CUIJ:", expediente["cuij"])
            print("Caratula:", expediente["caratula"])
            print("Actuaciones:", len(expediente["actuaciones"]))
            print("Estado:", expediente["estado_procesal"])

            col.update_one(
                {"pdf": ruta},
                {"$set": expediente},
                upsert=True
            )

            print("✅ Guardado correctamente")


if __name__ == "__main__":
    procesar_pdfs()



