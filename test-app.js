// Script de prueba rápida para verificar que Firebase funciona
// Ejecuta esto en la consola de carcompare-mu.vercel.app

console.log("🧪 Probando CarCompare...");

// Verificar que la app carga
if (document.readyState === 'complete') {
    console.log("✅ Página cargada completamente");
} else {
    console.log("⚠️ Página aún cargando...");
}

// Verificar elementos principales
const elements = [
    'auth-ui',
    'busqueda',
    'lista-coches',
    'cart-section'
];

elements.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
        console.log(`✅ Elemento ${id} encontrado`);
    } else {
        console.log(`❌ Elemento ${id} NO encontrado`);
    }
});

// Verificar Firebase
if (typeof firebase !== 'undefined') {
    console.log("✅ Firebase SDK cargado");
    console.log("📊 Número de apps inicializadas:", firebase.apps.length);
} else {
    console.log("❌ Firebase SDK NO cargado");
}

// Verificar funciones principales
const functions = [
    'login',
    'logout',
    'cargarDatos',
    'comprarCoche',
    'toggleFav'
];

functions.forEach(func => {
    if (typeof window[func] === 'function') {
        console.log(`✅ Función ${func} disponible`);
    } else {
        console.log(`❌ Función ${func} NO disponible`);
    }
});

console.log("🎉 Prueba completada. Revisa los resultados arriba.");