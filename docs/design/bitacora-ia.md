# Bitácora de uso de IA — Lab 05, San Camilo en Línea

| # | Fecha | Herramienta | Prompt | Qué propuso la IA | Qué verificamos o corregimos | Decisión |
|---|-------|-------------|--------|-------------------|------------------------------|----------|
| 1 | 06/10 | Claude | Prompt IA 1 adaptado: diagrama de clases de la HU-03 con el ADR-001 | Pedido compuesto por PedidoPuesto y este por LineaPedido desde el estado BORRADOR | Los sub-pedidos solo existen después del pago. Se cambió a Pedido compuesto por LineaPedido, y PedidoPuesto agrupa las líneas por agregación con multiplicidad 0..* | Corregida |
| 2 | 06/10 | Claude | Diagrama de secuencia de "pedido a varios puestos con pago único" | Ocho líneas de vida, `alt` de pago aprobado o rechazado, `loop` por línea y aviso asíncrono | El mensaje `producto.reservar()` iba de Pedido a sí mismo y no cumplía C1. Se agregó la línea de vida Producto | Corregida |
| 3 | 06/10 | Claude | Máquina de estados de PedidoPuesto en Mermaid | Cinco estados con guardas y dos estados finales | La transición inicial usaba `registrarPago()`, que es de Pedido. Se agregó `recibir()` a PedidoPuesto para cumplir C2 | Corregida |
| 4 | 06/10 | Claude | Diagramas de actividades y de paquetes | Cuatro particiones, tres decisiones y un fork; seis paquetes iguales a los módulos del ADR-001 | Los paquetes coinciden con el ADR-001. Las actividades se revisaron contra el criterio 3 de la historia | Aceptada |
| 5 | 06/10 | Claude | Prompt IA 2: esqueleto en Python del diagrama de clases | `src/pedidos/dominio.py` con dataclasses, ABC y enumeraciones | Se probó con adaptadores falsos y se comparó con pyreverse. `rechazar_pedido_puesto` necesitaba el id del pedido y se corrigió el diagrama | Corregida |
| 6 | 06/10 | Claude | Prompt IA 3: auditor de consistencia C1 a C5 | Ocho revisiones con tres problemas reales y una multiplicidad observada | Se aceptaron C1, C2 y C4. Se rechazó C3 por falso positivo. El ciclo de C4 se resolvió con el ADR-004 | Corregida |

Nunca se incluyeron datos personales ni información confidencial en los prompts.

## Anexo: prompts

### Prompt IA 1 — Diagrama de clases
```text
Actúa como diseñador de software orientado a objetos. Contexto: módulos Pedidos y Pagos de un
monolito modular (ADR-001: puertos y adaptadores para integraciones externas, ADR-003: pagos con
Culqi y avisos por WhatsApp con cola de reintentos). Historia y criterios: [historia.md].
Tarea: genera un diagrama de clases en PlantUML con atributos tipados, operaciones, multiplicidades,
una enumeración para el estado del sub-pedido de cada puesto y una interfaz para la pasarela de pagos.
Formato: solo el código PlantUML. No agregues clases que no se deriven de la historia; si asumes
algo, indícalo.
```

### Prompt 2 — Diagrama de secuencia
```text
Con este diagrama de clases [clases.puml], genera en PlantUML el diagrama de secuencia del escenario
"pedido a varios puestos con pago único": actor, PWA, controlador, servicio, repositorio, entidades y
puertos. Incluye un fragmento alt para pago aprobado y rechazado, un loop, un mensaje asíncrono para
el aviso al comerciante y los mensajes de retorno. Usa solo operaciones que existan en las clases.
```

### Prompt 3 — Máquina de estados
```text
Genera en Mermaid stateDiagram-v2 la máquina de estados de PedidoPuesto con los estados RECIBIDO,
LISTO, RECOGIDO, ENTREGADO y RECHAZADO. Incluye estado inicial, estados finales y guardas entre
corchetes. Nombra cada transición con la operación de la clase que la provoca.
```

### Prompt 4 — Actividades y paquetes
```text
Genera en PlantUML: a) el diagrama de actividades "preparación y consolidación de un pedido
multipuesto" con particiones Sistema, Comerciante, Repartidor y Cliente, al menos dos decisiones y un
fork; b) el diagrama de paquetes con un paquete por módulo del ADR-001 más uno compartido,
dependencias etiquetadas y una nota con la regla de dependencias.
```

### Prompt IA 2 — Ingeniería directa
```text
Genera el esqueleto en Python 3.10 con dataclasses y type hints del siguiente diagrama de clases.
Respeta exactamente los nombres de clases, atributos y operaciones en snake_case, las enumeraciones,
las interfaces como clases abstractas ABC y las multiplicidades. Implementa solo la lógica mínima de
Pedido y PedidoPuesto; los adaptadores deben lanzar NotImplementedError. [clases.puml]
```

### Prompt IA 3 — Auditor de consistencia
```text
Actúa como revisor de diseño. Te paso cinco diagramas UML en PlantUML y Mermaid: [los cinco archivos].
Verifica estas reglas y responde en una tabla con regla, elemento, problema y corrección sugerida:
C1 cada mensaje de secuencia es una operación de la clase receptora; C2 cada transición de estados
corresponde a una operación de la clase; C3 multiplicidades coherentes con los criterios de
aceptación; C4 paquetes sin ciclos; C5 nombres consistentes. No reescribas los diagramas; solo
reporta hallazgos y cita la línea.
```
