from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4


class EstadoPedido(Enum):
    BORRADOR = "BORRADOR"
    CONFIRMADO = "CONFIRMADO"
    PAGADO = "PAGADO"
    CANCELADO = "CANCELADO"


class EstadoPedidoPuesto(Enum):
    RECIBIDO = "RECIBIDO"
    LISTO = "LISTO"
    RECOGIDO = "RECOGIDO"
    ENTREGADO = "ENTREGADO"
    RECHAZADO = "RECHAZADO"


class TipoEntrega(Enum):
    RECOJO = "RECOJO"
    DELIVERY = "DELIVERY"


@dataclass
class Cliente:
    nombre: str
    celular: str
    id: UUID = field(default_factory=uuid4)


@dataclass
class Puesto:
    nombre: str
    rubro: str
    celular_comerciante: str
    id: UUID = field(default_factory=uuid4)


@dataclass
class Producto:
    nombre: str
    precio: Decimal
    stock: int
    puesto: Puesto
    id: UUID = field(default_factory=uuid4)

    def reservar(self, cantidad: int) -> None:
        if cantidad > self.stock:
            raise ValueError("Stock insuficiente")
        self.stock -= cantidad

    def liberar(self, cantidad: int) -> None:
        self.stock += cantidad


@dataclass
class LineaPedido:
    producto: Producto
    cantidad: int
    precio_unitario: Decimal

    def subtotal(self) -> Decimal:
        return self.precio_unitario * self.cantidad


@dataclass
class Pago:
    monto: Decimal
    codigo_operacion: str
    aprobado: bool
    id: UUID = field(default_factory=uuid4)


@dataclass
class AvisoPedido:
    celular: str
    puesto: str
    resumen: str


@dataclass
class PedidoPuesto:
    puesto: Puesto
    lineas: list[LineaPedido] = field(default_factory=list)
    estado: EstadoPedidoPuesto | None = None
    id: UUID = field(default_factory=uuid4)

    def recibir(self) -> None:
        self.estado = EstadoPedidoPuesto.RECIBIDO

    def subtotal(self) -> Decimal:
        return sum((linea.subtotal() for linea in self.lineas), Decimal("0"))

    def marcar_listo(self) -> None:
        self._exigir(EstadoPedidoPuesto.RECIBIDO)
        self.estado = EstadoPedidoPuesto.LISTO

    def rechazar(self, motivo: str) -> None:
        self._exigir(EstadoPedidoPuesto.RECIBIDO)
        for linea in self.lineas:
            linea.producto.liberar(linea.cantidad)
        self.estado = EstadoPedidoPuesto.RECHAZADO

    def registrar_recojo(self) -> None:
        self._exigir(EstadoPedidoPuesto.LISTO)
        self.estado = EstadoPedidoPuesto.RECOGIDO

    def confirmar_entrega(self) -> None:
        self._exigir(EstadoPedidoPuesto.RECOGIDO)
        self.estado = EstadoPedidoPuesto.ENTREGADO

    def _exigir(self, esperado: EstadoPedidoPuesto) -> None:
        if self.estado is not esperado:
            raise ValueError(f"Transición no permitida desde {self.estado}")


@dataclass
class Pedido:
    cliente: Cliente
    tipo_entrega: TipoEntrega
    lineas: list[LineaPedido] = field(default_factory=list)
    pedidos_puesto: list[PedidoPuesto] = field(default_factory=list)
    estado: EstadoPedido = EstadoPedido.BORRADOR
    pago: Pago | None = None
    fecha: datetime = field(default_factory=datetime.now)
    id: UUID = field(default_factory=uuid4)

    def agregar_producto(self, producto: Producto, cantidad: int) -> None:
        self.lineas.append(LineaPedido(producto, cantidad, producto.precio))

    def calcular_total(self) -> Decimal:
        return sum((linea.subtotal() for linea in self.lineas), Decimal("0"))

    def confirmar(self) -> None:
        if not self.lineas:
            raise ValueError("El pedido debe tener al menos una línea")
        for linea in self.lineas:
            linea.producto.reservar(linea.cantidad)
        self.estado = EstadoPedido.CONFIRMADO

    def registrar_pago(self, pago: Pago) -> None:
        self.pago = pago
        self.estado = EstadoPedido.PAGADO
        por_puesto: dict[UUID, PedidoPuesto] = {}
        for linea in self.lineas:
            puesto = linea.producto.puesto
            sub = por_puesto.setdefault(puesto.id, PedidoPuesto(puesto))
            sub.lineas.append(linea)
        self.pedidos_puesto = list(por_puesto.values())
        for sub in self.pedidos_puesto:
            sub.recibir()

    def cancelar(self, motivo: str) -> None:
        for linea in self.lineas:
            linea.producto.liberar(linea.cantidad)
        self.estado = EstadoPedido.CANCELADO


class PasarelaPago(ABC):
    @abstractmethod
    def cobrar(self, monto: Decimal, token_yape: str) -> Pago: ...

    @abstractmethod
    def reembolsar(self, codigo_operacion: str, monto: Decimal) -> None: ...


class CulqiYapeAdapter(PasarelaPago):
    def cobrar(self, monto: Decimal, token_yape: str) -> Pago:
        raise NotImplementedError("Integrar con Culqi")

    def reembolsar(self, codigo_operacion: str, monto: Decimal) -> None:
        raise NotImplementedError("Integrar con Culqi")


class Notificador(ABC):
    @abstractmethod
    def notificar_pedido_recibido(self, aviso: AvisoPedido) -> None: ...


class WhatsAppAdapter(Notificador):
    def notificar_pedido_recibido(self, aviso: AvisoPedido) -> None:
        raise NotImplementedError("Integrar con WhatsApp Business Cloud API")


class RepositorioPedidos(ABC):
    @abstractmethod
    def buscar(self, id: UUID) -> Pedido: ...

    @abstractmethod
    def guardar(self, pedido: Pedido) -> None: ...


class ServicioPedidos:
    def __init__(
        self,
        repositorio: RepositorioPedidos,
        pasarela: PasarelaPago,
        notificador: Notificador,
    ) -> None:
        self.repositorio = repositorio
        self.pasarela = pasarela
        self.notificador = notificador

    def confirmar_y_pagar(self, pedido_id: UUID, token_yape: str) -> Pedido:
        pedido = self.repositorio.buscar(pedido_id)
        pedido.confirmar()
        pago = self.pasarela.cobrar(pedido.calcular_total(), token_yape)
        if pago.aprobado:
            pedido.registrar_pago(pago)
            self.repositorio.guardar(pedido)
            for sub in pedido.pedidos_puesto:
                self.notificador.notificar_pedido_recibido(
                    AvisoPedido(
                        celular=sub.puesto.celular_comerciante,
                        puesto=sub.puesto.nombre,
                        resumen=f"{len(sub.lineas)} productos por S/ {sub.subtotal()}",
                    )
                )
        else:
            pedido.cancelar("pago rechazado")
            self.repositorio.guardar(pedido)
        return pedido

    def rechazar_pedido_puesto(self, pedido_id: UUID, pedido_puesto_id: UUID, motivo: str) -> None:
        pedido = self.repositorio.buscar(pedido_id)
        sub = next(s for s in pedido.pedidos_puesto if s.id == pedido_puesto_id)
        sub.rechazar(motivo)
        if pedido.pago is not None:
            self.pasarela.reembolsar(pedido.pago.codigo_operacion, sub.subtotal())
        self.repositorio.guardar(pedido)
