# models/gerenciador.py
from datetime import date
from typing import List, Optional # Para type hinting

# Import relativo dentro do pacote
from .cliente import Cliente
from .quarto import Quarto
from .reserva import Reserva

class GerenciadorDeReservas:
    """Classe para gerenciar clientes, quartos e reservas do hotel."""
    def __init__(self):
        self._clientes: List[Cliente] = []
        self._quartos: List[Quarto] = []
        self._reservas: List[Reserva] = []

    # --- Gerenciamento de Clientes ---
    def adicionar_cliente(self, cliente: Cliente) -> bool:
        """Adiciona um novo cliente à lista, evitando duplicatas de ID ou e-mail."""
        if not isinstance(cliente, Cliente):
            print("Erro: Objeto fornecido não é um Cliente.")
            return False
        # Verifica se já existe cliente com mesmo ID ou E-mail
        if any(c.id_unico == cliente.id_unico for c in self._clientes):
            print(f"Erro: Cliente com ID {cliente.id_unico} já existe.")
            return False
        if any(c.email == cliente.email for c in self._clientes):
            print(f"Erro: Cliente com E-mail {cliente.email} já existe.")
            return False

        self._clientes.append(cliente)
        print(f"Cliente '{cliente.nome}' adicionado com sucesso.")
        return True

    def buscar_cliente_por_id(self, id_unico: str) -> Optional[Cliente]:
        """Busca um cliente pelo seu ID único."""
        for cliente in self._clientes:
            if cliente.id_unico == id_unico:
                return cliente
        return None # Retorna None se não encontrar

    def listar_clientes(self) -> List[Cliente]:
        """Retorna a lista de todos os clientes."""
        return self._clientes

    # --- Gerenciamento de Quartos ---
    def adicionar_quarto(self, quarto: Quarto) -> bool:
        """Adiciona um novo quarto à lista, evitando duplicatas de número."""
        if not isinstance(quarto, Quarto):
            print("Erro: Objeto fornecido não é um Quarto.")
            return False
        # Verifica se já existe quarto com mesmo número
        if any(q.numero == quarto.numero for q in self._quartos):
            print(f"Erro: Quarto número {quarto.numero} já existe.")
            return False

        self._quartos.append(quarto)
        print(f"Quarto {quarto.numero} ({quarto.tipo}) adicionado com sucesso.")
        return True

    def buscar_quarto_por_numero(self, numero_quarto: int) -> Optional[Quarto]:
        """Busca um quarto pelo seu número."""
        for quarto in self._quartos:
            if quarto.numero == numero_quarto:
                return quarto
        return None

    def listar_quartos(self, status_desejado: Optional[str] = None) -> List[Quarto]:
        """Retorna a lista de quartos, opcionalmente filtrada por status."""
        if status_desejado:
            if status_desejado not in ["disponível", "ocupado", "manutenção"]:
                 print(f"Aviso: Status '{status_desejado}' inválido para filtro. Listando todos.")
                 return self._quartos
            return [q for q in self._quartos if q.status_disponibilidade == status_desejado]
        return self._quartos

    # --- Gerenciamento de Reservas ---
    def verificar_disponibilidade(self, numero_quarto: int, data_checkin: date, data_checkout: date) -> bool:
        """Verifica se um quarto está disponível para um determinado período."""
        quarto = self.buscar_quarto_por_numero(numero_quarto)
        if not quarto:
            print(f"Erro: Quarto número {numero_quarto} não encontrado.")
            return False

        # 1. Verifica o status geral do quarto (manutenção, etc.)
        if quarto.status_disponibilidade == "manutenção":
             print(f"Quarto {numero_quarto} está em manutenção.")
             return False

        # 2. Verifica conflitos com reservas existentes para o mesmo quarto
        # Uma reserva conflita se:
        # (checkin_nova < checkout_existente) AND (checkout_nova > checkin_existente)
        for reserva in self._reservas:
            if reserva.quarto.numero == numero_quarto and reserva.status_reserva == "confirmada":
                # Verifica sobreposição de datas
                if (data_checkin < reserva.data_checkout) and (data_checkout > reserva.data_checkin):
                    print(f"Conflito: Quarto {numero_quarto} já reservado de {reserva.data_checkin.strftime('%d/%m/%Y')} a {reserva.data_checkout.strftime('%d/%m/%Y')}.")
                    return False # Há conflito

        # Se passou por todas as verificações, está disponível
        # Nota: O status 'ocupado' é gerenciado pelas reservas ativas.
        # Se não houver conflito, mesmo que o status base seja 'disponível',
        # ele está efetivamente disponível para *este* período.
        return True

    def criar_reserva(self, id_cliente: str, numero_quarto: int, data_checkin: date, data_checkout: date) -> Optional[Reserva]:
        """Cria uma nova reserva se o cliente existir e o quarto estiver disponível."""
        cliente = self.buscar_cliente_por_id(id_cliente)
        if not cliente:
            print(f"Erro ao criar reserva: Cliente com ID {id_cliente} não encontrado.")
            return None

        quarto = self.buscar_quarto_por_numero(numero_quarto)
        if not quarto:
            print(f"Erro ao criar reserva: Quarto número {numero_quarto} não encontrado.")
            return None

        # Verifica se as datas são válidas
        if data_checkout <= data_checkin:
             print("Erro ao criar reserva: Data de check-out deve ser posterior à data de check-in.")
             return None
        if data_checkin < date.today(): # Não permite reservar no passado
             print("Erro ao criar reserva: Data de check-in não pode ser no passado.")
             return None


        # Verifica disponibilidade real (considerando outras reservas)
        if self.verificar_disponibilidade(numero_quarto, data_checkin, data_checkout):
            try:
                nova_reserva = Reserva(cliente, quarto, data_checkin, data_checkout)
                self._reservas.append(nova_reserva)
                # Opcional: Atualizar o status do quarto para 'ocupado' se a reserva começar hoje?
                # Por enquanto, a disponibilidade é verificada dinamicamente.
                # Se quisesse mudar o status base:
                # if data_checkin <= date.today() < data_checkout:
                #     quarto.set_status_disponibilidade("ocupado")
                print(f"Reserva criada com sucesso! ID: {nova_reserva.reserva_id}")
                return nova_reserva
            except (ValueError, TypeError) as e:
                print(f"Erro ao instanciar reserva: {e}")
                return None
        else:
            print(f"Erro ao criar reserva: Quarto {numero_quarto} não está disponível no período solicitado.")
            return None

    def cancelar_reserva(self, reserva_id: str) -> bool:
        """Cancela uma reserva existente pelo seu ID."""
        reserva_encontrada = None
        for reserva in self._reservas:
            if reserva.reserva_id == reserva_id:
                reserva_encontrada = reserva
                break

        if reserva_encontrada:
            if reserva_encontrada.status_reserva == "cancelada":
                 print(f"Reserva {reserva_id} já está cancelada.")
                 return False
            # Verifica se já passou o check-in (poderia ter regras de negócio aqui)
            if reserva_encontrada.data_checkin < date.today() and reserva_encontrada.status_reserva != "concluída":
                print(f"Aviso: Cancelando reserva {reserva_id} após a data de check-in.")
                # Poderia adicionar lógica para taxas de cancelamento, etc.

            reserva_encontrada.set_status_reserva("cancelada")
            print(f"Reserva {reserva_id} cancelada com sucesso.")

            # Opcional: Verificar se o quarto deve voltar a ser 'disponível'
            # Isso é complexo se houver outras reservas futuras.
            # A verificação dinâmica de disponibilidade é mais segura.
            # Se quisesse tentar:
            # quarto = reserva_encontrada.quarto
            # if not any(r.quarto == quarto and r.status_reserva == 'confirmada' and r.data_checkin <= date.today() < r.data_checkout for r in self._reservas):
            #    if quarto.status_disponibilidade == 'ocupado': # Só muda se estava ocupado por esta reserva
            #        quarto.set_status_disponibilidade('disponível')

            return True
        else:
            print(f"Erro ao cancelar: Reserva com ID {reserva_id} não encontrada.")
            return False

    def listar_reservas(self, status_desejado: Optional[str] = None) -> List[Reserva]:
        """Retorna a lista de reservas, opcionalmente filtrada por status."""
        reservas_filtradas = self._reservas
        if status_desejado:
            if status_desejado not in ["confirmada", "cancelada", "concluída", "pendente"]:
                print(f"Aviso: Status '{status_desejado}' inválido para filtro. Listando todas.")
            else:
                reservas_filtradas = [r for r in self._reservas if r.status_reserva == status_desejado]

        # Ordena por data de check-in para melhor visualização
        return sorted(reservas_filtradas, key=lambda r: r.data_checkin)

    def listar_reservas_por_cliente(self, id_cliente: str) -> List[Reserva]:
        """Retorna a lista de reservas de um cliente específico."""
        cliente = self.buscar_cliente_por_id(id_cliente)
        if not cliente:
            print(f"Cliente com ID {id_cliente} não encontrado.")
            return []
        reservas_cliente = [r for r in self._reservas if r.cliente.id_unico == id_cliente]
        return sorted(reservas_cliente, key=lambda r: r.data_checkin)

    def atualizar_status_reservas_concluidas(self):
        """Verifica reservas cuja data de checkout já passou e marca como 'concluída'."""
        hoje = date.today()
        for reserva in self._reservas:
            if reserva.status_reserva == "confirmada" and reserva.data_checkout <= hoje:
                reserva.set_status_reserva("concluída")
                print(f"Reserva {reserva.reserva_id} marcada como concluída.")
                # Aqui também poderia verificar se o quarto agora está disponível
