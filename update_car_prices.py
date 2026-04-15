import json
import random

# Precios base aproximados en USD para modelos populares (2024)
PRECIOS_BASE = {
    'BMW': {
        '3 Series': 45000,
        '5 Series': 60000,
        'X3': 50000,
        'X5': 65000,
        'X7': 80000
    },
    'Audi': {
        'A3': 38000,
        'A4': 45000,
        'A6': 55000,
        'Q5': 50000,
        'Q7': 65000
    },
    'Mercedes-Benz': {
        'C-Class': 48000,
        'E-Class': 58000,
        'S-Class': 110000,
        'GLC': 52000,
        'GLE': 60000
    },
    'Volkswagen': {
        'Golf': 28000,
        'Passat': 32000,
        'Tiguan': 30000,
        'Touareg': 55000
    },
    'Toyota': {
        'Corolla': 22000,
        'Camry': 28000,
        'RAV4': 30000,
        'Highlander': 40000,
        'Prius': 29000
    },
    'Honda': {
        'Civic': 24000,
        'Accord': 29000,
        'CR-V': 31000,
        'Pilot': 38000
    },
    'Ford': {
        'Focus': 22000,
        'Mustang': 35000,
        'Explorer': 38000,
        'F-150': 40000
    }
}

def calcular_precio_mercado(marca, modelo, año):
    """
    Calcula precio aproximado basado en marca, modelo y año
    Simula precios de mercado realistas
    """
    try:
        marca_normalizada = marca.strip()
        modelo_normalizado = modelo.strip()

        # Buscar precio base
        precio_base = None
        if marca_normalizada in PRECIOS_BASE:
            modelos_marca = PRECIOS_BASE[marca_normalizada]
            # Buscar modelo exacto o parcial
            for mod, precio in modelos_marca.items():
                if mod.lower() in modelo_normalizado.lower() or modelo_normalizado.lower() in mod.lower():
                    precio_base = precio
                    break

        if not precio_base:
            # Precio por defecto basado en marca
            precios_marca_default = {
                'BMW': 55000,
                'Audi': 45000,
                'Mercedes-Benz': 60000,
                'Volkswagen': 30000,
                'Toyota': 28000,
                'Honda': 28000,
                'Ford': 30000
            }
            precio_base = precios_marca_default.get(marca_normalizada, 35000)

        # Ajustar por año (depreciación aproximada)
        años_diferencia = 2024 - año
        depreciacion_anual = 0.08  # 8% por año
        factor_depreciacion = (1 - depreciacion_anual) ** años_diferencia

        precio_calculado = precio_base * factor_depreciacion

        # Añadir variación aleatoria (±10%)
        variacion = random.uniform(0.9, 1.1)
        precio_final = int(precio_calculado * variacion)

        return precio_final

    except Exception as e:
        print(f"Error calculando precio para {marca} {modelo} {año}: {e}")
        return None

def actualizar_precios_coches():
    """Lee coches.json y actualiza los precios con cálculos aproximados"""
    try:
        with open('coches.json', 'r', encoding='utf-8') as f:
            coches = json.load(f)

        print(f"Actualizando precios para {len(coches)} coches con cálculos aproximados...")

        for i, coche in enumerate(coches):
            marca = coche.get('marca', '')
            modelo = coche.get('modelo', '')
            año = coche.get('año', 2024)

            if not marca or not modelo:
                print(f"[{i+1}/{len(coches)}] Saltando {marca} {modelo} - datos insuficientes")
                continue

            precio = calcular_precio_mercado(marca, modelo, año)
            if precio:
                coche['precio'] = precio
                print(f"[{i+1}/{len(coches)}] {marca} {modelo} ({año}) - ${precio:,}")
            else:
                if 'precio' not in coche:
                    coche['precio'] = None
                print(f"[{i+1}/{len(coches)}] {marca} {modelo} ({año}) - Precio no disponible")

        # Guardar archivo actualizado
        with open('coches.json', 'w', encoding='utf-8') as f:
            json.dump(coches, f, indent=2, ensure_ascii=False)

        print("✅ Archivo coches.json actualizado con precios aproximados!")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    actualizar_precios_coches()