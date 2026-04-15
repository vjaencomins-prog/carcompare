import json
import requests
import time

VPIC_API = 'https://vpic.nhtsa.dot.gov/api/vehicles'

print("Obteniendo todas las marcas de vPIC...")
response = requests.get(f'{VPIC_API}/getallmakes?format=json')
makes_data = response.json()
makes = [item['Make_Name'] for item in makes_data.get('Results', [])]

print(f"Encontradas {len(makes)} marcas")

coches = []
años = [2023, 2022, 2021, 2020]

# Procesar cada marca
for i, make in enumerate(makes[:80]):  # 80 marcas
    print(f"[{i+1}/80] Procesando {make}...")
    
    # Para cada año, obtener modelos
    for año in años:
        try:
            response = requests.get(
                f'{VPIC_API}/getmodelsformakeyear/make/{make}/modelyear/{año}?format=json',
                timeout=5
            )
            data = response.json()
            
            for item in data.get('Results', [])[:2]:
                coche = {
                    "marca": make,
                    "modelo": item.get('Model_Name', ''),
                    "año": año
                }
                coches.append(coche)
                
            time.sleep(0.05)
        except Exception as e:
            continue

# Eliminar duplicados
unique_coches = []
seen = set()
for coche in coches:
    key = (coche['marca'], coche['modelo'], coche['año'])
    if key not in seen:
        seen.add(key)
        unique_coches.append(coche)

print(f"\nTotal de coches únicos: {len(unique_coches)}")

# Guardar en JSON
with open('coches.json', 'w', encoding='utf-8') as f:
    json.dump(unique_coches, f, ensure_ascii=False, indent=2)

print("✅ coches.json actualizado con datos de vPIC")
marcas_unicas = len(set(c['marca'] for c in unique_coches))
print(f"Archivo contiene {len(unique_coches)} vehículos de {marcas_unicas} marcas")
