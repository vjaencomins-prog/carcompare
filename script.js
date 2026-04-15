let coches = [];
let comparados = [];
let resultadosActuales = [];
let vpicMakes = [];
let modoBusqueda = false; // false = modo sugerencias, true = modo búsqueda
const VPIC_API = 'https://vpic.nhtsa.dot.gov/api/vehicles';

function normalizarTexto(texto) {
    return String(texto)
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .replace(/\s+/g, ' ')
        .trim();
}

async function cargarDatos() {
    await cargarCochesLocales();
    await cargarMarcasVpic();
    mostrarSugerencias();
}

async function cargarMarcasVpic() {
    try {
        const response = await fetch(`${VPIC_API}/getallmakes?format=json`);
        const data = await response.json();
        vpicMakes = data.Results
            .map(item => item.Make_Name)
            .filter(Boolean)
            .sort((a, b) => normalizarTexto(a).localeCompare(normalizarTexto(b)));
    } catch (error) {
        console.warn('No se pudieron cargar marcas desde vPIC:', error);
    }
}

async function cargarCochesLocales() {
    try {
        const res = await fetch('./coches.json');
        coches = await res.json();
    } catch (err) {
        console.error('Error cargando coches.json:', err);
        coches = [];
    }
}

function crearCocheVpic({ marca, modelo = '', año = '', km = null, combustible = null, source = 'vpic' }) {
    return {
        marca,
        modelo,
        año,
        km,
        combustible,
        precio: null,
        source,
        imagen: `https://picsum.photos/id/${Math.floor(Math.random() * 1000) + 100}/400/250`
    };
}

function escapeHtmlAttribute(value) {
    return String(value || '')
        .replace(/&/g, '&amp;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
}

function construirImgCarImages(coche, clase, ancho = 400, alto = 250) {
    const marca = escapeHtmlAttribute(coche.marca || '');
    const modelo = escapeHtmlAttribute(coche.modelo || '');
    const año = escapeHtmlAttribute(coche.año || '');
    const altText = escapeHtmlAttribute(`${coche.marca || 'Coche'} ${coche.modelo || ''}`.trim());
    const srcFallback = escapeHtmlAttribute(coche.imagen || `https://via.placeholder.com/${ancho}x${alto}/cccccc/666666?text=Buscando+imagen`);

    return `<img src="${srcFallback}" alt="${altText}" class="${clase}" onerror="this.src='https://via.placeholder.com/${ancho}x${alto}/cccccc/666666?text=No+Image'" data-ci-make="${marca}" data-ci-model="${modelo}" data-ci-year="${año}" data-ci-width="${ancho}" data-ci-height="${alto}" data-ci-format="webp">`;
}

function obtenerSugerencias() {
    // Seleccionar hasta 3 coches populares de diferentes categorías
    const sugerencias = [];

    const sedan = coches.find(c => normalizarTexto(c.carroceria) === 'sedan' && c.año >= 2023);
    if (sedan) sugerencias.push({...sedan, destacado: 'Más Vendido'});

    const suv = coches.find(c => normalizarTexto(c.carroceria) === 'suv' && c.año >= 2023);
    if (suv) sugerencias.push({...suv, destacado: 'Familiar Favorito'});

    const electrico = coches.find(c => normalizarTexto(c.combustible) === 'electrico');
    if (electrico) sugerencias.push({...electrico, destacado: 'Ecológico'});

    // Si no hay suficientes sugerencias por categoría, completar con los primeros coches disponibles
    if (sugerencias.length < 3) {
        coches.some(coche => {
            if (sugerencias.length >= 3) return true;
            if (sugerencias.some(s => s.marca === coche.marca && s.modelo === coche.modelo)) return false;
            sugerencias.push({...coche, destacado: sugerencias.length === 0 ? 'Recomendado' : sugerencias.length === 1 ? 'Seleccionado' : 'Ideal'});
            return false;
        });
    }

    return sugerencias.slice(0, 3);
}

function mostrarSugerencias() {
    const sugerencias = obtenerSugerencias();
    const contenedor = document.getElementById('sugerencias');
    contenedor.innerHTML = '';

    if (!sugerencias.length) {
        contenedor.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: #999; font-size: 1.1em;">No hay sugerencias disponibles por el momento. Intenta cargar la página de nuevo.</div>';
        return;
    }

    sugerencias.forEach((coche, index) => {
        const modelo = coche.modelo || 'Modelo no disponible';
        const año = coche.año || 'No disponible';
        const cilindros = coche.cilindros || 'N/A';
        const potencia = coche.potencia ? `${coche.potencia} HP` : 'N/A';
        const combustible = coche.combustible || 'N/A';
        const traccion = coche.traccion || 'N/A';
        const carroceria = coche.carroceria || 'N/A';
        const precio = coche.precio ? `$${coche.precio.toLocaleString()}` : 'Precio no disponible';
        const imagenHTML = construirImgCarImages(coche, 'sugerencia-imagen', 400, 250);

        const div = document.createElement('div');
        div.classList.add('sugerencia-coche');

        div.innerHTML = `
            ${imagenHTML}
            <h3>${coche.marca} ${modelo}</h3>
            <span class="destacado">${coche.destacado}</span>
            <p><strong>⚙️ Motor:</strong> ${cilindros} cilindros</p>
            <p><strong>💨 Potencia:</strong> ${potencia}</p>
            <p><strong>⛽ Combustible:</strong> ${combustible}</p>
            <p><strong>💰 Precio:</strong> ${precio}</p>
            <p><strong>📅</strong> ${año}</p>
            <button onclick="añadirComparadorDesdeSugerencia(${index})">Seleccionar</button>
        `;

        contenedor.appendChild(div);
    });
}

function añadirComparadorDesdeSugerencia(index) {
    const sugerencias = obtenerSugerencias();
    añadirComparadorDesdeLista(sugerencias, index);
}

function añadirComparadorDesdeLista(lista, index) {
    if (comparados.length >= 3) {
        alert('Solo puedes comparar 3 coches máximo');
        return;
    }

    const coche = lista[index];
    if (comparados.some(c => c.marca === coche.marca && c.modelo === coche.modelo)) {
        alert('Este coche ya está en el comparador');
        return;
    }

    comparados.push(coche);
    mostrarComparador();
}

function filtrarPorOpciones(lista) {
    const combustible = normalizarTexto(document.getElementById('filtro-combustible').value);
    const año = document.getElementById('filtro-año').value;

    return lista.filter(coche => {
        // Filtrar por combustible solo si existe en el coche
        if (combustible && coche.combustible) {
            if (!normalizarTexto(coche.combustible).includes(combustible)) {
                return false;
            }
        }

        // Filtrar por año
        if (año) {
            if (año === '2018') {
                if (coche.año > 2018) return false;
            } else {
                if (coche.año.toString() !== año) return false;
            }
        }

        return true;
    });
}

function mostrarCoches(lista) {
    resultadosActuales = lista;
    const contenedor = document.getElementById('lista-coches');
    contenedor.innerHTML = '';

    if (lista.length === 0) {
        contenedor.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 40px;"><p style="font-size: 1.2em; color: #999;">🔍 No se han encontrado coches.</p></div>';
        return;
    }

    lista.forEach((coche, index) => {
        const modelo = coche.modelo || 'Modelo no disponible';
        const año = coche.año || 'No disponible';
        const cilindros = coche.cilindros || 'N/A';
        const potencia = coche.potencia ? `${coche.potencia} HP` : 'N/A';
        const combustible = coche.combustible || 'N/A';
        const traccion = coche.traccion || 'N/A';
        const carroceria = coche.carroceria || 'N/A';
        const precio = coche.precio ? `$${coche.precio.toLocaleString()}` : 'Precio no disponible';
        const imagenHTML = construirImgCarImages(coche, 'coche-imagen', 400, 250);
        const source = coche.source ? `<small>Fuente: ${coche.source}</small>` : '';

        const div = document.createElement('div');
        div.classList.add('coche');

        div.innerHTML = `
            ${imagenHTML}
            <h3>${coche.marca} ${modelo}</h3>
            <p><strong>⚙️ Motor:</strong> ${cilindros} cilindros</p>
            <p><strong>💨 Potencia:</strong> ${potencia}</p>
            <p><strong>⛽ Combustible:</strong> ${combustible}</p>
            <p><strong>🔄 Tracción:</strong> ${traccion}</p>
            <p><strong>📦 Carrocería:</strong> ${carroceria}</p>
            <p><strong>💰 Precio:</strong> ${precio}</p>
            <p><strong>📅</strong> ${año}</p>
            ${source}
            <button onclick="añadirComparador(${index})">Comparar</button>
        `;

        contenedor.appendChild(div);
    });
}

function añadirComparador(index) {
    if (comparados.length >= 3) {
        alert('Solo puedes comparar 3 coches máximo');
        return;
    }

    const coche = resultadosActuales[index];
    if (comparados.some(c => c.marca === coche.marca && c.modelo === coche.modelo)) {
        alert('Este coche ya está en el comparador');
        return;
    }

    comparados.push(coche);
    mostrarComparador();
}

function mostrarComparador() {
    const comp = document.getElementById('comparador');
    comp.innerHTML = '';

    if (comparados.length === 0) {
        comp.innerHTML = '<p style="grid-column: 1/-1; text-align: center; padding: 20px; color: #999;">Selecciona coches para compararlos aquí.</p>';
        return;
    }

    comparados.forEach((coche, idx) => {
        const año = coche.año || 'No disponible';
        const cilindros = coche.cilindros || 'N/A';
        const potencia = coche.potencia ? `${coche.potencia} HP` : 'N/A';
        const combustible = coche.combustible || 'N/A';
        const traccion = coche.traccion || 'N/A';
        const carroceria = coche.carroceria || 'N/A';
        const precio = coche.precio ? `$${coche.precio.toLocaleString()}` : 'Precio no disponible';
        const imagenHTML = construirImgCarImages(coche, 'comparador-imagen', 200, 150);

        comp.innerHTML += `
            <div>
                ${imagenHTML}
                <h4>${coche.marca} ${coche.modelo || ''}</h4>
                <p><strong>📅 Año:</strong> ${año}</p>
                <p><strong>⚙️ Motor:</strong> ${cilindros} cilindros</p>
                <p><strong>💨 Potencia:</strong> ${potencia}</p>
                <p><strong>⛽ Combustible:</strong> ${combustible}</p>
                <p><strong>🔄 Tracción:</strong> ${traccion}</p>
                <p><strong>📦 Carrocería:</strong> ${carroceria}</p>
                <p><strong>💰 Precio:</strong> ${precio}</p>
                <button onclick="eliminarComparador(${idx})" style="background: #e74c3c; color: white; padding: 8px; border: none; border-radius: 5px; cursor: pointer; margin-top: 10px; width: 100%;">Eliminar</button>
                <hr>
            </div>
        `;
    });
}

function eliminarComparador(index) {
    comparados.splice(index, 1);
    mostrarComparador();
}

async function obtenerModelosPorMarcaYAnio(marca, año) {
    try {
        const response = await fetch(`${VPIC_API}/getmodelsformakeyear/make/${encodeURIComponent(marca)}/modelyear/${año}?format=json`);
        const data = await response.json();
        return data.Results.map(item => crearCocheVpic({
            marca,
            modelo: item.Model_Name,
            año,
            source: `vPIC (${marca} ${año})`
        }));
    } catch (error) {
        console.warn('Error al obtener modelos por marca y año:', error);
        return [crearCocheVpic({ marca, año, source: `vPIC (${marca} ${año})` })];
    }
}

async function buscarEnVPIC(texto) {
    if (!texto || !vpicMakes.length) {
        return [];
    }

    const añoMatch = texto.match(/\b(19|20)\d{2}\b/);
    if (añoMatch) {
        const año = añoMatch[0];
        const makeTexto = texto.replace(año, '').trim();
        const makeEncontrado = vpicMakes.find(make => normalizarTexto(make).includes(normalizarTexto(makeTexto)));
        if (makeEncontrado) {
            return await obtenerModelosPorMarcaYAnio(makeEncontrado, año);
        }
    }

    const coincidencias = vpicMakes
        .filter(make => normalizarTexto(make).includes(texto))
        .slice(0, 30);

    return coincidencias.map(make => crearCocheVpic({ marca: make, source: 'vPIC' }));
}

async function buscarCoches(texto) {
    const textoNormalizado = normalizarTexto(texto);
    const local = coches.filter(coche => {
        const datos = `${coche.marca} ${coche.modelo} ${coche.combustible} ${coche.año}`;
        return normalizarTexto(datos).includes(textoNormalizado);
    });
    const vpic = await buscarEnVPIC(textoNormalizado);
    const todos = [...local, ...vpic];
    const filtrados = filtrarPorOpciones(todos);
    return filtrados;
}

function toggleModoBusqueda() {
    modoBusqueda = !modoBusqueda;
    const searchSection = document.getElementById('search-section');
    const resultsSection = document.getElementById('results-section');
    const heroSection = document.querySelector('.hero-section');
    const verTodosBtn = document.getElementById('ver-todos');

    if (modoBusqueda) {
        // Mostrar modo búsqueda
        heroSection.style.display = 'none';
        searchSection.style.display = 'block';
        resultsSection.style.display = 'block';
        verTodosBtn.textContent = 'Volver a Sugerencias';
        mostrarCoches(filtrarPorOpciones(coches));
    } else {
        // Mostrar modo sugerencias
        heroSection.style.display = 'block';
        searchSection.style.display = 'none';
        resultsSection.style.display = 'none';
        verTodosBtn.textContent = 'Ver Todos los Vehículos';
        mostrarSugerencias();
    }
}

cargarDatos();

// Event listeners

document.getElementById('ver-todos').addEventListener('click', toggleModoBusqueda);

document.getElementById('busqueda').addEventListener('input', async (e) => {
    const texto = e.target.value;
    if (!texto.trim()) {
        const filtrados = filtrarPorOpciones(coches);
        mostrarCoches(filtrados);
        return;
    }

    const resultados = await buscarCoches(texto);
    mostrarCoches(resultados);
});

['filtro-combustible', 'filtro-año'].forEach(id => {
    document.getElementById(id).addEventListener('change', async () => {
        const texto = document.getElementById('busqueda').value;
        if (!texto.trim()) {
            const filtrados = filtrarPorOpciones(coches);
            mostrarCoches(filtrados);
        } else {
            const resultados = await buscarCoches(texto);
            mostrarCoches(resultados);
        }
    });
});

document.getElementById('limpiar-comparador').addEventListener('click', () => {
    comparados = [];
    mostrarComparador();
});
