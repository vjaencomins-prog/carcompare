# CarCompare

Aplicación web para comparar y comprar coches con autenticación de usuario y base de datos Firebase.

## ⚠️ IMPORTANTE: Firebase Configuration Error

Si ves el error `Firebase: Error (auth/configuration-not-found)`, significa que el proyecto de Firebase actual no existe o está mal configurado.

### 🚀 Solución Rápida

**Ejecuta el contenido de `setup-firebase.js` en la consola del navegador** para ver la guía completa paso a paso.

### Pasos para arreglar:

1. **Crear nuevo proyecto Firebase:**
   - Ve a https://console.firebase.google.com/
   - Crea proyecto llamado "carcompare" (o similar)

2. **Habilitar servicios:**
   - **Authentication:** Habilita Google Sign-in
   - **Firestore:** Crea base de datos en modo prueba
   - **Analytics:** Opcional pero recomendado

3. **Configurar dominios:**
   - En Authentication > Configuración > Dominios autorizados
   - Añade: `carcompare-mu.vercel.app` y `localhost`

4. **Obtener nuevas claves:**
   - Configuración del proyecto > Tus apps > Web app
   - Copia el `firebaseConfig` y reemplaza en `script.js`

5. **Probar:**
   - Sube cambios a GitHub
   - Ve a carcompare-mu.vercel.app
   - El login debería funcionar

### 🔧 Troubleshooting

Si aún no funciona, ejecuta `firebase-debug.js` en la consola del navegador para diagnóstico detallado.

#### Error "Can't find variable: auth"
- **Causa**: Firebase no se inicializó correctamente
- **Solución**: La app ahora maneja esto automáticamente mostrando "Login (No disponible)"
- **Para arreglar completamente**: Configura un nuevo proyecto Firebase siguiendo `setup-firebase.js`

#### Probar la aplicación
Ejecuta `test-app.js` en la consola para verificar que todos los componentes funcionan correctamente.

## Configuración de Firebase

1. Ve a [Firebase Console](https://console.firebase.google.com/)
2. Crea un nuevo proyecto
3. **Authentication:**
   - Ve a Authentication > Sign-in method
   - Habilita "Google" como proveedor
4. **Firestore Database:**
   - Ve a Firestore Database > Crear base de datos
   - Elige "Modo de prueba" para desarrollo
5. **Dominios autorizados:**
   - Ve a Authentication > Configuración
   - En "Dominios autorizados", añade:
     - `carcompare-mu.vercel.app`
     - `localhost` (para desarrollo local)
     - Cualquier otro dominio donde uses la app

6. **Actualizar script.js:**
   - Las claves ya están configuradas correctamente

### Estructura de Firestore
- `usuarios/{userId}`: Datos del usuario (carrito, etc.)
- `favoritos/{userId}`: Lista de coches favoritos

## 🔧 Troubleshooting

### Login con Google no funciona
1. **Revisa la consola del navegador** (F12 > Console) para ver errores
2. **Verifica dominios autorizados** en Firebase Console
3. **Ejecuta el script de debug**: Copia el contenido de `firebase-debug.js` en la consola
4. **Comprueba que las claves** en `script.js` sean correctas

### Botón de favoritos
- Ahora es más pequeño (30x30px) y no solapa la imagen
- Solo funciona si estás logueado con Google

## Despliegue

La aplicación está configurada para desplegarse en Vercel con soporte para Firebase.

## Uso

- Regístrate/inicia sesión con Google
- Busca y filtra coches
- Añade a favoritos (♥)
- Añade al carrito de compras
- Compara hasta 3 coches
- Tus datos se guardan automáticamente en la nube
