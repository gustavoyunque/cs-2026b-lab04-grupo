# ADR-004: Romper el ciclo pedidos–notificaciones con un DTO en el paquete compartido

- Estado: Aceptado
- Fecha: 2026-10-06
- Decisores: Gustavo Alonso Yunque Quispe y Giovani Angel Mendoza Contreras

## Contexto
En el diseño detallado del Lab 05, el puerto `Notificador` recibía un `PedidoPuesto` para avisar al comerciante (RF-05). Eso obliga al paquete notificaciones a conocer una clase de pedidos, y pedidos ya depende de notificaciones para usar el puerto. La revisión de consistencia detectó el ciclo (regla C4), que va contra el monolito modular del ADR-001 y complica extraer un módulo más adelante.

## Alternativas consideradas
1. **Dejar el ciclo:** no exige cambios, pero los dos módulos ya no se pueden probar ni desplegar por separado.
2. **Mover el puerto `Notificador` al paquete pedidos:** rompe el ciclo, pero notificaciones pasaría a depender de pedidos y cada módulo nuevo que quiera avisar repetiría el problema.
3. **Pasar un DTO `AvisoPedido` definido en el paquete compartido:** el puerto recibe solo celular, puesto y resumen.

## Decisión
Usaremos la alternativa 3. El puerto queda como `notificarPedidoRecibido(aviso: AvisoPedido)` y `AvisoPedido` vive en el paquete compartido. `ServicioPedidos` arma el aviso con los datos del sub-pedido antes de encolarlo.

## Consecuencias
- Positivas: no hay ciclos entre paquetes; notificaciones no conoce el dominio de pedidos y sirve para otros módulos; el mensaje que viaja por la cola pg-boss del ADR-003 es pequeño y estable.
- Negativas / riesgos: hay que mantener un DTO más y, si el aviso necesita un dato nuevo, se cambia el DTO en compartido, lo que afecta a todos los que lo usan.
