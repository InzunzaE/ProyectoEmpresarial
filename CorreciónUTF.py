# -*- coding: utf-8 -*-
"""
Corregir_UTF8.py
----------------
Corrige textos mal codificados (mojibake) en archivos CSV.

Ejemplo:
'JosÃ© MartÃ­nez' → 'José Martínez'

Permite:
- Reparar un solo archivo
- Reparar todos los CSV de una carpeta automáticamente

Eitan Misael Inzunza Becerra
2025-06-11
"""

import os  # Permite trabajar con rutas, archivos y carpetas del sistema operativo


# === CONFIGURACIÓN ===
# OPCIÓN A: Reparar solo 1 archivo:
ruta_archivo = r"C:\Users\eitan\OneDrive\Documentos\Universidad\ProyectoEmpresarial\AUTHORS_master_v3.csv"  
# ↑ Ruta exacta del archivo a reparar (déjala así si vas a trabajar solo con un archivo)

# OPCIÓN B: Reparar todos los CSV dentro de una carpeta:
ruta_carpeta = r""     # Si agregas una ruta aquí, procesará todos los .csv dentro de ella


def reparar_mojibake(texto: str) -> str:
    """
    Repara texto corrompido por recodificación UTF-8→Latin-1.
    Además corrige secuencias específicas.
    """

    texto = texto.replace("<81>", "Á")  # Reemplazo manual de un caso común de error de codificación

    patrones = ("Ã", "Â", "�")  # Fragmentos que suelen aparecer cuando hay mojibake

    # Corrección iterativa (hasta 3 intentos)
    for _ in range(3):
        if any(p in texto for p in patrones):  # Si todavía aparecen errores...
            texto = texto.encode("latin-1", errors="ignore").decode("utf-8", errors="ignore") 
            # ↑ Reinterpreta el texto para corregir los caracteres extraños, primero convierte a bytes y luego transforma a UTF-8
        else:
            break  # Si ya no hay errores, termina antes

    return texto  # Devuelve el texto reparado



def reparar_archivo(ruta: str):
    """
    Repara un solo archivo CSV y genera otro con el sufijo _utf8.csv
    """

    nombre_salida = os.path.splitext(ruta)[0] + "_utf8.csv"  
    # Crea un nuevo nombre de archivo agregando el sufijo _utf8

    with open(ruta, "rb") as f:  # Abre el archivo en modo binario (para evitar problemas de encoding)
        raw = f.read()  # Lee TODO el archivo como bytes

    texto = raw.decode("latin-1", errors="ignore")  # Intenta interpretar el archivo como Latin-1
    texto_reparado = reparar_mojibake(texto)  # Repara el contenido línea por línea

    with open(nombre_salida, "w", encoding="utf-8-sig", newline="") as f:
        f.write(texto_reparado)  # Guarda el archivo final en UTF-8 (con BOM para compatibilidad con Excel)

    print(f"✅ Reparado: {os.path.basename(ruta)} → {os.path.basename(nombre_salida)}")
    # Mensaje informativo de éxito



def main():
    print("=== Reparador de codificación UTF-8 (mojibake) ===")

    # Si se especificó un archivo y existe, se repara   
    if ruta_archivo and os.path.isfile(ruta_archivo):
        reparar_archivo(ruta_archivo)

    # Si se especificó una carpeta, procesa todos los CSV dentro de ella
    if ruta_carpeta and os.path.isdir(ruta_carpeta):
        print("\nProcesando todos los CSV de la carpeta...\n")
        for archivo in os.listdir(ruta_carpeta):  # Recorre cada archivo encontrado
            if archivo.lower().endswith(".csv"):  # Verifica que sea CSV
                reparar_archivo(os.path.join(ruta_carpeta, archivo))  # Lo repara

    print("\n🎉 Proceso terminado.")  # Mensaje final


# Ejecuta main() si este archivo es ejecutado directamente
if __name__ == "__main__":
    main()
