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

// Verificar configuración específica
console.log("🔧 Configuración actual:");
try {
    const config = {
        apiKey: "AIzaSyD43VnRxL2pMGxt676rw9TFQVB7JCIHPmQ",
        authDomain: "carcompare-b9451.firebaseapp.com",
        projectId: "carcompare-b9451"
    };
    console.log("API Key:", config.apiKey ? "Presente" : "Faltante");
    console.log("Auth Domain:", config.authDomain);
    console.log("Project ID:", config.projectId);
} catch (e) {
    console.error("Error al verificar config:", e);
}

// Probar conexión con Firebase
console.log("🌐 Probando conexión...");
fetch('https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSyD43VnRxL2pMGxt676rw9TFQVB7JCIHPmQ', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ returnSecureToken: false })
})
.then(response => response.json())
.then(data => {
    if (data.error) {
        console.error("❌ Error de Firebase:", data.error.message);
        if (data.error.message.includes('CONFIGURATION_NOT_FOUND')) {
            console.error("🔧 SOLUCIÓN: El proyecto de Firebase no existe o las claves son incorrectas");
            console.log("📝 Pasos para arreglar:");
            console.log("1. Ve a https://console.firebase.google.com/");
            console.log("2. Crea un nuevo proyecto o verifica que 'carcompare-b9451' existe");
            console.log("3. Ve a Configuración del proyecto > General > Tus apps");
            console.log("4. Copia la configuración web y reemplaza en script.js");
        }
    } else {
        console.log("✅ Conexión exitosa con Firebase");
    }
})
.catch(error => {
    console.error("❌ Error de conexión:", error);
});

console.log("📋 Errores en consola (si los hay) se mostrarán arriba");