// Script para crear un nuevo proyecto Firebase
// Ejecuta estos comandos en orden:

console.log("🚀 Guía para crear un nuevo proyecto Firebase:");
console.log("");

console.log("1️⃣ Crear proyecto:");
console.log("   - Ve a https://console.firebase.google.com/");
console.log("   - Haz clic en 'Crear un proyecto'");
console.log("   - Nombre: 'carcompare' (o el que prefieras)");
console.log("   - Elige si quieres Google Analytics (recomendado: Sí)");
console.log("");

console.log("2️⃣ Habilitar Authentication:");
console.log("   - Ve a 'Authentication' en el menú lateral");
console.log("   - Haz clic en 'Comenzar'");
console.log("   - Ve a 'Sign-in method'");
console.log("   - Habilita 'Google' como proveedor");
console.log("   - Configura el nombre público de la app");
console.log("   - Añade dominios autorizados:");
console.log("     * carcompare-mu.vercel.app");
console.log("     * localhost");
console.log("");

console.log("3️⃣ Configurar Firestore:");
console.log("   - Ve a 'Firestore Database'");
console.log("   - Haz clic en 'Crear base de datos'");
console.log("   - Elige 'Modo de prueba' (para desarrollo)");
console.log("   - Selecciona ubicación (us-central o europe-west)");
console.log("");

console.log("4️⃣ Obtener configuración web:");
console.log("   - Ve a 'Configuración del proyecto' (icono de engranaje)");
console.log("   - Baja hasta 'Tus apps'");
console.log("   - Haz clic en el icono '</>' (Web app)");
console.log("   - Registra la app con nombre 'CarCompare Web'");
console.log("   - Copia el objeto firebaseConfig que aparece");
console.log("");

console.log("5️⃣ Reemplazar configuración:");
console.log("   - Abre script.js");
console.log("   - Reemplaza el objeto firebaseConfig con el nuevo");
console.log("   - Guarda y sube los cambios a GitHub");
console.log("");

console.log("6️⃣ Probar:");
console.log("   - Ve a carcompare-mu.vercel.app");
console.log("   - El botón 'Entrar con Google' debería funcionar");
console.log("");

console.log("🔧 Si aún no funciona:");
console.log("   - Ejecuta el contenido de firebase-debug.js en la consola");
console.log("   - Revisa los errores que aparecen");