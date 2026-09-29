# Drivers arquitectónicos — San Camilo en Línea

Caso N.º 7 de la guía: pedidos a los puestos del Mercado San Camilo (Arequipa), con recojo o delivery.
Actores: **cliente**, **comerciante** y **repartidor**.

## 1. Requisitos funcionales clave
| ID    | Requisito                                                                                   | Actor        | Prioridad |
|-------|---------------------------------------------------------------------------------------------|--------------|-----------|
| RF-01 | El comerciante publica un producto (foto, nombre, precio, stock) desde su celular           | Comerciante  | Alta      |
| RF-02 | El cliente navega el catálogo por puesto y por categoría (frutas, carnes, abarrotes, etc.)  | Cliente      | Alta      |
| RF-03 | El cliente arma un solo pedido con productos de varios puestos y elige recojo o delivery    | Cliente      | Alta      |
| RF-04 | El cliente paga el pedido con Yape                                                          | Cliente      | Alta      |
| RF-05 | El comerciante recibe la confirmación del pedido por WhatsApp                               | Comerciante  | Alta      |
| RF-06 | El repartidor ve los pedidos asignados, recoge en cada puesto y marca "entregado"           | Repartidor   | Media     |
| RF-07 | El comerciante marca un producto como agotado con un solo toque                             | Comerciante  | Media     |

## 2. Atributos de calidad (ordenados por prioridad)
1. **Capacidad de interacción (usabilidad)** — atributo crítico del caso: muchos comerciantes tienen poca experiencia digital y celulares de gama baja; si publicar es difícil, el catálogo queda vacío y la plataforma no sirve.
2. **Disponibilidad** — un pedido pagado no se puede perder aunque falle WhatsApp o la pasarela responda lento.
3. **Rendimiento** — el catálogo debe cargar rápido con datos móviles 3G/4G en el mercado, donde la señal es irregular.
4. **Modificabilidad** — se prevé agregar Plin, nuevos mercados de Arequipa y cupones sin reescribir el sistema.
5. **Seguridad** — se manejan pagos y teléfonos de clientes (datos personales).

## 3. Restricciones
| ID   | Tipo        | Restricción                                                                                          |
|------|-------------|------------------------------------------------------------------------------------------------------|
| R-01 | Plazo       | MVP en producción en 1 mes                                                                           |
| R-02 | Equipo      | 1 developer (trabajo individual) con experiencia en JavaScript/React, Node.js, Python, Java y SQL    |
| R-03 | Presupuesto | Bajo: un VPS de ~US$ 6/mes; los únicos pagos variables son la comisión de la pasarela y WhatsApp     |
| R-04 | Normativa   | Ley N.º 29733 de Protección de Datos Personales (teléfonos y direcciones de clientes)                |
| R-05 | Tecnología  | Pago con Yape solo mediante pasarela autorizada (Culqi); notificaciones vía WhatsApp Business Cloud API |
| R-06 | Dispositivo | Comerciantes con celulares Android de gama baja (2 GB de RAM) y señal 3G dentro del mercado           |

## 4. Escenarios de atributos de calidad
| ID    | Atributo                    | Fuente                           | Estímulo                                        | Entorno                                          | Artefacto                     | Respuesta                                                                      | Medida                                              |
|-------|-----------------------------|----------------------------------|-------------------------------------------------|--------------------------------------------------|-------------------------------|--------------------------------------------------------------------------------|-----------------------------------------------------|
| QA-01 | Capacidad de interacción    | Comerciante con poca experiencia digital | Quiere publicar un producto nuevo          | Celular Android de gama baja, señal 3G, operación normal | PWA — módulo Catálogo    | Toma la foto, escribe nombre y precio y publica; la foto se comprime en el celular | ≤ 3 toques desde la pantalla de inicio y ≤ 60 s en total |
| QA-02 | Disponibilidad              | WhatsApp Business Cloud API      | No responde al enviar la confirmación del pedido | Operación normal, sábado 9–11 a. m.              | Módulo Notificaciones         | El pedido queda registrado como pagado y el mensaje se reintenta desde una cola  | 0 pedidos perdidos; reintento exitoso en ≤ 10 min  |
| QA-03 | Rendimiento                 | 150 clientes simultáneos         | Abren el catálogo de un puesto                  | Hora pico del sábado (9–11 a. m.), red 4G         | API del módulo Catálogo       | Devuelve la lista paginada de productos con miniaturas en WebP                   | p95 ≤ 2 s                                           |
