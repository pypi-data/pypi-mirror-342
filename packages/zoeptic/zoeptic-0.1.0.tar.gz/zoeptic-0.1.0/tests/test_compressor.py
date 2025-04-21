import os
from zoeptic.compression import compress_by_extension

def test_compression_by_extension():
    # Crear archivos de prueba
    with open("datos.csv", "w", encoding="utf-8") as f:
        f.write("id,nombre\n1,Ana\n2,Juan")
    with open("notas.txt", "w", encoding="utf-8") as f:
        f.write("Esto es un archivo de texto")

    # Ejecutar la compresión selectiva
    compress_by_extension(['.csv'], zip_output='seleccion.zip', gzip_output='seleccion.csv.gz')

    # Verificar que los archivos comprimidos se generaron
    assert os.path.exists('seleccion.zip')
    assert os.path.exists('seleccion.csv.gz')

    # Limpieza
    os.remove('datos.csv')
    os.remove('notas.txt')
    os.remove('seleccion.zip')
    os.remove('seleccion.csv.gz')

