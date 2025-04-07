import flet as ft
import json
import uuid
from datetime import datetime
import os
from typing import List, Dict, Optional, Any

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
        
        if not quarto.disponivel:
            return None
        
        # Verificar se o quarto está disponível nas datas solicitadas
        if not self._verificar_disponibilidade(quarto_numero, check_in, check_out):
            return None
        
        reserva = Reserva(cliente_id, quarto_numero, check_in, check_out)
        self._reservas.append(reserva)
        
        # Atualizar disponibilidade do quarto
        quarto.disponivel = False
        
        self._salvar_dados()
        return reserva
    
    def _verificar_disponibilidade(self, quarto_numero: int, check_in: str, check_out: str) -> bool:
        # Converter strings para objetos datetime
        try:
            data_check_in = datetime.strptime(check_in, "%Y-%m-%d")
            data_check_out = datetime.strptime(check_out, "%Y-%m-%d")
        except ValueError:
            return False
        
        # Verificar se check_out é posterior a check_in
        if data_check_out <= data_check_in:
            return False
        
        # Verificar se há sobreposição com outras reservas
        for reserva in self._reservas:
            if reserva.quarto_numero == quarto_numero and reserva.status != "Cancelada":
                reserva_check_in = datetime.strptime(reserva.check_in, "%Y-%m-%d")
                reserva_check_out = datetime.strptime(reserva.check_out, "%Y-%m-%d")
                
                # Verificar sobreposição
                if (data_check_in < reserva_check_out and data_check_out > reserva_check_in):
                    return False
        
        return True
    
    def obter_reserva_por_id(self, reserva_id: str) -> Optional[Reserva]:
        for reserva in self._reservas:
            if reserva.id == reserva_id:
                return reserva
        return None
    
    def atualizar_reserva(self, reserva_id: str, check_in: str, check_out: str, status: str) -> bool:
        reserva = self.obter_reserva_por_id(reserva_id)
        if reserva:
            # Se estamos cancelando a reserva, liberar o quarto
            if status == "Cancelada" and reserva.status != "Cancelada":
                quarto = self.obter_quarto_por_numero(reserva.quarto_numero)
                if quarto:
                    quarto.disponivel = True
            
            reserva.check_in = check_in
            reserva.check_out = check_out
            reserva.status = status
            self._salvar_dados()
            return True
        return False
    
    def cancelar_reserva(self, reserva_id: str) -> bool:
        return self.atualizar_reserva(reserva_id, 
                                     self.obter_reserva_por_id(reserva_id).check_in,
                                     self.obter_reserva_por_id(reserva_id).check_out,
                                     "Cancelada")
    
    def listar_clientes(self) -> List[Cliente]:
        return self._clientes
    
    def listar_quartos(self) -> List[Quarto]:
        return self._quartos
    
    def listar_quartos_disponiveis(self) -> List[Quarto]:
        return [q for q in self._quartos if q.disponivel]
    
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


# Interface gráfica com Flet
class HotelApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Refúgio dos Sonhos - Sistema de Gerenciamento"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window_width = 1000
        self.page.window_height = 800
        self.page.padding = 20
        
        self.gerenciador = GerenciadorDeReservas()
        
        # Elementos da interface
        self.tela_atual = "inicial"
        
        # Elementos para a tela inicial
        self.lista_quartos = ft.ListView(expand=True, spacing=10, padding=20)
        
        # Elementos para o formulário de cliente
        self.campo_nome = ft.TextField(label="Nome", width=300)
        self.campo_telefone = ft.TextField(label="Telefone", width=300)
        self.campo_email = ft.TextField(label="E-mail", width=300)
        self.cliente_selecionado = None
        
        # Elementos para a lista de clientes
        self.lista_clientes = ft.ListView(expand=True, spacing=10, padding=20)
        
        # Elementos para o formulário de reserva
        self.dropdown_clientes = ft.Dropdown(label="Cliente", width=300)
        self.dropdown_quartos = ft.Dropdown(label="Quarto", width=300)
        self.campo_check_in = ft.TextField(label="Check-in (AAAA-MM-DD)", width=300)
        self.campo_check_out = ft.TextField(label="Check-out (AAAA-MM-DD)", width=300)
        
        # Elementos para a lista de reservas
        self.lista_reservas = ft.ListView(expand=True, spacing=10, padding=20)
        
        # Configurar a interface
        self.configurar_interface()
    
    def configurar_interface(self):
        # Barra de navegação
        barra_navegacao = ft.AppBar(
            title=ft.Text("Refúgio dos Sonhos"),
            center_title=True,
            bgcolor=ft.colors.BLUE_700,
            actions=[
                ft.IconButton(
                    icon=ft.icons.HOME,
                    tooltip="Tela Inicial",
                    on_click=lambda _: self.navegar_para("inicial")
                ),
                ft.IconButton(
                    icon=ft.icons.PERSON,
                    tooltip="Gerenciar Clientes",
                    on_click=lambda _: self.navegar_para("clientes")
                ),
                ft.IconButton(
                    icon=ft.icons.BOOK_ONLINE,
                    tooltip="Fazer Reserva",
                    on_click=lambda _: self.navegar_para("nova_reserva")
                ),
                ft.IconButton(
                    icon=ft.icons.LIST,
                    tooltip="Ver Reservas",
                    on_click=lambda _: self.navegar_para("reservas")
                ),
            ]
        )
        
        self.page.appbar = barra_navegacao
        self.navegar_para("inicial")
    
    def navegar_para(self, tela: str):
        self.tela_atual = tela
        
        if tela == "inicial":
            self.mostrar_tela_inicial()
        elif tela == "clientes":
            self.mostrar_tela_clientes()
        elif tela == "novo_cliente":
            self.mostrar_formulario_cliente()
        elif tela == "nova_reserva":
            self.mostrar_formulario_reserva()
        elif tela == "reservas":
            self.mostrar_tela_reservas()
        
        self.page.update()
    
    def mostrar_tela_inicial(self):
        self.atualizar_lista_quartos()
        
        self.page.controls = [
            ft.Column([
                ft.Row([
                    ft.Text("Quartos Disponíveis", size=24, weight=ft.FontWeight.BOLD)
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    ft.ElevatedButton(
                        text="Adicionar Novo Quarto",
                        icon=ft.icons.ADD,
                        on_click=self.mostrar_dialogo_novo_quarto
                    )
                ], alignment=ft.MainAxisAlignment.CENTER),
                self.lista_quartos
            ], alignment=ft.MainAxisAlignment.START, expand=True)
        ]
    
    def atualizar_lista_quartos(self):
        self.lista_quartos.controls = []
        
        for quarto in self.gerenciador.listar_quartos():
            card_quarto = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.HOTEL),
                            title=ft.Text(f"Quarto {quarto.numero} - {quarto.tipo}"),
                            subtitle=ft.Text(f"Preço: R$ {quarto.preco:.2f} / diária"),
                            trailing=ft.Chip(
                                label=ft.Text("Disponível" if quarto.disponivel else "Ocupado"),
                                bgcolor=ft.colors.GREEN if quarto.disponivel else ft.colors.RED,
                            ),
                        ),
                        ft.Row([
                            ft.TextButton("Editar", on_click=lambda e, q=quarto: self.mostrar_dialogo_editar_quarto(e, q)),
                            ft.TextButton("Excluir", on_click=lambda e, q=quarto: self.excluir_quarto(e, q))
                        ], alignment=ft.MainAxisAlignment.END)
                    ]),
                    padding=10
                )
            )
            
            self.lista_quartos.controls.append(card_quarto)
    
    def mostrar_dialogo_novo_quarto(self, e):
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
            self.page.dialog.open = False
            self.page.update()
        
        def salvar_quarto(e):
            try:
                numero = int(campo_numero.value)
                tipo = dropdown_tipo.value
                preco = float(campo_preco.value)
                
                # Verificar se já existe um quarto com este número
                if self.gerenciador.obter_quarto_por_numero(numero):
                    self.mostrar_snackbar("Já existe um quarto com este número!")
                    return
                
                quarto = Quarto(numero, tipo, preco)
                self.gerenciador.adicionar_quarto(quarto)
                
                self.mostrar_snackbar("Quarto adicionado com sucesso!")
                self.atualizar_lista_quartos()
                fechar_dialogo(e)
            except ValueError:
                self.mostrar_snackbar("Por favor, preencha todos os campos corretamente!")
        
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
        
        self.page.dialog = dialogo
        dialogo.open = True
        self.page.update()
    
    def mostrar_dialogo_editar_quarto(self, e, quarto):
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
            self.page.dialog.open = False
            self.page.update()
        
        def salvar_quarto(e):
            try:
                tipo = dropdown_tipo.value
                preco = float(campo_preco.value)
                disponivel = switch_disponivel.value
                
                self.gerenciador.atualizar_quarto(quarto.numero, tipo, preco, disponivel)
                
                self.mostrar_snackbar("Quarto atualizado com sucesso!")
                self.atualizar_lista_quartos()
                fechar_dialogo(e)
            except ValueError:
                self.mostrar_snackbar("Por favor, preencha todos os campos corretamente!")
        
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
        
        self.page.dialog = dialogo
        dialogo.open = True
        self.page.update()
    
    def excluir_quarto(self, e, quarto):
        def confirmar_exclusao(e):
            self.gerenciador.remover_quarto(quarto.numero)
            self.mostrar_snackbar("Quarto excluído com sucesso!")
            self.atualizar_lista_quartos()
            fechar_dialogo(e)
        
        def fechar_dialogo(e):
            self.page.dialog.open = False
            self.page.update()
        
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
        
        self.page.dialog = dialogo
        dialogo.open = True
        self.page.update()
    
    def mostrar_tela_clientes(self):
        self.atualizar_lista_clientes()
        
        self.page.controls = [
            ft.Column([
                ft.Row([
                    ft.Text("Gerenciamento de Clientes", size=24, weight=ft.FontWeight.BOLD)
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    ft.ElevatedButton(
                        text="Adicionar Novo Cliente",
                        icon=ft.icons.PERSON_ADD,
                        on_click=lambda _: self.navegar_para("novo_cliente")
                    )
                ], alignment=ft.MainAxisAlignment.CENTER),
                self.lista_clientes
            ], alignment=ft.MainAxisAlignment.START, expand=True)
        ]
    
    def atualizar_lista_clientes(self):
        self.lista_clientes.controls = []
        
        for cliente in self.gerenciador.listar_clientes():
            card_cliente = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.PERSON),
                            title=ft.Text(cliente.nome),
                            subtitle=ft.Column([
                                ft.Text(f"Telefone: {cliente.telefone}"),
                                ft.Text(f"E-mail: {cliente.email}")
                            ])
                        ),
                        ft.Row([
                            ft.TextButton("Editar", on_click=lambda e, c=cliente: self.editar_cliente(e, c)),
                            ft.TextButton("Excluir", on_click=lambda e, c=cliente: self.excluir_cliente(e, c))
                        ], alignment=ft.MainAxisAlignment.END)
                    ]),
                    padding=10
                )
            )
            
            self.lista_clientes.controls.append(card_cliente)
    
    def mostrar_formulario_cliente(self):
        # Limpar campos se não estiver editando
        if not self.cliente_selecionado:
            self.campo_nome.value = ""
            self.campo_telefone.value = ""
            self.campo_email.value = ""
        
        botao_salvar = ft.ElevatedButton(
            text="Salvar Cliente",
            icon=ft.icons.SAVE,
            on_click=self.salvar_cliente
        )
        
        botao_cancelar = ft.OutlinedButton(
            text="Cancelar",
            on_click=lambda _: self.navegar_para("clientes")
        )
        
        self.page.controls = [
            ft.Column([
                ft.Row([
                    ft.Text(
                        "Novo Cliente" if not self.cliente_selecionado else "Editar Cliente",
                        size=24,
                        weight=ft.FontWeight.BOLD
                    )
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    content=ft.Column([
                        self.campo_nome,
                        self.campo_telefone,
                        self.campo_email,
                        ft.Row([
                            botao_cancelar,
                            botao_salvar
                        ], alignment=ft.MainAxisAlignment.END)
                    ], spacing=20),
                    padding=20,
                    width=400
                )
            ], alignment=ft.MainAxisAlignment.CENTER, expand=True)
        ]
    
    def salvar_cliente(self, e):
        nome = self.campo_nome.value
        telefone = self.campo_telefone.value
        email = self.campo_email.value
        
        if not nome or not telefone or not email:
            self.mostrar_snackbar("Por favor, preencha todos os campos!")
            return
        
        if self.cliente_selecionado:
            # Atualizar cliente existente
            self.gerenciador.atualizar_cliente(
                self.cliente_selecionado.id,
                nome,
                telefone,
                email
            )
            self.mostrar_snackbar("Cliente atualizado com sucesso!")
        else:
            # Criar novo cliente
            cliente = Cliente(nome, telefone, email)
            self.gerenciador.adicionar_cliente(cliente)
            self.mostrar_snackbar("Cliente adicionado com sucesso!")
        
        self.cliente_selecionado = None
        self.navegar_para("clientes")
    
    def editar_cliente(self, e, cliente):
        self.cliente_selecionado = cliente
        self.campo_nome.value = cliente.nome
        self.campo_telefone.value = cliente.telefone
        self.campo_email.value = cliente.email
        
        self.navegar_para("novo_cliente")
    
    def excluir_cliente(self, e, cliente):
        def confirmar_exclusao(e):
            self.gerenciador.remover_cliente(cliente.id)
            self.mostrar_snackbar("Cliente excluído com sucesso!")
            self.atualizar_lista_clientes()
            fechar_dialogo(e)
        
        def fechar_dialogo(e):
            self.page.dialog.open = False
            self.page.update()
        
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
        
        self.page.dialog = dialogo
        dialogo.open = True
        self.page.update()
    
    def mostrar_formulario_reserva(self):
        # Atualizar dropdowns
        self.atualizar_dropdown_clientes()
        self.atualizar_dropdown_quartos()
        
        # Limpar campos
        self.campo_check_in.value = ""
        self.campo_check_out.value = ""
        
        botao_salvar = ft.ElevatedButton(
            text="Fazer Reserva",
            icon=ft.icons.BOOK_ONLINE,
            on_click=self.salvar_reserva
        )
        
        botao_cancelar = ft.OutlinedButton(
            text="Cancelar",
            on_click=lambda _: self.navegar_para("reservas")
        )
        
        self.page.controls = [
            ft.Column([
                ft.Row([
                    ft.Text("Nova Reserva", size=24, weight=ft.FontWeight.BOLD)
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    content=ft.Column([
                        self.dropdown_clientes,
                        self.dropdown_quartos,
                        self.campo_check_in,
                        self.campo_check_out,
                        ft.Row([
                            botao_cancelar,
                            botao_salvar
                        ], alignment=ft.MainAxisAlignment.END)
                    ], spacing=20),
                    padding=20,
                    width=400
                )
            ], alignment=ft.MainAxisAlignment.CENTER, expand=True)
        ]
    
    def atualizar_dropdown_clientes(self):
        self.dropdown_clientes.options = []
        
        for cliente in self.gerenciador.listar_clientes():
            self.dropdown_clientes.options.append(
                ft.dropdown.Option(key=cliente.id, text=cliente.nome)
            )
        
        if self.dropdown_clientes.options:
            self.dropdown_clientes.value = self.dropdown_clientes.options[0].key
    
    def atualizar_dropdown_quartos(self):
        self.dropdown_quartos.options = []
        
        for quarto in self.gerenciador.listar_quartos_disponiveis():
            self.dropdown_quartos.options.append(
                ft.dropdown.Option(
                    key=str(quarto.numero),
                    text=f"Quarto {quarto.numero} - {quarto.tipo} - R$ {quarto.preco:.2f}"
                )
            )
        
        if self.dropdown_quartos.options:
            self.dropdown_quartos.value = self.dropdown_quartos.options[0].key
    
    def salvar_reserva(self, e):
        cliente_id = self.dropdown_clientes.value
        quarto_numero = int(self.dropdown_quartos.value) if self.dropdown_quartos.value else None
        check_in = self.campo_check_in.value
        check_out = self.campo_check_out.value
        
        if not cliente_id or not quarto_numero or not check_in or not check_out:
            self.mostrar_snackbar("Por favor, preencha todos os campos!")
            return
        
        # Validar formato das datas
        try:
            datetime.strptime(check_in, "%Y-%m-%d")
            datetime.strptime(check_out, "%Y-%m-%d")
        except ValueError:
            self.mostrar_snackbar("Formato de data inválido! Use AAAA-MM-DD")
            return
        
        reserva = self.gerenciador.criar_reserva(cliente_id, quarto_numero, check_in, check_out)
        
        if reserva:
            self.mostrar_snackbar("Reserva criada com sucesso!")
            self.navegar_para("reservas")
        else:
            self.mostrar_snackbar("Não foi possível criar a reserva. Verifique a disponibilidade do quarto nas datas selecionadas.")
    
    def mostrar_tela_reservas(self):
        self.atualizar_lista_reservas()
        
        self.page.controls = [
            ft.Column([
                ft.Row([
                    ft.Text("Gerenciamento de Reservas", size=24, weight=ft.FontWeight.BOLD)
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    ft.ElevatedButton(
                        text="Nova Reserva",
                        icon=ft.icons.ADD,
                        on_click=lambda _: self.navegar_para("nova_reserva")
                    )
                ], alignment=ft.MainAxisAlignment.CENTER),
                self.lista_reservas
            ], alignment=ft.MainAxisAlignment.START, expand=True)
        ]
    
    def atualizar_lista_reservas(self):
        self.lista_reservas.controls = []
        
        for reserva in self.gerenciador.listar_reservas():
            cliente = self.gerenciador.obter_cliente_por_id(reserva.cliente_id)
            quarto = self.gerenciador.obter_quarto_por_numero(reserva.quarto_numero)
            
            if not cliente or not quarto:
                continue
            
            cor_status = {
                "Confirmada": ft.colors.GREEN,
                "Pendente": ft.colors.ORANGE,
                "Cancelada": ft.colors.RED,
                "Concluída": ft.colors.BLUE
            }.get(reserva.status, ft.colors.GREY)
            
            card_reserva = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.BOOK_ONLINE),
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
                            ft.TextButton("Editar", on_click=lambda e, r=reserva: self.editar_reserva(e, r)),
                            ft.TextButton("Cancelar Reserva", on_click=lambda e, r=reserva: self.cancelar_reserva(e, r))
                        ], alignment=ft.MainAxisAlignment.END)
                    ]),
                    padding=10
                )
            )
            
            self.lista_reservas.controls.append(card_reserva)
    
    def editar_reserva(self, e, reserva):
        cliente = self.gerenciador.obter_cliente_por_id(reserva.cliente_id)
        quarto = self.gerenciador.obter_quarto_por_numero(reserva.quarto_numero)
        
        # Campos do formulário
        campo_cliente = ft.TextField(label="Cliente", value=cliente.nome, disabled=True)
        campo_quarto = ft.TextField(label="Quarto", value=f"{quarto.numero} - {quarto.tipo}", disabled=True)
        campo_check_in = ft.TextField(label="Check-in (AAAA-MM-DD)", value=reserva.check_in)
        campo_check_out = ft.TextField(label="Check-out (AAAA-MM-DD)", value=reserva.check_out)
        dropdown_status = ft.Dropdown(
            label="Status",
            options=[
                ft.dropdown.Option(status) for status in Reserva.STATUS
            ],
            value=reserva.status
        )
        
        def fechar_dialogo(e):
            self.page.dialog.open = False
            self.page.update()
        
        def salvar_reserva(e):
            try:
                check_in = campo_check_in.value
                check_out = campo_check_out.value
                status = dropdown_status.value
                
                # Validar formato das datas
                datetime.strptime(check_in, "%Y-%m-%d")
                datetime.strptime(check_out, "%Y-%m-%d")
                
                self.gerenciador.atualizar_reserva(reserva.id, check_in, check_out, status)
                
                self.mostrar_snackbar("Reserva atualizada com sucesso!")
                self.atualizar_lista_reservas()
                fechar_dialogo(e)
            except ValueError:
                self.mostrar_snackbar("Formato de data inválido! Use AAAA-MM-DD")
        
        # Criar o diálogo
        dialogo = ft.AlertDialog(
            title=ft.Text("Editar Reserva"),
            content=ft.Column([
                campo_cliente,
                campo_quarto,
                campo_check_in,
                campo_check_out,
                dropdown_status
            ], tight=True, spacing=20, width=400),
            actions=[
                ft.TextButton("Cancelar", on_click=fechar_dialogo),
                ft.TextButton("Salvar", on_click=salvar_reserva)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.dialog = dialogo
        dialogo.open = True
        self.page.update()
    
    def cancelar_reserva(self, e, reserva):
        def confirmar_cancelamento(e):
            self.gerenciador.cancelar_reserva(reserva.id)
            self.mostrar_snackbar("Reserva cancelada com sucesso!")
            self.atualizar_lista_reservas()
            fechar_dialogo(e)
        
        def fechar_dialogo(e):
            self.page.dialog.open = False
            self.page.update()
        
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
        
        self.page.dialog = dialogo
        dialogo.open = True
        self.page.update()
    
    def mostrar_snackbar(self, mensagem):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(mensagem),
            action="OK"
        )
        self.page.snack_bar.open = True
        self.page.update()

def main(page: ft.Page):
    app = HotelApp(page)

ft.app(target=main)
