# ADR-001: Adoptar un monolito modular para el MVP de San Camilo en Línea

- Estado: Aceptado
- Fecha: 2026-09-29
- Decisores: Gustavo Alonso Yunque Quispe (developer único)

## Contexto
El MVP debe estar en producción en 1 mes (R-01) y lo construye y opera una sola persona (R-02) con un VPS de bajo costo (R-03). La carga esperada es moderada: 150 clientes simultáneos en la hora pico del sábado (QA-03). Al mismo tiempo, un pedido pagado no puede perderse si falla WhatsApp (QA-02) y se prevé agregar Plin y otros mercados, por lo que importa la modificabilidad.

## Alternativas consideradas
1. **Monolito en capas (4,05):** el más rápido de construir, pero la lógica de pagos y notificaciones queda mezclada en la capa de servicios.
2. **Microservicios (2,70):** muy modificable y escalable, pero con 5 despliegues, 5 bases de datos y un broker excede lo que una persona puede operar en 1 mes.
3. **Monolito modular (4,20):** elegido. Detalle en [matriz-decision.md](../matriz-decision.md).

## Decisión
Usaremos un **monolito modular en Node.js (Express)** con 5 módulos: Catálogo, Pedidos, Pagos, Notificaciones y Reparto. Los módulos se comunican solo mediante sus interfaces públicas (servicios de aplicación), cada uno tiene su propio esquema en PostgreSQL y las integraciones externas (Culqi y WhatsApp) se implementan como adaptadores. El frontend es una PWA en React servida por el mismo servidor.

## Consecuencias
- Positivas: un solo despliegue y un solo servidor, bajo costo, entrega rápida; una falla de WhatsApp queda aislada en el módulo Notificaciones; si la carga crece, un módulo (por ejemplo, Pedidos) puede extraerse como servicio independiente.
- Negativas / riesgos: hay que respetar los límites entre módulos (se validará con `dependency-cruiser` en la integración continua); una falla grave del proceso Node.js detiene todo el sistema, por lo que se usará PM2 con reinicio automático y copias de seguridad diarias de la base de datos.
