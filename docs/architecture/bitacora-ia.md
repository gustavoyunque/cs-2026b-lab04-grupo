# Bitácora de uso de IA — San Camilo en Línea

| # | Fecha | Herramienta | Prompt (resumen) | Qué propuso la IA | Qué verificamos o corregimos | Decisión |
|---|-------|-------------|------------------|-------------------|------------------------------|----------|
| 1 | 29/09 | Claude | Prompt 1 adaptado (RCRTF): 3 alternativas de estilo para San Camilo en Línea, con 1 developer, 1 mes y VPS de bajo costo | Monolito en capas, monolito modular y microservicios; recomendó el monolito modular | Se contrastó con R-01, R-02 y R-03: la recomendación es coherente con el plazo y el equipo; los microservicios quedan descartados por costo operativo | Aceptada |
| 2 | 29/09 | Claude | Prompt 2: crítica adversarial ("abogado del diablo") contra el monolito modular | 5 riesgos: erosión de límites entre módulos, VPS como punto único de falla, Redis como componente extra, fotos en disco sin respaldo, costo y aprobación de plantillas de WhatsApp | Se aceptaron las mitigaciones: dependency-cruiser en CI, PM2 + backups diarios, **reemplazar Redis por pg-boss**; se rechazó mover las fotos a S3 porque agrega costo (R-03) y basta con compresión WebP + backup | Corregida |
| 3 | 29/09 | Claude | Prompt 3: calcular la matriz ponderada con 6 criterios y los puntajes definidos | Totales: A = 4,00; B = 4,20; C = 2,70 | Al recalcular con `diagramas/matriz.py` el total de A es **4,05**, no 4,00 (error aritmético de la IA). El ganador no cambia | Corregida |
| 4 | 29/09 | Claude | Prompt 4: generar el código Mermaid de la arquitectura elegida a partir de la matriz | Diagrama `flowchart` con actores, 5 módulos, infraestructura, PostgreSQL y servicios externos | Se validó renderizándolo con mermaid-cli (sin errores); se agregó el almacenamiento de fotos y los IDs de requisitos (RF-xx) en cada módulo para trazabilidad con drivers.md | Corregida |
| 5 | 29/09 | Claude | Prompt 5: ¿cómo cobrar con Yape desde una web? | Integrar Yape mediante una pasarela autorizada (Culqi) con token de Yape | Se revisó la documentación oficial de Culqi (cargo único con token de Yape): la afirmación es correcta | Aceptada |
| 6 | 29/09 | Claude | Prompt 6: redactar borradores de ADR-002 (PWA vs nativa) y ADR-003 (pagos y notificaciones) | Borradores completos con contexto, alternativas, decisión y consecuencias | Se revisó que cada contexto cite IDs de drivers.md; se agregó el riesgo de plantillas aprobadas de WhatsApp para mensajes iniciados por la empresa | Corregida |

> Nunca se incluyeron datos personales ni información confidencial en los prompts.

## Anexo: prompts

### Prompt 1 — Generación de alternativas
```text
Actúa como arquitecto de software senior con experiencia en sistemas para PYMES.
Contexto: plataforma "San Camilo en Línea" para los puestos del Mercado San Camilo (Arequipa).
Los comerciantes publican productos desde su celular; los clientes arman un pedido con productos
de varios puestos, eligen recojo o delivery y pagan con Yape; el comerciante recibe la confirmación
por WhatsApp; un repartidor recoge y entrega. ~150 clientes simultáneos en la hora pico del sábado.
Restricciones: 1 developer con experiencia en JavaScript/React, Node.js, Python y SQL; MVP en
producción en 1 mes; presupuesto bajo (un VPS de ~US$ 6/mes); comerciantes con celulares Android
de gama baja y señal 3G. Atributo crítico: el comerciante publica un producto en ≤ 3 toques.
Tarea: propón 3 alternativas de estilo arquitectónico. Para cada una indica fortalezas, debilidades,
riesgos y qué atributos de calidad favorece o penaliza.
Formato: tabla comparativa en Markdown y, al final, tu recomendación justificada.
No inventes APIs ni capacidades de servicios; si no estás seguro, indícalo.
```

### Prompt 2 — Crítica adversarial
```text
Ahora actúa como "abogado del diablo". Critica duramente la alternativa que recomendaste
(monolito modular): ¿qué supuestos no se cumplen con nuestras restricciones?, ¿qué podría fallar
en producción?, ¿qué costo oculto tiene? Enumera los 5 riesgos más graves y, para cada uno,
una táctica arquitectónica de mitigación.
```

### Prompt 3 — Cálculo de la matriz
```text
Con estos criterios y pesos: tiempo de entrega 25 %, costo operativo 20 %, capacidad de
interacción 20 %, modificabilidad 15 %, simplicidad operativa 10 %, disponibilidad ante fallas
externas 10 %; y estos puntajes (1–5) para capas, monolito modular y microservicios: [...],
calcula el total ponderado de cada alternativa y muestra la tabla en Markdown.
```

### Prompt 4 — Diagrama Mermaid
```text
A partir de esta matriz de decisión y de drivers.md, genera un diagrama Mermaid (flowchart TB)
del monolito modular: mínimo 3 actores, los 5 módulos agrupados con subgraph, la capa de
infraestructura, PostgreSQL y los servicios externos Culqi y WhatsApp. Usa classDef para
distinguir módulos, actores y servicios externos. Devuelve solo el código.
```

### Prompt 5 — Verificación de Yape
```text
¿Cómo puede una aplicación web de un pequeño comercio en Perú cobrar con Yape?
¿Existe una API pública de Yape o debe usarse una pasarela? Indica la fuente oficial y
dime si no estás seguro.
```

### Prompt 6 — Borradores de ADR
```text
Usando esta plantilla de ADR [plantilla 000] y los drivers de drivers.md, redacta el ADR-002
(PWA vs app nativa Android) y el ADR-003 (integración de pagos y notificaciones con puertos,
adaptadores y cola de reintentos). El contexto debe citar los IDs RF-, QA- y R- y cada ADR debe
tener al menos una consecuencia positiva y una negativa.
```
