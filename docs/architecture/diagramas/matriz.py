# Genera diagramas/img/matriz-decision.png a partir de la matriz de decisión
import matplotlib.pyplot as plt
pesos = [25, 20, 20, 15, 10, 10]
puntajes = {"A. Capas": [5, 5, 4, 2, 5, 2],
            "B. Monolito modular": [4, 5, 4, 4, 4, 4],
            "C. Microservicios": [1, 2, 4, 5, 1, 4]}
totales = {k: sum(p * s for p, s in zip(pesos, v)) / 100 for k, v in puntajes.items()}
fig, ax = plt.subplots(figsize=(7, 3.6), dpi=160)
bars = ax.bar(totales.keys(), totales.values(), color=["#9aa7b5", "#2E7D32", "#c8310e"], width=.55)
for b, t in zip(bars, totales.values()):
    ax.text(b.get_x() + b.get_width() / 2, t + .07, f"{t:.2f}".replace(".", ","), ha="center", fontweight="bold")
ax.set_ylim(0, 5); ax.set_ylabel("Total ponderado (1–5)")
ax.set_title("San Camilo en Línea — Matriz de decisión ponderada")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout(); plt.savefig("img/matriz-decision.png")
