# CarCompare

Aplicación web para comparar y comprar coches con autenticación de usuario y base de datos Firebase.

## Características

- ✅ Búsqueda y filtrado de coches
- ✅ Comparador de hasta 3 coches
- ✅ Carrito de compras persistente
- ✅ Sistema de favoritos
- ✅ Autenticación con Google
- ✅ Datos guardados en Firebase Firestore

## Configuración de Firebase

1. Ve a [Firebase Console](https://console.firebase.google.com/)
2. Crea un nuevo proyecto
3. **Authentication:**
   - Ve a Authentication > Sign-in method
   - Habilita "Google" como proveedor
4. **Firestore Database:**
   - Ve a Firestore Database > Crear base de datos
   - Elige "Modo de prueba" para desarrollo
5. **Configuración web:**
   - Ve a Configuración del proyecto > Tus apps
   - Haz clic en "</>" para añadir app web
   - Copia el objeto `firebaseConfig`
6. **Actualizar script.js:**
   - Abre `script.js`
   - Reemplaza el objeto `firebaseConfig` con tus claves reales
   - O usa `firebase-config-example.js` como referencia

### Estructura de Firestore
- `usuarios/{userId}`: Datos del usuario (carrito, etc.)
- `favoritos/{userId}`: Lista de coches favoritos

## Despliegue

La aplicación está configurada para desplegarse en Vercel con soporte para Firebase.

## Uso

- Regístrate/inicia sesión con Google
- Busca y filtra coches
- Añade a favoritos (♥)
- Añade al carrito de compras
- Compara hasta 3 coches
- Tus datos se guardan automáticamente en la nube
