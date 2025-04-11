import flet as ft
import json
import uuid
from datetime import datetime, timedelta, date
import os
import calendar
from typing import List, Dict, Optional, Any, Tuple

# Classes do modelo de dados
class Cliente:
    def __init__(self, nome: str, telefone: str, email: str, id: str = None):
        self._nome = nome
        self._telefone = telefone
        self._email = email
        self._id = id if id else str(uuid.uuid4())
    
    @property
    def nome(self) -> str:
        return self._nome
    
    @nome.setter
    def nome(self, valor: str) -> None:
        self._nome = valor
    
    @property
    def telefone(self) -> str:
        return self._telefone
    
    @telefone.setter
    def telefone(self, valor: str) -> None:
        self._telefone = valor
    
    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, valor: str) -> None:
        self._email = valor
    
    @property
    def id(self) -> str:
        return self._id
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "nome": self._nome,
            "telefone": self._telefone,
            "email": self._email,
            "id": self._id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Cliente':
        return cls(
            nome=data["nome"],
            telefone=data["telefone"],
            email=data["email"],
            id=data["id"]
        )


class Quarto:
    TIPOS = ["Single", "Double", "Suite"]
    
    def __init__(self, numero: int, tipo: str, preco: float, disponivel: bool = True):
        self._numero = numero
        self._tipo = tipo if tipo in self.TIPOS else "Single"
        self._preco = preco
        self._disponivel = disponivel
    
    @property
    def numero(self) -> int:
        return self._numero
    
    @property
    def tipo(self) -> str:
        return self._tipo
    
    @tipo.setter
    def tipo(self, valor: str) -> None:
        if valor in self.TIPOS:
            self._tipo = valor
    
    @property
    def preco(self) -> float:
        return self._preco
    
    @preco.setter
    def preco(self, valor: float) -> None:
        if valor > 0:
            self._preco = valor
    
    @property
    def disponivel(self) -> bool:
        return self._disponivel
    
    @disponivel.setter
    def disponivel(self, valor: bool) -> None:
        self._disponivel = valor
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "numero": self._numero,
            "tipo": self._tipo,
            "preco": self._preco,
            "disponivel": self._disponivel
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Quarto':
        return cls(
            numero=data["numero"],
            tipo=data["tipo"],
            preco=data["preco"],
            disponivel=data["disponivel"]
        )


class Reserva:
    STATUS = ["Confirmada", "Pendente", "Cancelada", "Concluída"]
    
    def __init__(self, cliente_id: str, quarto_numero: int, 
                 check_in: str, check_out: str, 
                 status: str = "Pendente", id: str = None):
        self._cliente_id = cliente_id
        self._quarto_numero = quarto_numero
        self._check_in = check_in
        self._check_out = check_out
        self._status = status if status in self.STATUS else "Pendente"
        self._id = id if id else str(uuid.uuid4())
    
    @property
    def cliente_id(self) -> str:
        return self._cliente_id
    
    @property
    def quarto_numero(self) -> int:
        return self._quarto_numero
    
    @property
    def check_in(self) -> str:
        return self._check_in
    
    @check_in.setter
    def check_in(self, valor: str) -> None:
        self._check_in = valor
    
    @property
    def check_out(self) -> str:
        return self._check_out
    
    @check_out.setter
    def check_out(self, valor: str) -> None:
        self._check_out = valor
    
    @property
    def status(self) -> str:
        return self._status
    
    @status.setter
    def status(self, valor: str) -> None:
        if valor in self.STATUS:
            self._status = valor
    
    @property
    def id(self) -> str:
        return self._id
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "cliente_id": self._cliente_id,
            "quarto_numero": self._quarto_numero,
            "check_in": self._check_in,
            "check_out": self._check_out,
            "status": self._status,
            "id": self._id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Reserva':
        return cls(
            cliente_id=data["cliente_id"],
            quarto_numero=data["quarto_numero"],
            check_in=data["check_in"],
            check_out=data["check_out"],
            status=data["status"],
            id=data["id"]
        )


class GerenciadorDeReservas:
    def __init__(self):
        self._clientes: List[Cliente] = []
        self._quartos: List[Quarto] = []
        self._reservas: List[Reserva] = []
        self._arquivo_dados = "dados_hotel.json"
        self._carregar_dados()
    
    def adicionar_cliente(self, cliente: Cliente) -> None:
        self._clientes.append(cliente)
        self._salvar_dados()
    
    def obter_cliente_por_id(self, cliente_id: str) -> Optional[Cliente]:
        for cliente in self._clientes:
            if cliente.id == cliente_id:
                return cliente
        return None
    
    def atualizar_cliente(self, cliente_id: str, nome: str, telefone: str, email: str) -> bool:
        cliente = self.obter_cliente_por_id(cliente_id)
        if cliente:
            cliente.nome = nome
            cliente.telefone = telefone
            cliente.email = email
            self._salvar_dados()
            return True
        return False
    
    def remover_cliente(self, cliente_id: str) -> bool:
        cliente = self.obter_cliente_por_id(cliente_id)
        if cliente:
            self._clientes.remove(cliente)
            # Remover também todas as reservas associadas a este cliente
            self._reservas = [r for r in self._reservas if r.cliente_id != cliente_id]
            self._salvar_dados()
            return True
        return False
    
    def adicionar_quarto(self, quarto: Quarto) -> None:
        self._quartos.append(quarto)
        self._salvar_dados()
    
    def obter_quarto_por_numero(self, numero: int) -> Optional[Quarto]:
        for quarto in self._quartos:
            if quarto.numero == numero:
                return quarto
        return None
    
    def atualizar_quarto(self, numero: int, tipo: str, preco: float, disponivel: bool) -> bool:
        quarto = self.obter_quarto_por_numero(numero)
        if quarto:
            quarto.tipo = tipo
            quarto.preco = preco
            quarto.disponivel = disponivel
            self._salvar_dados()
            return True
        return False
    
    def remover_quarto(self, numero: int) -> bool:
        quarto = self.obter_quarto_por_numero(numero)
        if quarto:
            self._quartos.remove(quarto)
            # Remover também todas as reservas associadas a este quarto
            self._reservas = [r for r in self._reservas if r.quarto_numero != numero]
            self._salvar_dados()
            return True
        return False
    
    def criar_reserva(self, cliente_id: str, quarto_numero: int, 
                      check_in: str, check_out: str) -> Optional[Reserva]:
        cliente = self.obter_cliente_por_id(cliente_id)
        quarto = self.obter_quarto_por_numero(quarto_numero)
        
        if not cliente or not quarto:
            return None
        
        # Verificar se o quarto está disponível nas datas solicitadas
        if not self._verificar_disponibilidade(quarto_numero, check_in, check_out):
            return None
        
        reserva = Reserva(cliente_id, quarto_numero, check_in, check_out)
        self._reservas.append(reserva)
        
        # Não marcamos o quarto como indisponível permanentemente
        # Apenas verificamos a disponibilidade para o período específico
        
        self._salvar_dados()
        return reserva
    
    def _verificar_disponibilidade(self, quarto_numero: int, check_in: str, check_out: str) -> bool:
        # Converter strings para objetos datetime
        try:
            data_check_in = datetime.strptime(check_in, "%d-%m-%Y")
            data_check_out = datetime.strptime(check_out, "%d-%m-%Y")
        except ValueError:
            return False
        
        # Verificar se check_out é posterior a check_in
        if data_check_out <= data_check_in:
            return False
        
        # Verificar se há sobreposição com outras reservas ativas (não canceladas)
        for reserva in self._reservas:
            if reserva.quarto_numero == quarto_numero and reserva.status != "Cancelada":
                try:
                    reserva_check_in = datetime.strptime(reserva.check_in, "%d-%m-%Y")
                    reserva_check_out = datetime.strptime(reserva.check_out, "%d-%m-%Y")
                    
                    # Verificar sobreposição
                    if (data_check_in < reserva_check_out and data_check_out > reserva_check_in):
                        return False
                except ValueError:
                    # Se houver erro no formato da data, ignorar esta reserva
                    continue
        
        return True
    
    def obter_reserva_por_id(self, reserva_id: str) -> Optional[Reserva]:
        for reserva in self._reservas:
            if reserva.id == reserva_id:
                return reserva
        return None
    
    def atualizar_reserva(self, reserva_id: str, check_in: str, check_out: str, status: str) -> bool:
        reserva = self.obter_reserva_por_id(reserva_id)
        if reserva:
            # Atualizar os dados da reserva
            reserva.check_in = check_in
            reserva.check_out = check_out
            reserva.status = status
            self._salvar_dados()
            return True
        return False
    
    def cancelar_reserva(self, reserva_id: str) -> bool:
        reserva = self.obter_reserva_por_id(reserva_id)
        if reserva:
            reserva.status = "Cancelada"
            self._salvar_dados()
            return True
        return False
    
    def listar_clientes(self) -> List[Cliente]:
        return self._clientes
    
    def listar_quartos(self) -> List[Quarto]:
        return self._quartos
    
    def listar_quartos_disponiveis(self, check_in: str = None, check_out: str = None) -> List[Quarto]:
        # Se não foram fornecidas datas, retornar todos os quartos marcados como disponíveis
        if not check_in or not check_out:
            return [q for q in self._quartos if q.disponivel]
        
        # Se foram fornecidas datas, verificar disponibilidade para o período
        quartos_disponiveis = []
        for quarto in self._quartos:
            if self._verificar_disponibilidade(quarto.numero, check_in, check_out):
                quartos_disponiveis.append(quarto)
        
        return quartos_disponiveis
    
    def listar_reservas(self) -> List[Reserva]:
        return self._reservas
    
    def listar_reservas_por_cliente(self, cliente_id: str) -> List[Reserva]:
        return [r for r in self._reservas if r.cliente_id == cliente_id]
    
    def listar_reservas_por_quarto(self, quarto_numero: int) -> List[Reserva]:
        return [r for r in self._reservas if r.quarto_numero == quarto_numero]
    
    def _salvar_dados(self) -> None:
        dados = {
            "clientes": [c.to_dict() for c in self._clientes],
            "quartos": [q.to_dict() for q in self._quartos],
            "reservas": [r.to_dict() for r in self._reservas]
        }
        
        with open(self._arquivo_dados, "w") as arquivo:
            json.dump(dados, arquivo, indent=4)
    
    def _carregar_dados(self) -> None:
        if not os.path.exists(self._arquivo_dados):
            # Criar alguns dados iniciais
            self._criar_dados_iniciais()
            return
        
        try:
            with open(self._arquivo_dados, "r") as arquivo:
                dados = json.load(arquivo)
                
                self._clientes = [Cliente.from_dict(c) for c in dados.get("clientes", [])]
                self._quartos = [Quarto.from_dict(q) for q in dados.get("quartos", [])]
                self._reservas = [Reserva.from_dict(r) for r in dados.get("reservas", [])]
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            self._criar_dados_iniciais()
    
    def _criar_dados_iniciais(self) -> None:
        # Criar alguns quartos iniciais
        self._quartos = [
            Quarto(101, "Single", 150.0),
            Quarto(102, "Single", 150.0),
            Quarto(201, "Double", 250.0),
            Quarto(202, "Double", 250.0),
            Quarto(301, "Suite", 400.0),
        ]
        
        # Salvar os dados iniciais
        self._salvar_dados()


# Função auxiliar para formatar data
def formatar_data(data: datetime) -> str:
    """Converte um objeto datetime para string no formato DD-MM-YYYY"""
    return data.strftime("%d-%m-%Y")


# Interface gráfica com Flet
def main(page: ft.Page):
    # Configurações da página
    page.title = "Refúgio dos Sonhos - Sistema de Gerenciamento"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1200
    page.window_height = 800
    page.padding = 20
    
    # Instanciar o gerenciador de reservas
    gerenciador = GerenciadorDeReservas()
    
    # Variáveis de estado
    tela_atual = ft.Ref[str]()
    tela_atual.current = "inicial"
    
    cliente_selecionado = ft.Ref[Cliente]()
    
    # Data atual para o calendário
    data_calendario = ft.Ref[datetime]()
    data_calendario.current = datetime.now()
    
    # Elementos da interface
    lista_quartos = ft.ListView(expand=True, spacing=10, padding=20)
    lista_clientes = ft.ListView(expand=True, spacing=10, padding=20)
    lista_reservas = ft.ListView(expand=True, spacing=10, padding=20)
    
    # Campos de formulário
    campo_nome = ft.TextField(label="Nome", width=300)
    campo_telefone = ft.TextField(label="Telefone", width=300)
    campo_email = ft.TextField(label="E-mail", width=300)
    
    dropdown_clientes = ft.Dropdown(label="Cliente", width=300)
    dropdown_quartos = ft.Dropdown(label="Quarto", width=300)
    
    # Datas para os calendários
    data_check_in = ft.Ref[datetime]()
    data_check_in.current = datetime.now()
    
    data_check_out = ft.Ref[datetime]()
    data_check_out.current = datetime.now() + timedelta(days=1)
    
    # Texto para exibir as datas selecionadas
    texto_check_in = ft.Text(f"Check-in: {formatar_data(data_check_in.current)}")
    texto_check_out = ft.Text(f"Check-out: {formatar_data(data_check_out.current)}")
    
    # Conteúdo principal
    conteudo_principal = ft.Container(expand=True)
    
    # Funções auxiliares
    def mostrar_snackbar(mensagem):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(mensagem),
            action="OK"
        )
        page.snack_bar.open = True
        page.update()
    
    # Funções para atualizar listas
    def atualizar_lista_quartos():
        lista_quartos.controls.clear()
        
        for quarto in gerenciador.listar_quartos():
            # Verificar disponibilidade atual (considerando reservas ativas)
            disponivel = gerenciador._verificar_disponibilidade(
                quarto.numero, 
                formatar_data(datetime.now()), 
                formatar_data(datetime.now() + timedelta(days=1))
            )
            
            card_quarto = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.KING_BED),
                            title=ft.Text(f"Quarto {quarto.numero} - {quarto.tipo}"),
                            subtitle=ft.Text(f"Preço: R$ {quarto.preco:.2f} / diária"),
                            trailing=ft.Chip(
                                label=ft.Text("Disponível" if disponivel else "Ocupado"),
                                bgcolor=ft.Colors.GREEN if disponivel else ft.Colors.RED,
                            ),
                        ),
                        ft.Row([
                            ft.TextButton("Editar", on_click=lambda e, q=quarto: mostrar_dialogo_editar_quarto(q)),
                            ft.TextButton("Excluir", on_click=lambda e, q=quarto: excluir_quarto(q))
                        ], alignment=ft.MainAxisAlignment.END)
                    ]),
                    padding=10
                )
            )
            
            lista_quartos.controls.append(card_quarto)
        
        page.update()
    
    def atualizar_lista_clientes():
        lista_clientes.controls.clear()
        
        for cliente in gerenciador.listar_clientes():
            card_cliente = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.PERSON),
                            title=ft.Text(cliente.nome),
                            subtitle=ft.Column([
                                ft.Text(f"Telefone: {cliente.telefone}"),
                                ft.Text(f"E-mail: {cliente.email}")
                            ])
                        ),
                        ft.Row([
                            ft.TextButton("Editar", on_click=lambda e, c=cliente: editar_cliente(c)),
                            ft.TextButton("Excluir", on_click=lambda e, c=cliente: excluir_cliente(c))
                        ], alignment=ft.MainAxisAlignment.END)
                    ]),
                    padding=10
                )
            )
            
            lista_clientes.controls.append(card_cliente)
        
        page.update()
    
    def atualizar_lista_reservas():
        lista_reservas.controls.clear()
        
        for reserva in gerenciador.listar_reservas():
            cliente = gerenciador.obter_cliente_por_id(reserva.cliente_id)
            quarto = gerenciador.obter_quarto_por_numero(reserva.quarto_numero)
            
            if not cliente or not quarto:
                continue
            
            cor_status = {
                "Confirmada": ft.Colors.GREEN,
                "Pendente": ft.Colors.ORANGE,
                "Cancelada": ft.Colors.RED,
                "Concluída": ft.Colors.BLUE
            }.get(reserva.status, ft.Colors.GREY)
            
            card_reserva = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.BOOKMARK),
                            title=ft.Text(f"Reserva de {cliente.nome}"),
                            subtitle=ft.Column([
                                ft.Text(f"Quarto: {quarto.numero} - {quarto.tipo}"),
                                ft.Text(f"Check-in: {reserva.check_in} | Check-out: {reserva.check_out}"),
                                ft.Chip(
                                    label=ft.Text(reserva.status),
                                    bgcolor=cor_status
                                )
                            ])
                        ),
                        ft.Row([
                            ft.TextButton("Editar", on_click=lambda e, r=reserva: editar_reserva(r)),
                            ft.TextButton("Cancelar Reserva", on_click=lambda e, r=reserva: cancelar_reserva(r))
                        ], alignment=ft.MainAxisAlignment.END)
                    ]),
                    padding=10
                )
            )
            
            lista_reservas.controls.append(card_reserva)
        
        page.update()
    
    def atualizar_dropdown_clientes():
        dropdown_clientes.options.clear()
        
        for cliente in gerenciador.listar_clientes():
            dropdown_clientes.options.append(
                ft.dropdown.Option(key=cliente.id, text=cliente.nome)
            )
        
        if dropdown_clientes.options:
            dropdown_clientes.value = dropdown_clientes.options[0].key
        
        page.update()
    
    def atualizar_dropdown_quartos():
        dropdown_quartos.options.clear()
        
        # Usar as datas selecionadas para verificar disponibilidade
        check_in = formatar_data(data_check_in.current)
        check_out = formatar_data(data_check_out.current)
        
        # Obter quartos disponíveis para o período selecionado
        quartos_disponiveis = gerenciador.listar_quartos_disponiveis(check_in, check_out)
        
        for quarto in quartos_disponiveis:
            dropdown_quartos.options.append(
                ft.dropdown.Option(
                    key=str(quarto.numero),
                    text=f"Quarto {quarto.numero} - {quarto.tipo} - R$ {quarto.preco:.2f}"
                )
            )
        
        if dropdown_quartos.options:
            dropdown_quartos.value = dropdown_quartos.options[0].key
        else:
            dropdown_quartos.value = None
        
        page.update()
    
    # Funções para manipular quartos
    def mostrar_dialogo_novo_quarto(e):
        # Campos do formulário
        campo_numero = ft.TextField(label="Número do Quarto", keyboard_type=ft.KeyboardType.NUMBER)
        dropdown_tipo = ft.Dropdown(
            label="Tipo de Quarto",
            options=[
                ft.dropdown.Option("Single"),
                ft.dropdown.Option("Double"),
                ft.dropdown.Option("Suite")
            ],
            value="Single"
        )
        campo_preco = ft.TextField(label="Preço por Diária", keyboard_type=ft.KeyboardType.NUMBER)
        
        def fechar_dialogo(e):
            dialogo.open = False
            page.update()
        
        def salvar_quarto(e):
            try:
                numero = int(campo_numero.value)
                tipo = dropdown_tipo.value
                preco = float(campo_preco.value)
                
                # Verificar se já existe um quarto com este número
                if gerenciador.obter_quarto_por_numero(numero):
                    mostrar_snackbar("Já existe um quarto com este número!")
                    return
                
                quarto = Quarto(numero, tipo, preco)
                gerenciador.adicionar_quarto(quarto)
                
                mostrar_snackbar("Quarto adicionado com sucesso!")
                atualizar_lista_quartos()
                fechar_dialogo(e)
            except ValueError:
                mostrar_snackbar("Por favor, preencha todos os campos corretamente!")
        
        # Criar o diálogo
        dialogo = ft.AlertDialog(
            title=ft.Text("Adicionar Novo Quarto"),
            content=ft.Column([
                campo_numero,
                dropdown_tipo,
                campo_preco
            ], tight=True, spacing=20, width=400),
            actions=[
                ft.TextButton("Cancelar", on_click=fechar_dialogo),
                ft.TextButton("Salvar", on_click=salvar_quarto)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        page.dialog = dialogo
        dialogo.open = True
        page.update()
    
    def mostrar_dialogo_editar_quarto(quarto):
        # Campos do formulário
        campo_numero = ft.TextField(label="Número do Quarto", value=str(quarto.numero), disabled=True)
        dropdown_tipo = ft.Dropdown(
            label="Tipo de Quarto",
            options=[
                ft.dropdown.Option("Single"),
                ft.dropdown.Option("Double"),
                ft.dropdown.Option("Suite")
            ],
            value=quarto.tipo
        )
        campo_preco = ft.TextField(label="Preço por Diária", value=str(quarto.preco))
        switch_disponivel = ft.Switch(label="Disponível", value=quarto.disponivel)
        
        def fechar_dialogo(e):
            dialogo.open = False
            page.update()
        
        def salvar_quarto(e):
            try:
                tipo = dropdown_tipo.value
                preco = float(campo_preco.value)
                disponivel = switch_disponivel.value
                
                gerenciador.atualizar_quarto(quarto.numero, tipo, preco, disponivel)
                
                mostrar_snackbar("Quarto atualizado com sucesso!")
                atualizar_lista_quartos()
                fechar_dialogo(e)
            except ValueError:
                mostrar_snackbar("Por favor, preencha todos os campos corretamente!")
        
        # Criar o diálogo
        dialogo = ft.AlertDialog(
            title=ft.Text(f"Editar Quarto {quarto.numero}"),
            content=ft.Column([
                campo_numero,
                dropdown_tipo,
                campo_preco,
                switch_disponivel
            ], tight=True, spacing=20, width=400),
            actions=[
                ft.TextButton("Cancelar", on_click=fechar_dialogo),
                ft.TextButton("Salvar", on_click=salvar_quarto)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        page.dialog = dialogo
        dialogo.open = True
        page.update()
    
    def excluir_quarto(quarto):
        def confirmar_exclusao(e):
            gerenciador.remover_quarto(quarto.numero)
            mostrar_snackbar("Quarto excluído com sucesso!")
            atualizar_lista_quartos()
            fechar_dialogo(e)
        
        def fechar_dialogo(e):
            dialogo.open = False
            page.update()
        
        # Criar o diálogo de confirmação
        dialogo = ft.AlertDialog(
            title=ft.Text("Confirmar Exclusão"),
            content=ft.Text(f"Tem certeza que deseja excluir o Quarto {quarto.numero}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=fechar_dialogo),
                ft.TextButton("Excluir", on_click=confirmar_exclusao)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        page.dialog = dialogo
        dialogo.open = True
        page.update()
    
    # Funções para manipular clientes
    def salvar_cliente(e):
        nome = campo_nome.value
        telefone = campo_telefone.value
        email = campo_email.value
        
        if not nome or not telefone or not email:
            mostrar_snackbar("Por favor, preencha todos os campos!")
            return
        
        if cliente_selecionado.current:
            # Atualizar cliente existente
            gerenciador.atualizar_cliente(
                cliente_selecionado.current.id,
                nome,
                telefone,
                email
            )
            mostrar_snackbar("Cliente atualizado com sucesso!")
        else:
            # Criar novo cliente
            cliente = Cliente(nome, telefone, email)
            gerenciador.adicionar_cliente(cliente)
            mostrar_snackbar("Cliente adicionado com sucesso!")
        
        cliente_selecionado.current = None
        navegar_para("clientes")
    
    def editar_cliente(cliente):
        cliente_selecionado.current = cliente
        campo_nome.value = cliente.nome
        campo_telefone.value = cliente.telefone
        campo_email.value = cliente.email
        
        navegar_para("novo_cliente")
    
    def excluir_cliente(cliente):
        def confirmar_exclusao(e):
            gerenciador.remover_cliente(cliente.id)
            mostrar_snackbar("Cliente excluído com sucesso!")
            atualizar_lista_clientes()
            fechar_dialogo(e)
        
        def fechar_dialogo(e):
            dialogo.open = False
            page.update()
        
        # Criar o diálogo de confirmação
        dialogo = ft.AlertDialog(
            title=ft.Text("Confirmar Exclusão"),
            content=ft.Text(f"Tem certeza que deseja excluir o cliente {cliente.nome}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=fechar_dialogo),
                ft.TextButton("Excluir", on_click=confirmar_exclusao)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        page.dialog = dialogo
        dialogo.open = True
        page.update()
    
    # Funções para manipular reservas
    def selecionar_data_check_in(e):
        def handle_date_picker_change(e):
            data_check_in.current = e.control.value
            texto_check_in.value = f"Check-in: {formatar_data(data_check_in.current)}"
            # Atualizar a lista de quartos disponíveis quando a data mudar
            atualizar_dropdown_quartos()
            page.update()
        
        # Abrir o DatePicker
        page.open(
            ft.DatePicker(
                first_date=datetime.now(),
                last_date=datetime(year=datetime.now().year + 5, month=12, day=31),
                current_date=data_check_in.current,
                on_change=handle_date_picker_change,
            )
        )
    
    def selecionar_data_check_out(e):
        def handle_date_picker_change(e):
            data_check_out.current = e.control.value
            texto_check_out.value = f"Check-out: {formatar_data(data_check_out.current)}"
            # Atualizar a lista de quartos disponíveis quando a data mudar
            atualizar_dropdown_quartos()
            page.update()
        
        # Abrir o DatePicker
        page.open(
            ft.DatePicker(
                first_date=datetime.now(),
                last_date=datetime(year=datetime.now().year + 5, month=12, day=31),
                current_date=data_check_out.current,
                on_change=handle_date_picker_change,
            )
        )
    
    def salvar_reserva(e):
        cliente_id = dropdown_clientes.value
        quarto_numero = int(dropdown_quartos.value) if dropdown_quartos.value else None
        
        if not cliente_id or not quarto_numero or not data_check_in.current or not data_check_out.current:
            mostrar_snackbar("Por favor, preencha todos os campos e selecione as datas!")
            return
        
        # Converter datas para string no formato DD-MM-YYYY
        check_in = formatar_data(data_check_in.current)
        check_out = formatar_data(data_check_out.current)
        
        # Verificar se check-out é posterior a check-in
        if data_check_out.current <= data_check_in.current:
            mostrar_snackbar("A data de check-out deve ser posterior à data de check-in!")
            return
        
        reserva = gerenciador.criar_reserva(cliente_id, quarto_numero, check_in, check_out)
        
        if reserva:
            mostrar_snackbar("Reserva criada com sucesso!")
            navegar_para("reservas")
        else:
            mostrar_snackbar("Não foi possível criar a reserva. Verifique a disponibilidade do quarto nas datas selecionadas.")
    
    def editar_reserva(reserva):
        cliente = gerenciador.obter_cliente_por_id(reserva.cliente_id)
        quarto = gerenciador.obter_quarto_por_numero(reserva.quarto_numero)
        
        # Tentar converter as datas da reserva para datetime
        try:
            data_check_in_atual = datetime.strptime(reserva.check_in, "%d-%m-%Y")
            data_check_out_atual = datetime.strptime(reserva.check_out, "%d-%m-%Y")
        except ValueError:
            # Se houver erro no formato, usar datas atuais
            data_check_in_atual = datetime.now()
            data_check_out_atual = datetime.now() + timedelta(days=1)
        
        # Referências para as novas datas
        nova_data_check_in = ft.Ref[datetime]()
        nova_data_check_in.current = data_check_in_atual
        
        nova_data_check_out = ft.Ref[datetime]()
        nova_data_check_out.current = data_check_out_atual
        
        # Textos para exibir as datas
        texto_check_in_edit = ft.Text(f"Check-in: {formatar_data(data_check_in_atual)}")
        texto_check_out_edit = ft.Text(f"Check-out: {formatar_data(data_check_out_atual)}")
        
        # Campos do formulário
        campo_cliente = ft.TextField(label="Cliente", value=cliente.nome, disabled=True)
        campo_quarto = ft.TextField(label="Quarto", value=f"{quarto.numero} - {quarto.tipo}", disabled=True)
        
        def selecionar_data_check_in_edit(e):
            def handle_date_picker_change(e):
                nova_data_check_in.current = e.control.value
                texto_check_in_edit.value = f"Check-in: {formatar_data(nova_data_check_in.current)}"
                page.update()
            
            # Abrir o DatePicker
            page.open(
                ft.DatePicker(
                    first_date=datetime.now(),
                    last_date=datetime(year=datetime.now().year + 5, month=12, day=31),
                    current_date=nova_data_check_in.current,
                    on_change=handle_date_picker_change,
                )
            )
        
        def selecionar_data_check_out_edit(e):
            def handle_date_picker_change(e):
                nova_data_check_out.current = e.control.value
                texto_check_out_edit.value = f"Check-out: {formatar_data(nova_data_check_out.current)}"
                page.update()
            
            # Abrir o DatePicker
            page.open(
                ft.DatePicker(
                    first_date=datetime.now(),
                    last_date=datetime(year=datetime.now().year + 5, month=12, day=31),
                    current_date=nova_data_check_out.current,
                    on_change=handle_date_picker_change,
                )
            )
        
        dropdown_status = ft.Dropdown(
            label="Status",
            options=[
                ft.dropdown.Option(status) for status in Reserva.STATUS
            ],
            value=reserva.status
        )
        
        def fechar_dialogo(e):
            dialogo.open = False
            page.update()
        
        def salvar_reserva_edit(e):
            check_in = formatar_data(nova_data_check_in.current)
            check_out = formatar_data(nova_data_check_out.current)
            status = dropdown_status.value
            
            # Verificar se check-out é posterior a check-in
            if nova_data_check_out.current <= nova_data_check_in.current:
                mostrar_snackbar("A data de check-out deve ser posterior à data de check-in!")
                return
            
            gerenciador.atualizar_reserva(reserva.id, check_in, check_out, status)
            
            mostrar_snackbar("Reserva atualizada com sucesso!")
            atualizar_lista_reservas()
            fechar_dialogo(e)
            
            # Se estiver na tela de calendário, atualizar o calendário
            if tela_atual.current == "calendario":
                atualizar_calendario()
        
        # Criar o diálogo
        dialogo = ft.AlertDialog(
            title=ft.Text("Editar Reserva"),
            content=ft.Column([
                campo_cliente,
                campo_quarto,
                ft.Row([
                    ft.Column([
                        ft.Text("Check-in:"),
                        texto_check_in_edit,
                        ft.ElevatedButton(
                            "Selecionar Data",
                            icon=ft.Icons.CALENDAR_MONTH,
                            on_click=selecionar_data_check_in_edit
                        )
                    ]),
                    ft.Column([
                        ft.Text("Check-out:"),
                        texto_check_out_edit,
                        ft.ElevatedButton(
                            "Selecionar Data",
                            icon=ft.Icons.CALENDAR_MONTH,
                            on_click=selecionar_data_check_out_edit
                        )
                    ])
                ]),
                dropdown_status
            ], tight=True, spacing=20, width=400),
            actions=[
                ft.TextButton("Cancelar", on_click=fechar_dialogo),
                ft.TextButton("Salvar", on_click=salvar_reserva_edit)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        page.dialog = dialogo
        dialogo.open = True
        page.update()
    
    def cancelar_reserva(reserva):
        def confirmar_cancelamento(e):
            if gerenciador.cancelar_reserva(reserva.id):
                mostrar_snackbar("Reserva cancelada com sucesso!")
                atualizar_lista_reservas()
                
                # Se estiver na tela de calendário, atualizar o calendário
                if tela_atual.current == "calendario":
                    atualizar_calendario()
                
                fechar_dialogo(e)
            else:
                mostrar_snackbar("Erro ao cancelar a reserva!")
        
        def fechar_dialogo(e):
            dialogo.open = False
            page.update()
        
        # Criar o diálogo de confirmação
        dialogo = ft.AlertDialog(
            title=ft.Text("Confirmar Cancelamento"),
            content=ft.Text("Tem certeza que deseja cancelar esta reserva?"),
            actions=[
                ft.TextButton("Não", on_click=fechar_dialogo),
                ft.TextButton("Sim, Cancelar", on_click=confirmar_cancelamento)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        page.dialog = dialogo
        dialogo.open = True
        page.update()
    
    # Funções para o calendário de reservas
    def criar_reserva_no_calendario(quarto_numero: int, data_inicio: datetime):
        # Obter a lista de clientes para o dropdown
        clientes = gerenciador.listar_clientes()
        if not clientes:
            mostrar_snackbar("Não há clientes cadastrados. Cadastre um cliente primeiro.")
            return
        
        # Configurar datas iniciais
        data_check_in_cal = data_inicio
        data_check_out_cal = data_inicio + timedelta(days=1)
        
        # Dropdown de clientes
        dropdown_clientes_cal = ft.Dropdown(
            label="Cliente",
            options=[ft.dropdown.Option(key=c.id, text=c.nome) for c in clientes],
            value=clientes[0].id
        )
        
        # Textos para exibir as datas
        texto_check_in_cal = ft.Text(f"Check-in: {formatar_data(data_check_in_cal)}")
        texto_check_out_cal = ft.Text(f"Check-out: {formatar_data(data_check_out_cal)}")
        
        # Referências para as datas
        ref_data_check_in = ft.Ref[datetime]()
        ref_data_check_in.current = data_check_in_cal
        
        ref_data_check_out = ft.Ref[datetime]()
        ref_data_check_out.current = data_check_out_cal
        
        def selecionar_data_check_in_cal(e):
            def handle_date_picker_change(e):
                ref_data_check_in.current = e.control.value
                texto_check_in_cal.value = f"Check-in: {formatar_data(ref_data_check_in.current)}"
                page.update()
            
            # Abrir o DatePicker
            page.open(
                ft.DatePicker(
                    first_date=datetime.now(),
                    last_date=datetime(year=datetime.now().year + 5, month=12, day=31),
                    current_date=ref_data_check_in.current,
                    on_change=handle_date_picker_change,
                )
            )
        
        def selecionar_data_check_out_cal(e):
            def handle_date_picker_change(e):
                ref_data_check_out.current = e.control.value
                texto_check_out_cal.value = f"Check-out: {formatar_data(ref_data_check_out.current)}"
                page.update()
            
            # Abrir o DatePicker
            page.open(
                ft.DatePicker(
                    first_date=datetime.now(),
                    last_date=datetime(year=datetime.now().year + 5, month=12, day=31),
                    current_date=ref_data_check_out.current,
                    on_change=handle_date_picker_change,
                )
            )
        
        def fechar_dialogo(e):
            dialogo.open = False
            page.update()
        
        def salvar_reserva_cal(e):
            cliente_id = dropdown_clientes_cal.value
            
            # Converter datas para string no formato DD-MM-YYYY
            check_in = formatar_data(ref_data_check_in.current)
            check_out = formatar_data(ref_data_check_out.current)
            
            # Verificar se check-out é posterior a check-in
            if ref_data_check_out.current <= ref_data_check_in.current:
                mostrar_snackbar("A data de check-out deve ser posterior à data de check-in!")
                return
            
            reserva = gerenciador.criar_reserva(cliente_id, quarto_numero, check_in, check_out)
            
            if reserva:
                mostrar_snackbar("Reserva criada com sucesso!")
                atualizar_calendario()
                fechar_dialogo(e)
            else:
                mostrar_snackbar("Não foi possível criar a reserva. Verifique a disponibilidade do quarto nas datas selecionadas.")
        
        # Criar o diálogo
        dialogo = ft.AlertDialog(
            title=ft.Text(f"Nova Reserva - Quarto {quarto_numero}"),
            content=ft.Column([
                dropdown_clientes_cal,
                ft.Row([
                    ft.Column([
                        ft.Text("Check-in:"),
                        texto_check_in_cal,
                        ft.ElevatedButton(
                            "Selecionar Data",
                            icon=ft.Icons.CALENDAR_MONTH,
                            on_click=selecionar_data_check_in_cal
                        )
                    ]),
                    ft.Column([
                        ft.Text("Check-out:"),
                        texto_check_out_cal,
                        ft.ElevatedButton(
                            "Selecionar Data",
                            icon=ft.Icons.CALENDAR_MONTH,
                            on_click=selecionar_data_check_out_cal
                        )
                    ])
                ])
            ], tight=True, spacing=20, width=400),
            actions=[
                ft.TextButton("Cancelar", on_click=fechar_dialogo),
                ft.TextButton("Salvar", on_click=salvar_reserva_cal)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        page.dialog = dialogo
        dialogo.open = True
        page.update()
    
    def obter_dias_do_mes(ano: int, mes: int) -> int:
        """Retorna o número de dias em um mês específico"""
        return calendar.monthrange(ano, mes)[1]
    
    def obter_reservas_do_periodo(data_inicio: datetime, data_fim: datetime) -> Dict[int, List[Tuple[Reserva, str, str]]]:
        """
        Retorna um dicionário com as reservas do período agrupadas por número de quarto
        Cada item da lista é uma tupla (reserva, data_inicio_formatada, data_fim_formatada)
        """
        reservas_por_quarto = {}
        
        # Inicializar o dicionário com listas vazias para cada quarto
        for quarto in gerenciador.listar_quartos():
            reservas_por_quarto[quarto.numero] = []
        
        # Filtrar reservas que se sobrepõem ao período
        for reserva in gerenciador.listar_reservas():
            if reserva.status == "Cancelada":
                continue
                
            try:
                reserva_check_in = datetime.strptime(reserva.check_in, "%d-%m-%Y")
                reserva_check_out = datetime.strptime(reserva.check_out, "%d-%m-%Y")
                
                # Verificar se a reserva se sobrepõe ao período
                if not (reserva_check_out <= data_inicio or reserva_check_in >= data_fim):
                    # Calcular as datas de início e fim dentro do período visível
                    inicio_visivel = max(reserva_check_in, data_inicio)
                    fim_visivel = min(reserva_check_out, data_fim)
                    
                    # Adicionar à lista do quarto correspondente
                    if reserva.quarto_numero in reservas_por_quarto:
                        reservas_por_quarto[reserva.quarto_numero].append(
                            (reserva, inicio_visivel, fim_visivel)
                        )
            except ValueError:
                # Ignorar reservas com formato de data inválido
                continue
        
        return reservas_por_quarto
    
    def criar_bloco_reserva(reserva: Reserva, data_inicio: datetime, data_fim: datetime, largura_dia: float) -> ft.Container:
        """Cria um bloco visual para representar uma reserva no calendário"""
        cliente = gerenciador.obter_cliente_por_id(reserva.cliente_id)
        nome_cliente = cliente.nome if cliente else "Cliente desconhecido"
        
        # Determinar a cor com base no status
        cores_status = {
            "Confirmada": ft.colors.GREEN,
            "Pendente": ft.colors.ORANGE,
            "Concluída": ft.colors.BLUE,
            "Cancelada": ft.colors.RED  # Não deve aparecer, mas por precaução
        }
        cor_fundo = cores_status.get(reserva.status, ft.colors.GREY)
        
        # Calcular a posição e largura do bloco
        inicio = datetime.strptime(reserva.check_in, "%d-%m-%Y")
        fim = datetime.strptime(reserva.check_out, "%d-%m-%Y")
        
        # Ajustar para o período visível
        inicio_visivel = max(inicio, data_inicio)
        fim_visivel = min(fim, data_fim)
        
        # Calcular o deslocamento (em dias) desde o início do período visível
        deslocamento_dias = (inicio_visivel - data_inicio).days
        # Calcular a largura (em dias)
        largura_dias = (fim_visivel - inicio_visivel).days
        if largura_dias < 1:
            largura_dias = 1  # Garantir que a reserva seja visível mesmo se for apenas um dia
        
        # Criar o container para a reserva
        container = ft.Container(
            content=ft.Column([
                ft.Text(
                    nome_cliente,
                    size=12,
                    color=ft.colors.WHITE,
                    overflow=ft.TextOverflow.ELLIPSIS
                ),
                ft.Text(
                    f"{reserva.check_in} - {reserva.check_out}",
                    size=10,
                    color=ft.colors.WHITE,
                    overflow=ft.TextOverflow.ELLIPSIS
                )
            ], spacing=2, tight=True),
            bgcolor=cor_fundo,
            border_radius=5,
            padding=5,
            width=largura_dias * largura_dia,
            margin=ft.margin.only(left=deslocamento_dias * largura_dia),
            on_click=lambda e, r=reserva: editar_reserva(r)
        )
        
        return container
    
    def atualizar_calendario():
        """Atualiza a visualização do calendário de reservas"""
        # Obter o ano e mês atuais do calendário
        ano = data_calendario.current.year
        mes = data_calendario.current.month
        
        # Determinar o primeiro e último dia do mês
        primeiro_dia = datetime(ano, mes, 1)
        ultimo_dia = datetime(ano, mes, obter_dias_do_mes(ano, mes))
        
        # Criar o cabeçalho com o mês e ano
        cabecalho_mes = ft.Text(
            f"{calendar.month_name[mes]} {ano}",
            size=24,
            weight=ft.FontWeight.BOLD
        )
        
        # Botões para navegar entre os meses
        def mes_anterior(e):
            if data_calendario.current.month == 1:
                data_calendario.current = datetime(data_calendario.current.year - 1, 12, 1)
            else:
                data_calendario.current = datetime(data_calendario.current.year, data_calendario.current.month - 1, 1)
            atualizar_calendario()
        
        def mes_seguinte(e):
            if data_calendario.current.month == 12:
                data_calendario.current = datetime(data_calendario.current.year + 1, 1, 1)
            else:
                data_calendario.current = datetime(data_calendario.current.year, data_calendario.current.month + 1, 1)
            atualizar_calendario()
        
        botao_anterior = ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            on_click=mes_anterior,
            tooltip="Mês anterior"
        )
        
        botao_seguinte = ft.IconButton(
            icon=ft.Icons.ARROW_FORWARD,
            on_click=mes_seguinte,
            tooltip="Mês seguinte"
        )
        
        botao_hoje = ft.ElevatedButton(
            "Hoje",
            on_click=lambda e: (setattr(data_calendario, "current", datetime.now()), atualizar_calendario())
        )
        
        # Criar o cabeçalho com os dias do mês
        dias_cabecalho = ft.Row(spacing=0, tight=True)
        
        # Largura de cada coluna de dia (em pixels)
        largura_dia = 40
        
        # Adicionar coluna para os nomes dos quartos
        dias_cabecalho.controls.append(
            ft.Container(
                content=ft.Text("Quartos", weight=ft.FontWeight.BOLD),
                width=100,
                height=40,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.BLUE_100,
                border=ft.border.all(1, ft.colors.BLUE_200)
            )
        )
        
        # Adicionar colunas para cada dia do mês
        for dia in range(1, obter_dias_do_mes(ano, mes) + 1):
            data = datetime(ano, mes, dia)
            # Destacar o dia atual
            cor_fundo = ft.colors.BLUE_200 if data.date() == datetime.now().date() else ft.colors.BLUE_100
            
            dias_cabecalho.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            calendar.day_abbr[data.weekday()],
                            size=10,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.Text(
                            str(dia),
                            size=14,
                            weight=ft.FontWeight.BOLD
                        )
                    ], spacing=2, alignment=ft.MainAxisAlignment.CENTER),
                    width=largura_dia,
                    height=40,
                    alignment=ft.alignment.center,
                    bgcolor=cor_fundo,
                    border=ft.border.all(1, ft.colors.BLUE_200)
                )
            )
        
        # Obter as reservas para o período
        reservas_por_quarto = obter_reservas_do_periodo(primeiro_dia, ultimo_dia + timedelta(days=1))
        
        # Criar as linhas para cada quarto
        linhas_quartos = ft.Column(spacing=0, tight=True)
        
        for quarto in sorted(gerenciador.listar_quartos(), key=lambda q: q.numero):
            # Criar a linha para o quarto
            linha_quarto = ft.Row(spacing=0, tight=True)
            
            # Adicionar o nome do quarto
            linha_quarto.controls.append(
                ft.Container(
                    content=ft.Text(f"Quarto {quarto.numero}\n{quarto.tipo}", size=12),
                    width=100,
                    height=50,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.GREY_100,
                    border=ft.border.all(1, ft.colors.GREY_300)
                )
            )
            
            # Criar o container para os dias do mês
            container_dias = ft.Container(
                content=ft.Stack(
                    [
                        # Fundo com grid de dias
                        ft.Row(
                            [
                                ft.Container(
                                    width=largura_dia,
                                    height=50,
                                    border=ft.border.all(1, ft.colors.GREY_300),
                                    on_click=lambda e, q=quarto.numero, d=datetime(ano, mes, dia): criar_reserva_no_calendario(q, d)
                                )
                                for dia in range(1, obter_dias_do_mes(ano, mes) + 1)
                            ],
                            spacing=0,
                            tight=True
                        ),
                        # Reservas para este quarto
                        ft.Stack(
                            [
                                criar_bloco_reserva(reserva, primeiro_dia, ultimo_dia + timedelta(days=1), largura_dia)
                                for reserva, _, _ in reservas_por_quarto.get(quarto.numero, [])
                            ]
                        )
                    ]
                ),
                width=largura_dia * obter_dias_do_mes(ano, mes),
                height=50
            )
            
            linha_quarto.controls.append(container_dias)
            linhas_quartos.controls.append(linha_quarto)
        
        # Criar o scroll container para o calendário
        calendario_scroll = ft.Container(
            content=ft.Column([
                ft.Row([
                    botao_anterior,
                    cabecalho_mes,
                    botao_seguinte,
                    botao_hoje
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    content=ft.Column([
                        dias_cabecalho,
                        linhas_quartos
                    ], spacing=0, tight=True),
                    border_radius=10,
                    border=ft.border.all(2, ft.colors.BLUE_400),
                    clip_behavior=ft.ClipBehavior.HARD_EDGE
                )
            ]),
            expand=True,
            padding=20,
            scroll=ft.ScrollMode.ALWAYS
        )
        
        # Atualizar o conteúdo principal
        conteudo_principal.content = calendario_scroll
        page.update()
    
    # Funções de navegação
    def navegar_para(tela):
        tela_atual.current = tela
        
        if tela == "inicial":
            mostrar_tela_inicial()
        elif tela == "clientes":
            mostrar_tela_clientes()
        elif tela == "novo_cliente":
            mostrar_formulario_cliente()
        elif tela == "nova_reserva":
            mostrar_formulario_reserva()
        elif tela == "reservas":
            mostrar_tela_reservas()
        elif tela == "calendario":
            atualizar_calendario()
    
    # Funções para mostrar telas
    def mostrar_tela_inicial():
        atualizar_lista_quartos()
        
        conteudo_principal.content = ft.Column([
            ft.Row([
                ft.Text("Quartos Disponíveis", size=24, weight=ft.FontWeight.BOLD)
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                ft.ElevatedButton(
                    text="Adicionar Novo Quarto",
                    icon=ft.Icons.ADD,
                    on_click=mostrar_dialogo_novo_quarto
                )
            ], alignment=ft.MainAxisAlignment.CENTER),
            lista_quartos
        ], alignment=ft.MainAxisAlignment.START, expand=True)
        
        page.update()
    
    def mostrar_tela_clientes():
        atualizar_lista_clientes()
        
        conteudo_principal.content = ft.Column([
            ft.Row([
                ft.Text("Gerenciamento de Clientes", size=24, weight=ft.FontWeight.BOLD)
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                ft.ElevatedButton(
                    text="Adicionar Novo Cliente",
                    icon=ft.Icons.PERSON_ADD,
                    on_click=lambda e: navegar_para("novo_cliente")
                )
            ], alignment=ft.MainAxisAlignment.CENTER),
            lista_clientes
        ], alignment=ft.MainAxisAlignment.START, expand=True)
        
        page.update()
    
    def mostrar_formulario_cliente():
        # Limpar campos se não estiver editando
        if not cliente_selecionado.current:
            campo_nome.value = ""
            campo_telefone.value = ""
            campo_email.value = ""
        
        botao_salvar = ft.ElevatedButton(
            text="Salvar Cliente",
            icon=ft.Icons.SAVE,
            on_click=salvar_cliente
        )
        
        botao_cancelar = ft.OutlinedButton(
            text="Cancelar",
            on_click=lambda e: navegar_para("clientes")
        )
        
        conteudo_principal.content = ft.Column([
            ft.Row([
                ft.Text(
                    "Novo Cliente" if not cliente_selecionado.current else "Editar Cliente",
                    size=24,
                    weight=ft.FontWeight.BOLD
                )
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(
                content=ft.Column([
                    campo_nome,
                    campo_telefone,
                    campo_email,
                    ft.Row([
                        botao_cancelar,
                        botao_salvar
                    ], alignment=ft.MainAxisAlignment.END)
                ], spacing=20),
                padding=20,
                width=400
            )
        ], alignment=ft.MainAxisAlignment.CENTER, expand=True)
        
        page.update()
    
    def mostrar_formulario_reserva():
        # Atualizar dropdowns
        atualizar_dropdown_clientes()
        
        # Inicializar datas
        data_check_in.current = datetime.now()
        data_check_out.current = datetime.now() + timedelta(days=1)
        
        # Atualizar textos
        texto_check_in.value = f"Check-in: {formatar_data(data_check_in.current)}"
        texto_check_out.value = f"Check-out: {formatar_data(data_check_out.current)}"
        
        # Atualizar quartos disponíveis para as datas selecionadas
        atualizar_dropdown_quartos()
        
        botao_salvar = ft.ElevatedButton(
            text="Fazer Reserva",
            icon=ft.Icons.BOOKMARK_ADD,
            on_click=salvar_reserva
        )
        
        botao_cancelar = ft.OutlinedButton(
            text="Cancelar",
            on_click=lambda e: navegar_para("reservas")
        )
        
        conteudo_principal.content = ft.Column([
            ft.Row([
                ft.Text("Nova Reserva", size=24, weight=ft.FontWeight.BOLD)
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(
                content=ft.Column([
                    dropdown_clientes,
                    ft.Row([
                        ft.Column([
                            ft.Text("Check-in:"),
                            texto_check_in,
                            ft.ElevatedButton(
                                "Selecionar Data",
                                icon=ft.Icons.CALENDAR_MONTH,
                                on_click=selecionar_data_check_in
                            )
                        ]),
                        ft.Column([
                            ft.Text("Check-out:"),
                            texto_check_out,
                            ft.ElevatedButton(
                                "Selecionar Data",
                                icon=ft.Icons.CALENDAR_MONTH,
                                on_click=selecionar_data_check_out
                            )
                        ])
                    ]),
                    ft.Text("Quartos disponíveis para o período selecionado:", weight=ft.FontWeight.BOLD),
                    dropdown_quartos,
                    ft.Row([
                        botao_cancelar,
                        botao_salvar
                    ], alignment=ft.MainAxisAlignment.END)
                ], spacing=20),
                padding=20,
                width=500
            )
        ], alignment=ft.MainAxisAlignment.CENTER, expand=True)
        
        page.update()
    
    def mostrar_tela_reservas():
        atualizar_lista_reservas()
        
        conteudo_principal.content = ft.Column([
            ft.Row([
                ft.Text("Gerenciamento de Reservas", size=24, weight=ft.FontWeight.BOLD)
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                ft.ElevatedButton(
                    text="Nova Reserva",
                    icon=ft.Icons.ADD,
                    on_click=lambda e: navegar_para("nova_reserva")
                )
            ], alignment=ft.MainAxisAlignment.CENTER),
            lista_reservas
        ], alignment=ft.MainAxisAlignment.START, expand=True)
        
        page.update()
    
    # Barra de navegação
    barra_navegacao = ft.AppBar(
        title=ft.Text("Refúgio dos Sonhos"),
        center_title=True,
        bgcolor=ft.Colors.BLUE_700,
        actions=[
            ft.IconButton(
                icon=ft.Icons.HOME,
                tooltip="Tela Inicial",
                on_click=lambda e: navegar_para("inicial")
            ),
            ft.IconButton(
                icon=ft.Icons.PERSON,
                tooltip="Gerenciar Clientes",
                on_click=lambda e: navegar_para("clientes")
            ),
            ft.IconButton(
                icon=ft.Icons.BOOKMARK_ADD,
                tooltip="Fazer Reserva",
                on_click=lambda e: navegar_para("nova_reserva")
            ),
            ft.IconButton(
                icon=ft.Icons.LIST_ALT,
                tooltip="Ver Reservas",
                on_click=lambda e: navegar_para("reservas")
            ),
            ft.IconButton(
                icon=ft.Icons.CALENDAR_VIEW_MONTH,
                tooltip="Calendário de Reservas",
                on_click=lambda e: navegar_para("calendario")
            ),
        ]
    )
    
    # Configurar a página
    page.appbar = barra_navegacao
    page.add(conteudo_principal)
    
    # Iniciar com a tela inicial
    navegar_para("inicial")


ft.app(target=main)
