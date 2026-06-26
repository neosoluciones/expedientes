from db import col
from datetime import datetime

col.update_one(
    {},
    {
        '$set': {
            'tipo_proceso': 'Proceso judicial',
            'compilacion': datetime.now().strftime('%d/%m/%Y'),
            'paginas': 453,
            'anios_tramite': 14,
            'organismos': 5,
            'causas_conexas': 3,
            'ultimo_estado': '2026',
            'hitos_clave': [
                'Inicio del expediente',
                'Medidas procesales',
                'Intervencion de organismos',
                'Estado actual'
            ],
            'inmueble': {
                'direccion': 'Ruta Provincial N 7 s/n',
                'ubicacion': 'Cacheuta - Potrerillos, Lujan de Cuyo, Mendoza',
                'descripcion': 'Inmueble objeto del proceso judicial',
                'etiqueta': 'Objeto principal'
            },
            'palabras_clave': [
                'Proceso judicial',
                'Expediente',
                'Actuaciones',
                'Tribunal',
                'Partes'
            ]
        }
    }
)

print('Datos actualizados correctamente')
