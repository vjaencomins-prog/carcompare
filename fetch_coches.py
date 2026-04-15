#!/usr/bin/env python3
"""
Script para obtener datos de coches desde la API vPIC (NHTSA)
y popular coches.json con información real de múltiples años
"""

import json
import requests
from typing import List, Dict
import time

VPIC_API = "https://vpic.nhtsa.dot.gov/api/vehicles"

# Mapeo de características por modelo
CARACTERISTICAS = {
    # Cilindros por tipo de motor (estimado)
    "3": 3, "4": 4, "5": 5, "6": 6, "8": 8, "10": 10, "12": 12,
    # Por modelo (si contiene la palabra)
    "model_3": ("Tesla", 0, 358, "Eléctrico", "RWD", "Sedán"),
    "model_s": ("Tesla", 0, 670, "Eléctrico", "AWD", "Sedán"),
    "model_x": ("Tesla", 0, 670, "Eléctrico", "AWD", "SUV"),
    "model_y": ("Tesla", 0, 358, "Eléctrico", "RWD", "SUV"),
    "i3": ("BMW", 3, 181, "Eléctrico", "RWD", "Hatchback"),
    "i4": ("BMW", 4, 335, "Eléctrico", "RWD", "Sedán"),
    "leaf": ("Nissan", 0, 147, "Eléctrico", "FWD", "Hatchback"),
    "ariya": ("Nissan", 0, 389, "Eléctrico", "AWD", "SUV"),
    "ioniq": ("Hyundai", 0, 320, "Eléctrico", "AWD", "SUV"),
    "kona": ("Hyundai", 4, 175, "Gasolina", "AWD", "SUV"),
    "santa": ("Hyundai", 6, 277, "Gasolina", "AWD", "SUV"),
    "sportage": ("Kia", 4, 180, "Gasolina", "AWD", "SUV"),
    "sorento": ("Kia", 6, 281, "Gasolina", "AWD", "SUV"),
    "tiguan": ("Volkswagen", 4, 184, "Gasolina", "AWD", "SUV"),
    "golf": ("Volkswagen", 4, 184, "Gasolina", "FWD", "Hatchback"),
    "passat": ("Volkswagen", 4, 174, "Diésel", "FWD", "Sedán"),
    "rav4": ("Toyota", 4, 203, "Gasolina", "AWD", "SUV"),
    "camry": ("Toyota", 4, 203, "Gasolina", "FWD", "Sedán"),
    "corolla": ("Toyota", 4, 169, "Gasolina", "FWD", "Sedán"),
    "cr-v": ("Honda", 4, 190, "Gasolina", "AWD", "SUV"),
    "civic": ("Honda", 4, 174, "Gasolina", "FWD", "Sedán"),
    "accord": ("Honda", 4, 192, "Gasolina", "FWD", "Sedán"),
    "cx-5": ("Mazda", 4, 187, "Gasolina", "AWD", "SUV"),
    "cx-30": ("Mazda", 4, 186, "Gasolina", "AWD", "SUV"),
    "3": ("Mazda", 4, 186, "Gasolina", "FWD", "Sedán"),
    "mustang": ("Ford", 8, 480, "Gasolina", "RWD", "Coupé"),
    "f-150": ("Ford", 8, 400, "Gasolina", "AWD", "Pickup"),
    "escape": ("Ford", 4, 250, "Gasolina", "AWD", "SUV"),
    "explorer": ("Ford", 6, 365, "Gasolina", "AWD", "SUV"),
    "silverado": ("Chevrolet", 8, 420, "Gasolina", "AWD", "Pickup"),
    "traverse": ("Chevrolet", 6, 310, "Gasolina", "AWD", "SUV"),
    "equinox": ("Chevrolet", 4, 210, "Gasolina", "AWD", "SUV"),
    "altima": ("Nissan", 4, 182, "Gasolina", "FWD", "Sedán"),
    "rogue": ("Nissan", 4, 181, "Gasolina", "AWD", "SUV"),
    "350z": ("Nissan", 6, 350, "Gasolina", "RWD", "Coupé"),
    "a4": ("Audi", 4, 261, "Gasolina", "AWD", "Sedán"),
    "a6": ("Audi", 4, 261, "Gasolina", "AWD", "Sedán"),
    "q5": ("Audi", 4, 261, "Gasolina", "AWD", "SUV"),
    "q7": ("Audi", 6, 335, "Gasolina", "AWD", "SUV"),
    "3 series": ("BMW", 4, 255, "Gasolina", "RWD", "Sedán"),
    "5 series": ("BMW", 6, 335, "Gasolina", "AWD", "Sedán"),
    "x3": ("BMW", 4, 382, "Gasolina", "AWD", "SUV"),
    "x5": ("BMW", 6, 523, "Gasolina", "AWD", "SUV"),
    "c-class": ("Mercedes-Benz", 4, 255, "Gasolina", "RWD", "Sedán"),
    "e-class": ("Mercedes-Benz", 6, 362, "Gasolina", "RWD", "Sedán"),
    "s-class": ("Mercedes-Benz", 8, 503, "Gasolina", "RWD", "Sedán"),
    "glc": ("Mercedes-Benz", 4, 255, "Gasolina", "AWD", "SUV"),
    "gle": ("Mercedes-Benz", 6, 362, "Gasolina", "AWD", "SUV"),
    "s60": ("Volvo", 4, 295, "Gasolina", "AWD", "Sedán"),
    "s90": ("Volvo", 6, 345, "Gasolina", "AWD", "Sedán"),
    "xc60": ("Volvo", 4, 295, "Gasolina", "AWD", "SUV"),
    "xc90": ("Volvo", 6, 345, "Gasolina", "AWD", "SUV"),
    "911": ("Porsche", 6, 443, "Gasolina", "RWD", "Coupé"),
    "cayenne": ("Porsche", 6, 443, "Gasolina", "AWD", "SUV"),
    "tacan": ("Porsche", 0, 751, "Eléctrico", "AWD", "Sedán"),
}

def obtener_caracteristicas(marca: str, modelo: str) -> tuple:
    """Obtiene características estimadas para un modelo"""
    modelo_lower = modelo.lower()
    marca_lower = marca.lower()
    
    # Buscar por modelo específico
    for key, value in CARACTERISTICAS.items():
        if isinstance(value, tuple) and key in modelo_lower:
            return value
    
    # Búsqueda general por palabras clave del modelo
    for key, value in CARACTERISTICAS.items():
        if isinstance(value, tuple) and key in modelo_lower:
            return value
    
    # Defaults por marca
    defaults = {
        "tesla": (0, 350, "Eléctrico", "AWD", "SUV"),
        "bmw": (4, 255, "Gasolina", "AWD", "Sedán"),
        "audi": (4, 261, "Gasolina", "AWD", "Sedán"),
        "mercedes": (4, 255, "Gasolina", "RWD", "Sedán"),
        "volkswagen": (4, 184, "Gasolina", "FWD", "Sedan"),
        "toyota": (4, 169, "Gasolina", "FWD", "SUV"),
        "honda": (4, 174, "Gasolina", "FWD", "Sedan"),
        "ford": (4, 250, "Gasolina", "AWD", "SUV"),
        "chevrolet": (4, 210, "Gasolina", "AWD", "SUV"),
        "mazda": (4, 186, "Gasolina", "FWD", "Sedan"),
        "nissan": (4, 181, "Gasolina", "FWD", "Sedan"),
        "hyundai": (4, 175, "Gasolina", "FWD", "SUV"),
        "kia": (4, 180, "Gasolina", "FWD", "SUV"),
        "subaru": (4, 182, "Gasolina", "AWD", "SUV"),
        "volvo": (4, 295, "Gasolina", "AWD", "Sedan"),
        "porsche": (6, 443, "Gasolina", "AWD", "Coupe"),
        "lamborghini": (10, 602, "Gasolina", "AWD", "Coupe"),
        "ferrari": (12, 710, "Gasolina", "RWD", "Coupe"),
        "jaguar": (4, 296, "Gasolina", "RWD", "Sedan"),
        "land rover": (6, 340, "Gasolina", "AWD", "SUV"),
        "renault": (4, 165, "Gasolina", "FWD", "Hatchback"),
        "peugeot": (4, 165, "Gasolina", "FWD", "Sedan"),
        "fiat": (3, 110, "Gasolina", "FWD", "Hatchback"),
    }
    
    for key, value in defaults.items():
        if key in marca_lower:
            return value
    
    # Default universal
    return (4, 180, "Gasolina", "FWD", "SUV")

def obtener_marcas() -> List[str]:
    """Obtiene las marcas principales desde vPIC"""
    print("📥 Obteniendo marcas de vPIC...")
    try:
        response = requests.get(f"{VPIC_API}/getallmakes?format=json", timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Obtener las marcas principales (primeras 40)
        marcas = [item['Make_Name'] for item in data['Results'][:40]]
        print(f"✅ Obtenidas {len(marcas)} marcas")
        return marcas
    except Exception as e:
        print(f"❌ Error obteniendo marcas: {e}")
        # Fallback a marcas populares
        return [
            "BMW", "Audi", "Mercedes-Benz", "Volkswagen", "Toyota", "Honda", 
            "Ford", "Chevrolet", "Mazda", "Nissan", "Hyundai", "Kia", 
            "Subaru", "Volvo", "Tesla", "Porsche", "Lamborghini", "Ferrari",
            "Jaguar", "Land Rover", "Renault", "Peugeot", "Fiat", "Alfa Romeo"
        ]

def obtener_modelos(marca: str, año: int) -> List[str]:
    """Obtiene los modelos para una marca y año específicos"""
    try:
        response = requests.get(
            f"{VPIC_API}/getmodelsformakeyear/make/{marca}/modelyear/{año}?format=json",
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        modelos = [item['Model_Name'] for item in data.get('Results', [])]
        return modelos[:5]  # Limitar a 5 modelos por año
    except Exception as e:
        print(f"⚠️  Error obteniendo modelos para {marca} {año}: {e}")
        return []

def crear_coches_json() -> None:
    """Crea un coches.json con datos de vPIC y características realistas"""
    coches = []
    marcas = obtener_marcas()
    años = [2024, 2023, 2022, 2021, 2020, 2019, 2018]
    contador = 0
    max_coches = 150
    
    print(f"\n🚗 Obteniendo modelos para {len(marcas)} marcas y {len(años)} años...")
    print("=" * 60)
    
    for marca in marcas:
        if contador >= max_coches:
            break
            
        print(f"\n🏎️  {marca}")
        
        for año in años[:3]:  # Solo últimos 3 años para limitar tiempo
            if contador >= max_coches:
                break
                
            modelos = obtener_modelos(marca, año)
            print(f"  └─ {año}: {len(modelos)} modelos", end="")
            
            for modelo in modelos[:2]:  # Máximo 2 modelos por marca-año
                if contador >= max_coches:
                    break
                
                cilindros, potencia, combustible, traccion, carroceria = obtener_caracteristicas(marca, modelo)
                
                coche = {
                    "marca": marca,
                    "modelo": modelo,
                    "año": año,
                    "cilindros": cilindros,
                    "potencia": potencia,
                    "combustible": combustible,
                    "traccion": traccion,
                    "carroceria": carroceria
                }
                
                coches.append(coche)
                contador += 1
            
            if modelos:
                print(" ✅")
            else:
                print()
            
            time.sleep(0.5)  # Evitar saturar la API
    
    # Guardar a JSON
    output_file = "./coches.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(coches, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print(f"✅ Guardado {len(coches)} coches en {output_file}")
    print(f"📊 Años cubiertos: {sorted(set(c['año'] for c in coches), reverse=True)}")
    print(f"🏢 Marcas: {len(set(c['marca'] for c in coches))}")

if __name__ == "__main__":
    crear_coches_json()
