# ADR-002: Construir el frontend como PWA en lugar de una app nativa

- Estado: Aceptado
- Fecha: 2026-09-29
- Decisores: Gustavo Alonso Yunque Quispe (developer único)

## Contexto
El atributo crítico del caso es la capacidad de interacción: un comerciante con poca experiencia digital debe publicar un producto en ≤ 3 toques desde un celular Android de gama baja con señal 3G (QA-01, R-06, RF-01). Los clientes y repartidores también usan el sistema desde el celular (RF-02, RF-03, RF-06). El plazo es de 1 mes (R-01) con un solo developer (R-02).

## Alternativas consideradas
1. **App nativa Android (Kotlin):** mejor acceso a la cámara y al hardware, pero exige publicarla en Play Store, que cada usuario la instale y, para iOS, una segunda app.
2. **PWA en React:** una sola base de código para todos los actores, se abre desde un enlace de WhatsApp y puede "instalarse" en la pantalla de inicio; funciona con conexión intermitente mediante un service worker.

## Decisión
Usaremos una **PWA en React (Vite)** con service worker. La pantalla de inicio del comerciante tendrá un botón grande "Publicar producto" que abre directamente la cámara (`<input type="file" accept="image/*" capture>`); la foto se comprime a WebP en el propio celular antes de subirla, y si no hay señal, la publicación queda en cola local y se envía al recuperar conexión.

## Consecuencias
- Positivas: una sola base de código para los tres actores, sin tienda de apps ni instalación obligatoria, actualizaciones inmediatas; cumple el flujo de 3 toques (1. Publicar → 2. Tomar foto → 3. Guardar, con nombre y precio escritos en la misma pantalla).
- Negativas / riesgos: menor control sobre notificaciones push en algunos navegadores (se compensa con WhatsApp, ADR-003); en celulares muy antiguos el service worker puede no estar disponible, por lo que la PWA debe funcionar también sin él (solo en línea).
