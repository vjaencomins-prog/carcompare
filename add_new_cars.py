#!/usr/bin/env python3
"""
Script para añadir los nuevos coches proporcionados por el usuario a coches.json.
Los datos vienen de respuestas de API para Aston Martin, Ferrari, Jeep y DeLorean.
"""

import json
import random

# Datos proporcionados por el usuario (respuestas de API)
api_responses = [
    {"Count":18,"Message":"Response returned successfully","SearchCriteria":"Make:aston martin","Results":[{"Make_ID":440,"Make_Name":"Aston Martin","Model_ID":1684,"Model_Name":"V8 Vantage"},{"Make_ID":440,"Make_Name":"Aston Martin","Model_ID":1686,"Model_Name":"DBS"},{"Make_ID":440,"Make_Name":"Aston Martin","Model_ID":1687,"Model_Name":"DB9"},{"Make_ID":440,"Make_Name":"Aston Martin","Model_ID":1688,"Model_Name":"Rapide"},{"Make_ID":440,"Make_Name":"Aston Martin","Model_ID":1695,"Model_Name":"V12 Vantage"},{"Make_ID":440,"Make_Name":"Aston Martin","Model_ID":1697,"Model_Name":"Virage"},{"Make_ID":440,"Make_Name":"Aston Martin","Model_ID":1701,"Model_Name":"Vanquish"},{"Make_ID":440,"Make_Name":"Aston Martin","Model_ID":13751,"Model_Name":"DB11"},{"Make_ID":440,"Make_Name":"Aston Martin","Model_ID":14157,"Model_Name":"Lagonda"},{"Make_ID":440,"Make_Name":"Aston Martin","Model_ID":14162,"Model_Name":"Vantage"},{"Make_ID":440,"Make_Name":"Aston Martin","Model_ID":14164,"Model_Name":"V8"},{"Make_ID":440,"Make_Name":"Aston Martin","Model_ID":19610,"Model_Name":"Vanquish Zagato"},{"Make_ID":440,"Make_Name":"Aston Martin","Model_ID":27591,"Model_Name":"DBX"},{"Make_ID":440,"Make_Name":"Aston Martin","Model_ID":32082,"Model_Name":"DB12"},{"Make_ID":440,"Make_Name":"Aston Martin","Model_ID":33264,"Model_Name":"Valour"},{"Make_ID":440,"Make_Name":"Aston Martin","Model_ID":35163,"Model_Name":"DB7"},{"Make_ID":440,"Make_Name":"Aston Martin","Model_ID":35216,"Model_Name":"Valiant"},{"Make_ID":440,"Make_Name":"Aston Martin","Model_ID":36621,"Model_Name":"Valhalla"}]},
    {"Count":60,"Message":"Response returned successfully","SearchCriteria":"Make:ferrari","Results":[{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":3601,"Model_Name":"612 Scaglietti"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":3603,"Model_Name":"599"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":3605,"Model_Name":"599 GTB Fiorano"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":3606,"Model_Name":"430"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":3607,"Model_Name":"F430"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":9940,"Model_Name":"360"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":9941,"Model_Name":"575M Maranello"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":9942,"Model_Name":"456M"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":9944,"Model_Name":"Enzo"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":9954,"Model_Name":"F355"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":9957,"Model_Name":"550 Maranello"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":13843,"Model_Name":"F12 Berlinetta"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":13849,"Model_Name":"California T"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":13850,"Model_Name":"FF"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":13851,"Model_Name":"La Ferrari"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":13852,"Model_Name":"458 Italia"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":13855,"Model_Name":"458"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":13856,"Model_Name":"California"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":14016,"Model_Name":"348 tb"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":14017,"Model_Name":"348 ts"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":14020,"Model_Name":"512 TR"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":14024,"Model_Name":"355 Berlinetta"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":14025,"Model_Name":"355 GTS"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":14026,"Model_Name":"348 Spider"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":14027,"Model_Name":"456"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":14028,"Model_Name":"355 Spider"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":14031,"Model_Name":"Mondial T"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":14038,"Model_Name":"Testarossa"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":14039,"Model_Name":"F40"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":14047,"Model_Name":"328 GTB"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":14048,"Model_Name":"328 GTS"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":14049,"Model_Name":"3.2 Mondial"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":14050,"Model_Name":"328"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":14052,"Model_Name":"308GTB Quattrovalvole"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":14053,"Model_Name":"308GTS Quattrovalvole"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":14055,"Model_Name":"Mondial 8"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":14056,"Model_Name":"308 Convertible"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":14113,"Model_Name":"F12 Special Series"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":14114,"Model_Name":"F60 America"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":14598,"Model_Name":"308GTBi"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":14599,"Model_Name":"308GTSi"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":14600,"Model_Name":"308GTB"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":14601,"Model_Name":"308GTS"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":25180,"Model_Name":"F12 tdf (Tour de France)"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":25181,"Model_Name":"GTC4Lusso"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":26486,"Model_Name":"488"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":26488,"Model_Name":"Portofino"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":27823,"Model_Name":"812"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":27825,"Model_Name":"F8"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":27827,"Model_Name":"Roma"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":31617,"Model_Name":"Challenge Stradale"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":31829,"Model_Name":"Portofino M"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":31831,"Model_Name":"SF90"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":31833,"Model_Name":"550 Barchetta"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":31836,"Model_Name":"F50"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":31864,"Model_Name":"Purosangue"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":31865,"Model_Name":"Monza SP1/SP2"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":31866,"Model_Name":"Daytona SP3"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":31868,"Model_Name":"296"},{"Make_ID":603,"Make_Name":"Ferrari","Model_ID":34095,"Model_Name":"12Cilindri"}]},
    {"Count":24,"Message":"Response returned successfully","SearchCriteria":"Make:jeep","Results":[{"Make_ID":483,"Make_Name":"Jeep","Model_ID":1943,"Model_Name":"Wrangler"},{"Make_ID":483,"Make_Name":"Jeep","Model_ID":1944,"Model_Name":"Liberty"},{"Make_ID":483,"Make_Name":"Jeep","Model_ID":1945,"Model_Name":"Cherokee"},{"Make_ID":483,"Make_Name":"Jeep","Model_ID":1946,"Model_Name":"Compass"},{"Make_ID":483,"Make_Name":"Jeep","Model_ID":1947,"Model_Name":"Patriot"},{"Make_ID":483,"Make_Name":"Jeep","Model_ID":1948,"Model_Name":"Commander"},{"Make_ID":483,"Make_Name":"Jeep","Model_ID":1949,"Model_Name":"Grand Cherokee"},{"Make_ID":483,"Make_Name":"Jeep","Model_ID":6160,"Model_Name":"Renegade"},{"Make_ID":483,"Make_Name":"Jeep","Model_ID":14871,"Model_Name":"Grand Wagoneer"},{"Make_ID":483,"Make_Name":"Jeep","Model_ID":14905,"Model_Name":"Comanche"},{"Make_ID":483,"Make_Name":"Jeep","Model_ID":14927,"Model_Name":"Wagoneer"},{"Make_ID":483,"Make_Name":"Jeep","Model_ID":14978,"Model_Name":"J-10"},{"Make_ID":483,"Make_Name":"Jeep","Model_ID":14979,"Model_Name":"J-20"},{"Make_ID":483,"Make_Name":"Jeep","Model_ID":15073,"Model_Name":"CJ-7"},{"Make_ID":483,"Make_Name":"Jeep","Model_ID":15074,"Model_Name":"CJ-8 Scrambler"},{"Make_ID":483,"Make_Name":"Jeep","Model_ID":15086,"Model_Name":"CJ-5"},{"Make_ID":483,"Make_Name":"Jeep","Model_ID":15090,"Model_Name":"CJ-6"},{"Make_ID":483,"Make_Name":"Jeep","Model_ID":25197,"Model_Name":"Wrangler JK"},{"Make_ID":483,"Make_Name":"Jeep","Model_ID":25919,"Model_Name":"Gladiator"},{"Make_ID":483,"Make_Name":"Jeep","Model_ID":32375,"Model_Name":"Grand Cherokee L"},{"Make_ID":483,"Make_Name":"Jeep","Model_ID":32377,"Model_Name":"Wagoneer L"},{"Make_ID":483,"Make_Name":"Jeep","Model_ID":32378,"Model_Name":"Grand Wagoneer L"},{"Make_ID":483,"Make_Name":"Jeep","Model_ID":34270,"Model_Name":"Wagoneer S"},{"Make_ID":483,"Make_Name":"Jeep","Model_ID":37249,"Model_Name":"Recon"}]},
    {"Count":1,"Message":"Response returned successfully","SearchCriteria":"Make:delorean","Results":[{"Make_ID":13022,"Make_Name":"DeLorean","Model_ID":34304,"Model_Name":"DMC-12"}]}
]

# Descripciones base por marca
descripciones_base = {
    "Aston Martin": "Coche de lujo británico con un diseño elegante y prestaciones excepcionales. Ideal para quienes buscan exclusividad y rendimiento en carretera.",
    "Ferrari": "Ícono italiano de velocidad y lujo. Conduce con pasión y estilo inigualable, perfecto para amantes de la adrenalina.",
    "Jeep": "Vehículo todoterreno 4x4 diseñado para conquistar montañas y terrenos difíciles. Resistente y versátil para aventuras off-road.",
    "DeLorean": "Una joya antigua del automovilismo, famosa por su diseño futurista y su papel en la cultura pop. Un clásico atemporal."
}

def crear_coche_desde_modelo(make_name, model_name):
    marca = make_name
    modelo = model_name
    año = 2024  # Asumiendo coches nuevos
    combustible = "Gasolina"
    categoria = "gasolina"
    descripcion = descripciones_base.get(marca, "Coche con características destacadas.")
    imagen = f"https://source.unsplash.com/featured/400x300?{marca.lower().replace(' ', '')},{modelo.lower().replace(' ', '')},car"
    precio = random.randint(50000, 500000)  # Precio aleatorio alto para lujo
    cilindros = 8 if marca in ["Aston Martin", "Ferrari"] else 6
    potencia = random.randint(300, 700)
    traccion = "AWD" if marca == "Jeep" else "RWD"
    carroceria = "SUV" if marca == "Jeep" else "Coupé"

    return {
        "marca": marca,
        "modelo": modelo,
        "año": año,
        "cilindros": cilindros,
        "potencia": potencia,
        "combustible": combustible,
        "traccion": traccion,
        "carroceria": carroceria,
        "imagen": imagen,
        "precio": precio,
        "descripcion": descripcion,
        "categoria": categoria
    }

def main():
    # Cargar coches existentes
    try:
        with open("coches.json", "r", encoding="utf-8") as f:
            coches = json.load(f)
    except FileNotFoundError:
        coches = []

    nuevos_coches = []
    for response in api_responses:
        make_name = response["SearchCriteria"].split(":")[1].replace(" ", "").title()  # e.g., Aston Martin
        for result in response["Results"]:
            modelo = result["Model_Name"]
            coche = crear_coche_desde_modelo(make_name, modelo)
            # Verificar duplicados
            if not any(c["marca"].lower() == coche["marca"].lower() and 
                       c["modelo"].lower() == coche["modelo"].lower() and 
                       c["año"] == coche["año"] for c in coches):
                nuevos_coches.append(coche)

    # Añadir nuevos coches
    coches.extend(nuevos_coches)

    # Guardar
    with open("coches.json", "w", encoding="utf-8") as f:
        json.dump(coches, f, indent=2, ensure_ascii=False)

    print(f"Añadidos {len(nuevos_coches)} nuevos coches.")

if __name__ == "__main__":
    main()