# models/reserva.py
import uuid
from datetime import date
from typing import Literal
from .cliente import Cliente # Import relativo dentro do pacote
from .quarto import Quarto   # Import relativo dentro do pacote

StatusReserva = Literal["confirmada", "cancelada", "concluída", "pendente"]

class Reserva:
    """Classe para representar uma reserva no hotel."""
    def __init__(self, cliente: Cliente, quarto: Quarto, data_checkin: date, data_checkout: date):
        if not isinstance(cliente, Cliente):
            raise TypeError("O 'cliente' fornecido não é um objeto Cliente válido.")
        if not isinstance(quarto, Quarto):
            raise TypeError("O 'quarto' fornecido não é um objeto Quarto válido.")
        if not isinstance(data_checkin, date) or not isinstance(data_checkout, date):
            raise TypeError("As datas de check-in e check-out devem ser objetos date.")
        if data_checkout <= data_checkin:
            raise ValueError("A data de check-out deve ser posterior à data de check-in.")

        self._reserva_id = str(uuid.uuid4()) # ID único para a reserva
        self._cliente = cliente
        self._quarto = quarto
        self._data_checkin = data_checkin
        self._data_checkout = data_checkout
        self._status_reserva: StatusReserva = "confirmada" # Status inicial

    # --- Getters usando @property ---
    @property
    def reserva_id(self) -> str:
        return self._reserva_id

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def quarto(self) -> Quarto:
        return self._quarto

    @property
    def data_checkin(self) -> date:
        return self._data_checkin

    @property
    def data_checkout(self) -> date:
        return self._data_checkout

    @property
    def status_reserva(self) -> StatusReserva:
        return self._status_reserva

    # --- Setter para o status da reserva ---
    def set_status_reserva(self, status: StatusReserva):
        """Define o status da reserva."""
        if status in ["confirmada", "cancelada", "concluída", "pendente"]:
            self._status_reserva = status
        else:
            print(f"Erro: Status '{status}' inválido para a reserva {self.reserva_id}.")
            # Ou raise ValueError("Status de reserva inválido.")

    # --- Outros Métodos ---
    def calcular_duracao_estadia(self) -> int:
        """Calcula a duração da estadia em dias."""
        return (self._data_checkout - self._data_checkin).days

    def calcular_custo_total(self) -> float:
        """Calcula o custo total da reserva."""
        duracao = self.calcular_duracao_estadia()
        return duracao * self._quarto.preco_diaria

    def exibir_informacoes(self) -> str:
        """Retorna uma string com os detalhes da reserva."""
        return (f"--- Detalhes da Reserva ID: {self.reserva_id[:8]}... ---\\n"
                f"Cliente: {self.cliente.nome} (ID: {self.cliente.id_unico[:8]}...)\\n"
                f"Quarto: {self.quarto.numero} ({self.quarto.tipo.capitalize()})\\n"
                f"Check-in: {self.data_checkin.strftime('%d/%m/%Y')}\\n"
                f"Check-out: {self.data_checkout.strftime('%d/%m/%Y')}\\n"
                f"Duração: {self.calcular_duracao_estadia()} noites\\n"
                f"Custo Total Estimado: R$ {self.calcular_custo_total():.2f}\\n"
                f"Status da Reserva: {self.status_reserva.capitalize()}")

    def __str__(self) -> str:
        """Representação em string do objeto Reserva."""
        return f"Reserva {self.reserva_id[:8]}... ({self.cliente.nome} -> Q{self.quarto.numero}, Status: {self.status_reserva})"

    def __repr__(self) -> str:
        """Representação 'oficial' do objeto."""
        return (f"Reserva(id='{self.reserva_id}', cliente={repr(self.cliente)}, quarto={repr(self.quarto)}, "
                f"checkin={repr(self.data_checkin)}, checkout={repr(self.data_checkout)}, status='{self.status_reserva}')")

