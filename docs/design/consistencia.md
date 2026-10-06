# Revisión de consistencia entre diagramas — San Camilo en Línea

Se aplicó el Prompt IA 3 de la guía a los cinco diagramas: `clases.puml`, `secuencia-pedido-multipuesto.puml`, `estados-pedido-puesto.mmd`, `actividades-consolidar-pedido.puml` y `paquetes.puml`. Cada hallazgo de la IA fue verificado por el equipo contra los archivos.

## Reglas

- **C1** cada mensaje de secuencia es una operación de la clase receptora.
- **C2** cada transición de estados corresponde a una operación de la clase.
- **C3** las multiplicidades son coherentes con los criterios de aceptación.
- **C4** los paquetes no tienen ciclos.
- **C5** los nombres son consistentes entre diagramas.

## Hallazgos

| Regla | Elemento | Hallazgo de la IA | Verificación del equipo | Resultado |
|---|---|---|---|---|
| C1 | Secuencia, mensaje 7 | `Pedido -> Pedido : producto.reservar(cantidad)` no es una operación de Pedido. | Correcto. `reservar` es de Producto. Se agregó la línea de vida Producto y el mensaje pasó a `Pedido -> Producto : reservar(cantidad)`. Lo mismo para `liberar`. | Corregido |
| C2 | Estados, transición inicial | `[*] --> RECIBIDO : registrarPago()` usa una operación de Pedido y no de PedidoPuesto. | Correcto. Se agregó `recibir()` a PedidoPuesto; `Pedido.registrarPago()` la invoca al crear cada sub-pedido. | Corregido |
| C4 | Paquetes y puerto Notificador | `notificarPedidoRecibido(pedidoPuesto: PedidoPuesto)` obliga a notificaciones a conocer una clase de pedidos, mientras pedidos usa a notificaciones: hay un ciclo. | Correcto. Se creó el DTO `AvisoPedido` en el paquete compartido y el puerto ahora lo recibe. La decisión quedó en el ADR-004. | Corregido |
| C3 | Clases, Pedido–PedidoPuesto | La multiplicidad `0..*` contradice el criterio 1, que exige un sub-pedido por cada puesto, así que debería ser `1..*`. | **Falso positivo.** Antes del pago y cuando el pago es rechazado, que es el criterio 2, el pedido no tiene sub-pedidos. `0..*` es lo correcto. | Rechazado |
| C1 | Secuencia, mensaje 2 | `POST /pedidos/{id}/pago` no es una operación de ninguna clase del diagrama de clases. | Cierto, pero no se corrige: PWA y PedidoController son de la capa de presentación y el diagrama de clases solo cubre el dominio de Pedidos y Pagos. Se documenta el límite. | Documentado |
| C5 | Estados y clases | `rechazar()` aparece sin parámetro en el diagrama de estados y como `rechazar(motivo)` en clases. | Aceptable: en las transiciones se omiten los parámetros para que se lean bien. Los nombres coinciden. | Aceptado |
| C2 | Estados, resto de transiciones | `marcarListo`, `rechazar`, `registrarRecojo` y `confirmarEntrega` existen en PedidoPuesto. | Verificado contra `clases.puml`. | Sin hallazgo |
| C4 | Paquetes después del cambio | reparto → pedidos → catálogo, pagos, notificaciones → compartido. | Verificado: no hay camino de vuelta hacia pedidos. | Sin hallazgo |

## Qué habría pasado sin verificar

Si se aceptaba el hallazgo C3, la multiplicidad `1..*` habría obligado a crear sub-pedidos antes de cobrar. Con un pago rechazado quedarían sub-pedidos huérfanos y avisos enviados a comerciantes por pedidos que nunca se pagaron, lo que rompe el criterio 2.
