// Script de verificación de Firebase
// Ejecuta esto en la consola del navegador en carcompare-mu.vercel.app

console.log("🔍 Verificando Firebase...");

// Verificar si Firebase está cargado
if (typeof firebase !== 'undefined') {
    console.log("✅ Firebase SDK cargado");
    console.log("Versión:", firebase.SDK_VERSION);

    // Verificar configuración
    if (firebase.apps.length > 0) {
        console.log("✅ Firebase app inicializada");
        const app = firebase.apps[0];
        console.log("Config:", app.options);
    } else {
        console.log("❌ Firebase app NO inicializada");
    }

    // Verificar servicios
    if (firebase.auth) {
        console.log("✅ Firebase Auth disponible");
    }
    if (firebase.firestore) {
        console.log("✅ Firestore disponible");
    }
} else {
    console.log("❌ Firebase SDK NO cargado");
}

// Verificar si hay errores en la página
console.log("📋 Errores en consola (si los hay) se mostrarán arriba");