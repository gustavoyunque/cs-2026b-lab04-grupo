# ADR-003: Integrar pagos y notificaciones mediante adaptadores y una cola de reintentos

- Estado: Aceptado
- Fecha: 2026-09-29
- Decisores: Gustavo Alonso Yunque Quispe (developer único)

## Contexto
El cliente paga con Yape (RF-04) y el comerciante recibe la confirmación por WhatsApp (RF-05). Yape solo puede cobrarse en línea a través de una pasarela autorizada (R-05); se verificó que Culqi documenta el cargo con token de Yape. Un pedido pagado no puede perderse aunque WhatsApp no responda (QA-02). Además, se prevé agregar Plin más adelante (modificabilidad) y el presupuesto es bajo (R-03).

## Alternativas consideradas
1. **Llamadas directas y síncronas** a Culqi y WhatsApp dentro del flujo del pedido: simple, pero si WhatsApp falla, el pedido falla.
2. **Puertos y adaptadores + cola Redis/BullMQ:** desacopla y reintenta, pero agrega un servicio más (Redis) para operar.
3. **Puertos y adaptadores + cola pg-boss sobre PostgreSQL:** desacopla y reintenta usando la base de datos que ya existe.

## Decisión
Definiremos dos puertos: `PasarelaPago` (implementado por `CulqiYapeAdapter`) y `Notificador` (implementado por `WhatsAppCloudAdapter`). El pedido se guarda como **pagado** apenas Culqi confirma el cargo; el aviso al comerciante se encola en **pg-boss** y se reintenta con espera exponencial hasta 10 minutos. Los mensajes de WhatsApp iniciados por la empresa se enviarán con **plantillas aprobadas** por Meta.

## Consecuencias
- Positivas: una caída de WhatsApp no bloquea ni pierde pedidos (QA-02); agregar Plin significa crear un nuevo adaptador de `PasarelaPago` sin tocar Pedidos; no se agrega Redis, lo que mantiene un solo servidor de datos.
- Negativas / riesgos: Culqi cobra comisión por transacción y requiere afiliación del comercio; las plantillas de WhatsApp deben aprobarse antes del lanzamiento y cada conversación iniciada por la empresa tiene costo; pg-boss agrega carga a PostgreSQL (aceptable con el volumen esperado).
