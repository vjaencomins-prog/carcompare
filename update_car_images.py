import json

def generar_url_imagen(marca, modelo, año):
    """
    Genera URL de imagen usando Unsplash (API de imágenes gratuita y sin autenticación)
    Busca imágenes de coches basado en la marca
    """
    # Normalizar marca para búsqueda
    marca_limpia = marca.lower().replace('-', '').replace(' ', '')
    
    # URLs de Unsplash que buscan imágenes de coches
    # La API pública de Unsplash no requiere API key para búsquedas básicas
    return f'https://source.unsplash.com/featured/400x300?{marca_limpia},car'

def actualizar_imagenes_coches():
    """Lee coches.json y actualiza las imágenes con URLs de Unsplash"""
    try:
        with open('coches.json', 'r', encoding='utf-8') as f:
            coches = json.load(f)
        
        print(f"Actualizando {len(coches)} coches con imágenes de Unsplash...")
        
        for i, coche in enumerate(coches):
            marca = coche.get('marca', '')
            modelo = coche.get('modelo', '')
            año = coche.get('año', 2024)
            
            # Generar URL de imagen (Unsplash)
            url_imagen = generar_url_imagen(marca, modelo, año)
            coche['imagen'] = url_imagen
            
            print(f"[{i+1}/{len(coches)}] {marca} {modelo} ({año})")
        
        # Guardar archivo actualizado
        with open('coches.json', 'w', encoding='utf-8') as f:
            json.dump(coches, f, indent=2, ensure_ascii=False)
        
        print("✅ Archivo coches.json actualizado con imágenes de Unsplash!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    actualizar_imagenes_coches()
