const fs = require("fs");

// Use native fetch if available (Node 18+) otherwise fall back to node-fetch
let fetchFn;
try {
  fetchFn = global.fetch || require('node-fetch');
} catch (err) {
  fetchFn = null;
}

if (!fetchFn) {
  console.error('Necesitas Node 18+ o instalar node-fetch: npm install node-fetch');
  process.exit(1);
}

const makes = [
  "bmw", "audi", "mercedes-benz", "toyota",
  "volkswagen", "ford", "tesla", "hyundai",
  "kia", "nissan", "peugeot", "renault"
];

const years = [2018, 2019, 2020, 2021, 2022, 2023];

let allCars = [];

function normalizarCombustible(fuelType = '') {
  const fuel = fuelType.toString().toLowerCase();
  if (fuel.includes('diesel')) return 'Diésel';
  if (fuel.includes('electric')) return 'Eléctrico';
  if (fuel.includes('hybrid')) return 'Híbrido';
  if (fuel.includes('gasoline') || fuel.includes('petrol')) return 'Gasolina';
  return fuelType;
}

function capitalizar(text) {
  return String(text || '')
    .replace(/\b\w/g, char => char.toUpperCase())
    .trim();
}

function mapCar(car) {
  return {
    marca: capitalizar(car.make),
    modelo: car.model || 'Desconocido',
    año: Number(car.year) || 0,
    cilindros: car.engine_cylinders ? Number(car.engine_cylinders) : null,
    potencia: car.horsepower ? Number(car.horsepower) : null,
    combustible: normalizarCombustible(car.fuel_type),
    traccion: car.drive || car.drivetrain || car.transmission || 'N/A',
    carroceria: car.body_type || car.type || 'Desconocido',
    imagen: `https://source.unsplash.com/featured/400x300?${encodeURIComponent(car.make || 'car')},${encodeURIComponent(car.model || '')}`,
    precio: car.price ? Number(car.price) : null,
    descripcion: car.description || `Coche ${capitalizar(car.make)} ${car.model || ''}`.trim(),
    categoria: null
  };
}

async function getCars() {
  for (let make of makes) {
    for (let year of years) {
      try {
        const url = `https://carapi.app/api/trims?make=${make}&year=${year}`;
        const res = await fetchFn(url);
        const data = await res.json();

        if (data && data.data) {
          const filtered = data.data.filter(car =>
            car.fuel_type &&
            (car.fuel_type.toLowerCase().includes("diesel") ||
             car.fuel_type.toLowerCase().includes("electric"))
          );

          allCars.push(...filtered);
          console.log(`✔ ${make} ${year} → ${filtered.length} coches válidos`);
        } else {
          console.log(`⚠ ${make} ${year} → respuesta sin datos válidos`);
        }
      } catch (err) {
        console.log(`❌ Error con ${make} ${year}: ${err.message}`);
      }
    }
  }

  const uniqueCars = Array.from(
    new Map(allCars.map(car => [car.id, car])).values()
  );

  const finalCars = uniqueCars.slice(0, 1000);
  fs.writeFileSync("cars.json", JSON.stringify(finalCars, null, 2));
  console.log(`🔥 Total coches guardados en cars.json: ${finalCars.length}`);

  mergeIntoCoches(finalCars.map(mapCar));
}

function mergeIntoCoches(newCars) {
  const cochesPath = 'coches.json';
  let existingCoches = [];

  try {
    existingCoches = JSON.parse(fs.readFileSync(cochesPath, 'utf-8'));
  } catch (err) {
    console.warn(`No se pudo leer ${cochesPath}. Se creará uno nuevo.`, err.message);
  }

  const existingKeys = new Set(
    existingCoches.map(c => `${c.marca}|${c.modelo}|${c.año}|${(c.combustible || '').toString().toLowerCase()}`)
  );

  const merged = [...existingCoches];
  let added = 0;

  newCars.forEach(car => {
    const key = `${car.marca}|${car.modelo}|${car.año}|${(car.combustible || '').toString().toLowerCase()}`;
    if (!existingKeys.has(key)) {
      merged.push(car);
      existingKeys.add(key);
      added += 1;
    }
  });

  fs.writeFileSync(cochesPath, JSON.stringify(merged, null, 2));
  console.log(`✨ ${added} coches añadidos a ${cochesPath}. Total ahora: ${merged.length}`);
}

getCars();
