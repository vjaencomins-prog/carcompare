#!/usr/bin/env python3
"""
Script para obtener datos de coches desde CarQuery API
y popular coches.json con información detallada
"""

import json
import requests
from typing import List, Dict, Optional
import time

# CarQuery API
CARQUERY_API = "http://www.carqueryapi.com/api/0.3"

# CORS proxy alternativo si carquery falla
CORS_PROXY = "https://cors-anywhere.herokuapp.com/"

def obtener_años() -> List[int]:
    """Obtiene los años disponibles en CarQuery"""
    print("📅 Obteniendo años disponibles...")
    try:
        response = requests.get(f"{CARQUERY_API}/?cmd=getYears", timeout=10)
        response.raise_for_status()
        data = response.json()
        años = [int(año) for año in data.get('Years', [])]
        print(f"✅ Años obtenidos: {sorted(años, reverse=True)[:10]}")
        return sorted(años, reverse=True)[:10]  # Últimos 10 años
    except Exception as e:
        print(f"❌ Error obteniendo años: {e}")
        return list(range(2024, 2014, -1))  # Fallback

def obtener_marcas(año: int) -> List[str]:
    """Obtiene las marcas para un año específico"""
    try:
        response = requests.get(
            f"{CARQUERY_API}/?cmd=getMakes&year={año}",
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        marcas = [item['make_display'] for item in data.get('Makes', [])]
        return marcas[:15]  # Limitar a 15 marcas
    except Exception as e:
        print(f"⚠️  Error obteniendo marcas para {año}: {e}")
        return []

def obtener_modelos(año: int, marca: str) -> List[Dict]:
    """Obtiene los modelos para una marca y año específicos"""
    try:
        # Limpieza de marca para la API
        make_id = marca.lower().replace(' ', '_')
        
        response = requests.get(
            f"{CARQUERY_API}/?cmd=getModels&year={año}&make={make_id}",
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        modelos = data.get('Models', [])
        return modelos[:5]  # Máximo 5 modelos por marca-año
    except Exception as e:
        print(f"⚠️  Error obteniendo modelos para {marca} {año}: {e}")
        return []

def obtener_detalles_modelo(modelo_id: str) -> Optional[Dict]:
    """Obtiene información detallada del modelo"""
    try:
        response = requests.get(
            f"{CARQUERY_API}/?cmd=getModel&model={modelo_id}",
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"⚠️  Error obteniendo detalles del modelo: {e}")
        return None

def mapear_combustible(fuel_type: str) -> str:
    """Mapea tipos de combustible de CarQuery a valores estándar"""
    fuel = fuel_type.lower() if fuel_type else "gasolina"
    
    if "electric" in fuel or "ev" in fuel:
        return "Eléctrico"
    elif "hybrid" in fuel or "phev" in fuel:
        return "Híbrido"
    elif "diesel" in fuel or "biodiesel" in fuel:
        return "Diésel"
    elif "lpg" in fuel or "gnc" in fuel:
        return "GNC"
    else:
        return "Gasolina"

def mapear_carroceria(body_type: str) -> str:
    """Mapea tipos de carrocería"""
    if not body_type:
        return "Sedán"
    
    body = body_type.lower()
    
    if "suv" in body or "crossover" in body:
        return "SUV"
    elif "sedan" in body or "saloon" in body:
        return "Sedán"
    elif "coupe" in body or "coupé" in body:
        return "Coupé"
    elif "convertible" in body or "cabrio" in body:
        return "Descapotable"
    elif "hatchback" in body:
        return "Hatchback"
    elif "wagon" in body or "estate" in body:
        return "Familiar"
    elif "truck" in body or "pickup" in body:
        return "Pickup"
    elif "van" in body or "minivan" in body:
        return "Minivan"
    else:
        return "Sedán"

def estimar_potencia(modelo: str, marca: str) -> int:
    """Estima potencia basada en modelo y marca"""
    potencias = {
        "model s": 670, "model 3": 358, "model x": 670, "model y": 358,
        "911": 443, "cayenne": 443, "taycan": 751,
        "b-m-w": 295, "3 series": 255, "5 series": 335,
        "a3": 200, "a4": 261, "a6": 261, "a8": 456,
        "c-class": 255, "e-class": 362, "s-class": 503,
        "golf": 184, "passat": 174, "tiguan": 184,
        "corolla": 169, "camry": 203, "rav4": 203,
        "civic": 174, "accord": 192, "cr-v": 190,
        "mazda 3": 186, "mazda 6": 187, "cx-5": 187,
        "altima": 182, "rogue": 181, "sentra": 149,
        "elantra": 147, "kona": 175, "santa fe": 277,
        "rio": 120, "sportage": 180, "sorento": 281,
        "impreza": 182, "forester": 182,
        "s60": 295, "s90": 345, "xc60": 295, "xc90": 345,
        "mustang": 480, "f-150": 400, "escape": 250, "explorer": 365,
        "silverado": 420, "malibu": 160, "equinox": 210,
    }
    
    modelo_lower = modelo.lower()
    marca_lower = marca.lower()
    
    for key, power in potencias.items():
        if key in modelo_lower or key in f"{marca_lower} {modelo_lower}":
            return power
    
    # Default por marca
    if "tesla" in marca_lower:
        return 350
    elif "porsche" in marca_lower:
        return 450
    elif "lamborghini" in marca_lower:
        return 600
    elif "ferrari" in marca_lower:
        return 700
    elif "bmw" in marca_lower or "mercedes" in marca_lower or "audi" in marca_lower:
        return 250
    elif "toyota" in marca_lower or "honda" in marca_lower or "mazda" in marca_lower:
        return 180
    else:
        return 200

def estimar_cilindros(potencia: int) -> int:
    """Estima cilindros basados en potencia"""
    if potencia == 0:  # Eléctrico
        return 0
    elif potencia < 120:
        return 3
    elif potencia < 200:
        return 4
    elif potencia < 350:
        return 6
    elif potencia < 500:
        return 8
    else:
        return 12

def crear_coches_json() -> None:
    """Crea un coches.json con datos de CarQuery API"""
    coches = []
    años = obtener_años()
    contador = 0
    max_coches = 100
    
    print(f"\n🚗 Obteniendo coches desde CarQuery API...")
    print("=" * 70)
    
    for año in años[:5]:  # Últimos 5 años
        if contador >= max_coches:
            break
        
        marcas = obtener_marcas(año)
        print(f"\n📆 Año {año}: {len(marcas)} marcas")
        
        for marca in marcas:
            if contador >= max_coches:
                break
            
            modelos = obtener_modelos(año, marca)
            print(f"  └─ {marca}: {len(modelos)} modelos", end="")
            
            for modelo in modelos[:2]:  # Máximo 2 modelos por marca
                if contador >= max_coches:
                    break
                
                try:
                    # Información básica del modelo
                    modelo_nombre = modelo.get('model_name', 'Modelo')
                    modelo_id = modelo.get('model_id', '')
                    
                    # Obtener detalles si disponible
                    detalles = obtener_detalles_modelo(modelo_id) if modelo_id else None
                    
                    # Información derivada
                    combustible = mapear_combustible(
                        detalles.get('model_engine_fuel_type', '') if detalles else ""
                    )
                    potencia = estimar_potencia(modelo_nombre, marca)
                    cilindros = estimar_cilindros(potencia)
                    carroceria = mapear_carroceria(
                        detalles.get('model_body', '') if detalles else ""
                    )
                    
                    # Asumir tracción AWD para la mayoría
                    traccion = "AWD" if "SUV" in carroceria else "FWD"
                    if "Porsche" in marca or "Ferrari" in marca or "Lamborghini" in marca:
                        traccion = "RWD" if "SUV" not in carroceria else "AWD"
                    
                    coche = {
                        "marca": marca,
                        "modelo": modelo_nombre,
                        "año": año,
                        "cilindros": cilindros,
                        "potencia": potencia,
                        "combustible": combustible,
                        "traccion": traccion,
                        "carroceria": carroceria,
                        "source": "CarQuery"
                    }
                    
                    coches.append(coche)
                    contador += 1
                    
                except Exception as e:
                    print(f"Error procesando {marca} {modelo_nombre}: {e}")
                    continue
            
            if modelos:
                print(" ✅")
            else:
                print()
            
            time.sleep(0.3)  # Evitar saturar la API
    
    # Ordenar por año (descendente) y marca
    coches.sort(key=lambda x: (-x['año'], x['marca'], x['modelo']))
    
    # Guardar a JSON
    output_file = "./coches.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(coches, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 70)
    print(f"✅ Guardado {len(coches)} coches en {output_file}")
    print(f"📊 Estadísticas:")
    print(f"  • Años cubiertos: {sorted(set(c['año'] for c in coches), reverse=True)}")
    print(f"  • Marcas: {len(set(c['marca'] for c in coches))}")
    print(f"  • Combustibles: {set(c['combustible'] for c in coches)}")
    print(f"  • Carrocerías: {set(c['carroceria'] for c in coches)}")

if __name__ == "__main__":
    crear_coches_json()
