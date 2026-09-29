# Vista de despliegue de San Camilo en Línea (Python Diagrams + Graphviz)
# Ejecutar desde docs/architecture/diagramas:  python despliegue.py
from diagrams import Diagram, Cluster, Edge
from diagrams.generic.device import Mobile
from diagrams.onprem.network import Nginx, Internet
from diagrams.programming.language import Nodejs
from diagrams.programming.framework import React
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.generic.storage import Storage

graph_attr = {"fontsize": "20", "bgcolor": "white", "pad": "0.3"}

with Diagram("San Camilo en Línea - Vista de despliegue", filename="img/despliegue",
             show=False, direction="LR", graph_attr=graph_attr):
    cliente = Mobile("Cliente\n(PWA)")
    comerciante = Mobile("Comerciante\n(Android gama baja)")
    repartidor = Mobile("Repartidor\n(PWA)")

    with Cluster("VPS Linux (~US$ 6/mes)"):
        proxy = Nginx("Nginx\nHTTPS + archivos PWA")
        with Cluster("Monolito modular"):
            front = React("PWA React\n(build estático)")
            app = Nodejs("API Express\n5 módulos")
        db = PostgreSQL("PostgreSQL\nesquema por módulo\n+ cola pg-boss")
        fotos = Storage("Fotos WebP")
        with Cluster("Monitoreo"):
            metricas = Prometheus("Prometheus")
            panel = Grafana("Grafana")

    culqi = Internet("Culqi\n(Yape)")
    whatsapp = Internet("WhatsApp\nCloud API")

    [cliente, comerciante, repartidor] >> Edge(label="HTTPS") >> proxy
    proxy >> front
    proxy >> Edge(label="/api") >> app
    app >> Edge(label="SQL") >> db
    app >> fotos
    app >> Edge(label="avisos (reintento vía pg-boss)") >> whatsapp
    app >> Edge(label="cargo con token Yape") >> culqi
    metricas >> Edge(style="dashed", label="scrape /metrics") >> app
    panel >> metricas
