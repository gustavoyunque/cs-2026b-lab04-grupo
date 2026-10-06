# Historia de usuario crítica — San Camilo en Línea

**HU-03: Pedido a varios puestos con pago único**

Como cliente, quiero armar un solo pedido con productos de varios puestos del mercado y pagarlo una sola vez con Yape, para no pagar puesto por puesto ni manejar efectivo.

Se relaciona con los requisitos RF-03, RF-04 y RF-05 y con el escenario QA-02 de `docs/architecture/drivers.md`.

## Criterios de aceptación

1. **Pago aprobado.** Dado un pedido en BORRADOR con productos disponibles de dos o más puestos, cuando lo confirmo y el pago con Yape es aprobado, entonces el pedido queda PAGADO, se crea un sub-pedido RECIBIDO por cada puesto y cada comerciante recibe un aviso por WhatsApp.
2. **Pago rechazado.** Dado un pedido confirmado, cuando el pago con Yape es rechazado, entonces el pedido queda CANCELADO, no se crea ningún sub-pedido y el stock reservado se libera.
3. **Puesto que rechaza su parte.** Dado un pedido pagado, cuando un comerciante rechaza su sub-pedido porque un producto se agotó o no responde en 15 minutos, entonces ese sub-pedido queda RECHAZADO, se reembolsa al cliente solo el subtotal de ese puesto y los demás puestos siguen con su parte.

## Alcance del diseño

Se diseña el interior de los módulos **Pedidos** y **Pagos** del monolito modular del ADR-001. Catálogo, Notificaciones y Reparto solo aparecen por las clases o puertos que Pedidos necesita de ellos.
