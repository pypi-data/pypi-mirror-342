import csv
import json
import os

def csv_to_optimized_json(csv_path, json_path, remove_duplicates=True):
    """
    Convierte un archivo CSV a JSON, con opción de eliminar filas duplicadas.
    Basado solo en la columna 'id' para la eliminación de duplicados.

    Parámetros:
        csv_path (str): Ruta del archivo CSV de entrada.
        json_path (str): Ruta del archivo JSON de salida.
        remove_duplicates (bool): Si es True, elimina filas duplicadas.

    Retorna:
        bool: True si la operación fue exitosa, False en caso contrario
    """
    try:
        # Verificar si el archivo CSV existe
        if not os.path.exists(csv_path):
            print(f"Error: El archivo CSV no existe en la ruta: {csv_path}")
            return False

        with open(csv_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            data = list(reader)
            print(f"Datos leídos del CSV: {len(data)} filas")

            if remove_duplicates:
                seen = set()
                unique_data = []
                for row in data:
                    if 'id' not in row:
                        print("Error: La columna 'id' no existe en el CSV")
                        return False
                    
                    current_id = row['id'].strip()
                    print(f"Procesando ID: {current_id}")
                    
                    if current_id not in seen:
                        unique_data.append(row)
                        seen.add(current_id)
                    else:
                        print(f"ID duplicado encontrado: {current_id}")
                
                data = unique_data
                print(f"Datos después de eliminar duplicados: {len(data)} filas")

        # Forzar la escritura del archivo JSON
        with open(json_path, mode='w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
            jsonfile.flush()
            os.fsync(jsonfile.fileno())

        # Verificar si el archivo JSON se creó correctamente
        if os.path.exists(json_path):
            print(f"Archivo JSON creado exitosamente en: {json_path}")
            return True
        else:
            print(f"Error: No se pudo crear el archivo JSON en: {json_path}")
            return False

    except Exception as e:
        print(f"Error durante la conversión: {str(e)}")
        return False