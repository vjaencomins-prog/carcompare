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
3. Habilita Authentication con Google Provider
4. Habilita Firestore Database
5. Ve a Configuración del proyecto > Tus apps > Web app
6. Copia las claves de configuración
7. Pega las claves en `script.js` en la variable `firebaseConfig`

## Despliegue

La aplicación está configurada para desplegarse en Vercel con soporte para Firebase.

## Uso

- Regístrate/inicia sesión con Google
- Busca y filtra coches
- Añade a favoritos (♥)
- Añade al carrito de compras
- Compara hasta 3 coches
- Tus datos se guardan automáticamente en la nube
