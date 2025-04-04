# models/__init__.py
# Torna as classes facilmente importáveis a partir do pacote 'models'

from .pessoa import Pessoa
from .cliente import Cliente
from .quarto import Quarto, TipoQuarto, StatusDisponibilidade
from .reserva import Reserva, StatusReserva
from .gerenciador import GerenciadorDeReservas

# Opcional: Define o que é exportado quando se usa 'from models import *'
__all__ = [
    "Pessoa",
    "Cliente",
    "Quarto", "TipoQuarto", "StatusDisponibilidade",
    "Reserva", "StatusReserva",
    "GerenciadorDeReservas",
]
