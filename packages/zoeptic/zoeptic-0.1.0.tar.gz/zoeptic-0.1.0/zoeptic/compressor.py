# Crear el archivo zoeptic/compression.py con este contenido

import os
import zipfile
import gzip
import shutil

def compress_by_extension(extensions, zip_output='output.zip', gzip_output=None):
    """
    Comprime archivos según su extensión
    
    Args:
        extensions (list): Lista de extensiones a comprimir (con punto, como '.csv')
        zip_output (str): Nombre del archivo zip de salida
        gzip_output (str): Nombre base del archivo gzip de salida (opcional)
    """
    with zipfile.ZipFile(zip_output, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for filename in os.listdir('.'):
            if os.path.isfile(filename) and os.path.splitext(filename)[1] in extensions:
                # Añadir al archivo ZIP
                zipf.write(filename, os.path.basename(filename))
                
                # Si se especificó una salida gzip, comprimir también con gzip
                if gzip_output:
                    with open(filename, 'rb') as f_in:
                        with gzip.open(gzip_output, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    print(f"Archivo comprimido con gzip: {gzip_output}")
                
                print(f"Archivo añadido al ZIP: {filename}")


