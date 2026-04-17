#!/usr/bin/env python3
"""
Script para cargar coches desde API Ninjas y fusionarlos con coches.json.
Esta versión usa los endpoints de carmakes, carmodels y cars para traer datos
reales de combustibles, año y características.
"""

import json
import time
import urllib.parse
from typing import Any, Dict, List, Optional

import requests

API_KEY = "lj6xN3OecqDATtbZakrfjqVqlEOylHpCboJf5qUS"
BASE_URL = "https://api.api-ninjas.com/v1"
HEADERS = {"X-Api-Key": API_KEY}

INPUT_FILE = "coches.json"
OUTPUT_FILE = "coches.json"
MAX_MODEL_PER_MAKE = 8
MAX_CARS_PER_MODEL = 10
SLEEP_SECONDS = 0.5


def fetch_json(path: str, params: Optional[Dict[str, str]] = None) -> Any:
    url = f"{BASE_URL}/{path}"
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as exc:
        print(f"ERROR HTTP {response.status_code} en {url}: {response.text}")
    except Exception as exc:
        print(f"ERROR en {url}: {exc}")
    return None


def obtener_makes_ninjas() -> List[str]:
    data = fetch_json("carmakes")
    if not isinstance(data, list):
        return []
    return [item.get("name", item.get("make", "")).strip() for item in data if item]


def obtener_models_ninjas(make: str) -> List[str]:
    data = fetch_json("carmodels", {"make": make})
    if not isinstance(data, list):
        return []
    return [item.get("model", item.get("name", "")).strip() for item in data if item]


def obtener_cars_ninjas(make: str, model: str) -> List[Dict[str, Any]]:
    data = fetch_json("cars", {"make": make, "model": model})
    if not isinstance(data, list):
        return []
    return data


def obtener_trims_ninjas(make: str, model: str) -> List[Dict[str, Any]]:
    data = fetch_json("cartrims", {"make": make, "model": model})
    if not isinstance(data, list):
        return []
    return data


def crear_coche_desde_trim_api(item: Dict[str, Any], electric_makes: Optional[set] = None) -> Dict[str, Any]:
    marca = item.get("make") or item.get("make_display") or "Desconocido"
    modelo = item.get("model") or item.get("model_display") or "Desconocido"
    año = int(item.get("year") or 0)
    combustible_raw = item.get("fuel_type") or item.get("fuel") or item.get("fuelType")
    combustible = normalizar_combustible(combustible_raw)
    if combustible == "Desconocido" and electric_makes and str(marca).strip().lower() in electric_makes:
        combustible = "Eléctrico"
    carroceria = normalizar_carroceria(item.get("body_type") or item.get("bodyType") or item.get("trim"))
    traccion = normalizar_traccion(item.get("drive") or item.get("drive_type") or item.get("driveType"))
    cilindros = int(item.get("cylinders") or item.get("engine_cylinders") or 0)
    potencia = int(item.get("horsepower") or item.get("hp") or 0)
    precio = int(item.get("price") or item.get("msrp") or 0)

    return {
        "marca": marca.strip(),
        "modelo": modelo.strip(),
        "año": año,
        "km": item.get("miles") or item.get("mileage") or None,
        "cilindros": cilindros,
        "potencia": potencia,
        "combustible": combustible,
        "traccion": traccion,
        "carroceria": carroceria,
        "precio": precio,
        "categoria": combustible,
        "source": "API Ninjas",
        "trim": item.get("trim") or item.get("trim_name") or None,
    }


def obtener_electric_makes_ninjas() -> List[str]:
    data = fetch_json("electricvehiclemakes")
    if not isinstance(data, list):
        return []
    return [item.get("make", item.get("name", "")).strip() for item in data if item]


def normalizar_combustible(value: Optional[str]) -> str:
    if not value:
        return "Desconocido"
    fuel = value.lower()
    if "elect" in fuel or "ev" in fuel:
        return "Eléctrico"
    if "diesel" in fuel:
        return "Diésel"
    if "hybrid" in fuel or "híbrid" in fuel:
        return "Híbrido"
    if "gas" in fuel:
        return "Gasolina"
    return value.title()


def normalizar_carroceria(body_type: Optional[str]) -> str:
    if not body_type:
        return "Sedán"
    body = body_type.lower()
    if "suv" in body or "crossover" in body:
        return "SUV"
    if "sedan" in body or "saloon" in body:
        return "Sedán"
    if "coupe" in body or "coupé" in body:
        return "Coupé"
    if "hatch" in body:
        return "Hatchback"
    if "wagon" in body or "estate" in body or "familiar" in body:
        return "Familiar"
    if "van" in body or "minivan" in body or "bus" in body:
        return "Minivan"
    if "truck" in body or "pickup" in body:
        return "Pickup"
    return body_type.title()


def normalizar_traccion(drive: Optional[str]) -> str:
    if not drive:
        return "FWD"
    text = drive.lower()
    if "awd" in text or "4wd" in text or "4x4" in text:
        return "AWD"
    if "rwd" in text or "rear" in text:
        return "RWD"
    if "fwd" in text or "front" in text:
        return "FWD"
    return drive


def crear_coche_desde_api(item: Dict[str, Any], electric_makes: Optional[set] = None) -> Dict[str, Any]:
    marca = item.get("make") or item.get("make_display") or "Desconocido"
    modelo = item.get("model") or item.get("model_display") or "Desconocido"
    año = int(item.get("year") or 0)
    combustible_raw = item.get("fuel_type") or item.get("fuel") or item.get("fuelType")
    combustible = normalizar_combustible(combustible_raw)
    if combustible == "Desconocido" and electric_makes and str(marca).strip().lower() in electric_makes:
        combustible = "Eléctrico"
    carroceria = normalizar_carroceria(item.get("body_type") or item.get("bodyType") or item.get("trim"))
    traccion = normalizar_traccion(item.get("drive") or item.get("drive_type") or item.get("driveType"))
    cilindros = int(item.get("cylinders") or item.get("engine_cylinders") or 0)
    potencia = int(item.get("horsepower") or item.get("hp") or 0)
    precio = int(item.get("price") or item.get("msrp") or 0)

    return {
        "marca": marca.strip(),
        "modelo": modelo.strip(),
        "año": año,
        "km": item.get("miles") or item.get("mileage") or None,
        "cilindros": cilindros,
        "potencia": potencia,
        "combustible": combustible,
        "traccion": traccion,
        "carroceria": carroceria,
        "precio": precio,
        "categoria": combustible,
        "source": "API Ninjas"
    }


def clave_coche(coche: Dict[str, Any]) -> str:
    return "|".join([
        str(coche.get("marca", "")).strip().lower(),
        str(coche.get("modelo", "")).strip().lower(),
        str(coche.get("año", "")),
        str(coche.get("combustible", "")).strip().lower()
    ])


def cargar_json_existente(path: str) -> List[Dict[str, Any]]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        print(f"ERROR leyendo {path}: {exc}")
        return []


def guardar_json(path: str, coches: List[Dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(coches, f, ensure_ascii=False, indent=2)


def merge_cars(existing: List[Dict[str, Any]], new_cars: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    vistos = {clave_coche(coche): coche for coche in existing}
    for coche in new_cars:
        key = clave_coche(coche)
        if key not in vistos:
            vistos[key] = coche
    return list(vistos.values())


def main() -> None:
    existing = cargar_json_existente(INPUT_FILE)
    existing_keys = {clave_coche(coche) for coche in existing}
    print(f"Cargados {len(existing)} coches existentes y {len(existing_keys)} claves únicas.")

    makes = obtener_makes_ninjas()
    if not makes:
        print("No se pudieron obtener marcas de API Ninjas. Revisa la suscripción o la clave.")
        return

    electric_makes = set(name.strip().lower() for name in obtener_electric_makes_ninjas())
    if electric_makes:
        print(f"Marcas eléctricas reconocidas: {len(electric_makes)}")

    todos_nuevos: List[Dict[str, Any]] = []
    marcas_relevantes = sorted(set(str(c.get("marca", "")).strip() for c in existing if c.get("marca")))
    print(f"Marcas relevantes en fichero: {len(marcas_relevantes)}")

    for make in marcas_relevantes:
        print(f"Buscando modelos de {make}...")
        models = obtener_models_ninjas(make)
        if not models:
            continue

        for modelo in models[:MAX_MODEL_PER_MAKE]:
            print(f"  - Modelo {modelo}")

            cars = obtener_cars_ninjas(make, modelo)
            if cars:
                for raw in cars[:MAX_CARS_PER_MODEL]:
                    coche = crear_coche_desde_api(raw, electric_makes=electric_makes)
                    if clave_coche(coche) not in existing_keys:
                        todos_nuevos.append(coche)
                        existing_keys.add(clave_coche(coche))
                time.sleep(SLEEP_SECONDS)
            else:
                trims = obtener_trims_ninjas(make, modelo)
                if trims:
                    for raw in trims[:MAX_CARS_PER_MODEL]:
                        coche = crear_coche_desde_trim_api(raw, electric_makes=electric_makes)
                        if clave_coche(coche) not in existing_keys:
                            todos_nuevos.append(coche)
                            existing_keys.add(clave_coche(coche))
                    time.sleep(SLEEP_SECONDS)

            # Complemento con trims si hay menos resultados directos de cars
            if cars and len(cars) < MAX_CARS_PER_MODEL:
                trims = obtener_trims_ninjas(make, modelo)
                for raw in trims[:max(0, MAX_CARS_PER_MODEL - len(cars))]:
                    coche = crear_coche_desde_trim_api(raw, electric_makes=electric_makes)
                    if clave_coche(coche) not in existing_keys:
                        todos_nuevos.append(coche)
                        existing_keys.add(clave_coche(coche))
                time.sleep(SLEEP_SECONDS)

        time.sleep(SLEEP_SECONDS)

    total = merge_cars(existing, todos_nuevos)
    print(f"Añadidos {len(todos_nuevos)} coches nuevos. Total combinado: {len(total)}.")
    guardar_json(OUTPUT_FILE, total)
    print(f"Archivo actualizado: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
