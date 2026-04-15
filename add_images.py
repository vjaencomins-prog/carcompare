import json
import requests
import time

def obtener_imagen_coche(marca, modelo):
    """Obtiene una imagen de coche usando un servicio gratuito"""
    # Usar Picsum para imágenes placeholder realistas
    # Generar un ID consistente basado en marca+modelo para tener la misma imagen siempre
    import hashlib
    hash_obj = hashlib.md5(f"{marca} {modelo}".encode())
    image_id = int(hash_obj.hexdigest(), 16) % 1000  # ID entre 0-999

    # URL de Picsum con ID consistente
    return f"https://picsum.photos/id/{image_id + 100}/400/250"

def actualizar_coches_con_imagenes():
    """Lee coches.json, añade imágenes y guarda el archivo actualizado"""
    try:
        with open('coches.json', 'r', encoding='utf-8') as f:
            coches = json.load(f)

        print(f"Actualizando {len(coches)} coches con imágenes...")

        for i, coche in enumerate(coches):
            marca = coche.get('marca', '')
            modelo = coche.get('modelo', '')

            if 'imagen' not in coche:  # Solo si no tiene imagen
                imagen = obtener_imagen_coche(marca, modelo)
                coche['imagen'] = imagen
                print(f"[{i+1}/{len(coches)}] {marca} {modelo} -> {imagen}")

        # Guardar archivo actualizado
        with open('coches.json', 'w', encoding='utf-8') as f:
            json.dump(coches, f, indent=2, ensure_ascii=False)

        print("✅ Archivo coches.json actualizado con imágenes!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    actualizar_coches_con_imagenes()</content>
<parameter name="filePath">/Users/victorjaencomins/web coches/add_images.py