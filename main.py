import flet as ft
import json
import uuid
from datetime import datetime, timedelta
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
    page.window_width = 1000
    page.window_height = 800
    page.padding = 20
    
    # Instanciar o gerenciador de reservas
    gerenciador = GerenciadorDeReservas()
    
    # Variáveis de estado
    tela_atual = ft.Ref[str]()
    tela_atual.current = "inicial"
    
    cliente_selecionado = ft.Ref[Cliente]()
    
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
            
            # Definir cores e ícones com base na disponibilidade
            cor_fundo = ft.Colors.GREEN_50 if disponivel else ft.Colors.RED_50
            cor_borda = ft.Colors.GREEN if disponivel else ft.Colors.RED
            icone = ft.Icons.CHECK_CIRCLE if disponivel else ft.Icons.DO_NOT_DISTURB
            status_texto = "Disponível" if disponivel else "Ocupado"
            
            # Criar um card para o quarto com visual melhorado
            card_quarto = ft.Container(
                content=ft.Row([
                    # Ícone e informações do quarto
                    ft.Row([
                        ft.Icon(
                            name=ft.Icons.KING_BED,
                            size=30,
                            color=ft.Colors.BLUE_700
                        ),
                        ft.Column([
                            ft.Text(
                                f"Quarto {quarto.numero} - {quarto.tipo}",
                                size=18,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Text(
                                f"R$ {quarto.preco:.2f} / diária",
                                size=14,
                                color=ft.Colors.GREY_700
                            )
                        ], spacing=5)
                    ], spacing=15),
                    
                    # Indicador de status
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(name=icone, color=cor_borda),
                            ft.Text(status_texto, weight=ft.FontWeight.BOLD)
                        ], spacing=5),
                        padding=ft.padding.all(8),
                        border_radius=ft.border_radius.all(15),
                        bgcolor=cor_fundo
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.all(15),
                border_radius=ft.border_radius.all(10),
                border=ft.border.all(1, cor_borda),
                margin=ft.margin.only(bottom=5),
                ink=True,  # Efeito de clique
                on_click=lambda e, q=quarto: mostrar_opcoes_quarto(q) if disponivel else None
            )
            
            lista_quartos.controls.append(card_quarto)
        
        page.update()
    
    def mostrar_opcoes_quarto(quarto):
        def fechar_dialogo(e):
            dialogo.open = False
            page.update()
        
        def fazer_reserva(e):
            fechar_dialogo(e)
            navegar_para("nova_reserva")
        
        # Criar o diálogo com opções para o quarto
        dialogo = ft.AlertDialog(
            title=ft.Text(f"Quarto {quarto.numero} - {quarto.tipo}"),
            content=ft.Column([
                ft.Text(f"Preço: R$ {quarto.preco:.2f} / diária"),
                ft.Text("O que você deseja fazer com este quarto?")
            ], tight=True, spacing=10),
            actions=[
                ft.ElevatedButton(
                    "Fazer Reserva",
                    icon=ft.Icons.BOOKMARK_ADD,
                    on_click=fazer_reserva
                ),
                ft.TextButton("Fechar", on_click=fechar_dialogo)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        page.dialog = dialogo
        dialogo.open = True
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
            
            # Determinar se os botões de ação devem estar habilitados
            # (desabilitar para reservas já canceladas ou concluídas)
            botoes_habilitados = reserva.status not in ["Cancelada", "Concluída"]
            
            card_reserva = ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        leading=ft.Icon(
                            ft.Icons.BOOKMARK,
                            color=cor_status,
                            size=30
                        ),
                        title=ft.Text(
                            f"Reserva de {cliente.nome}",
                            size=18,
                            weight=ft.FontWeight.BOLD
                        ),
                        subtitle=ft.Column([
                            ft.Text(f"Quarto: {quarto.numero} - {quarto.tipo}"),
                            ft.Text(f"Check-in: {reserva.check_in} | Check-out: {reserva.check_out}"),
                            ft.Container(
                                content=ft.Text(
                                    reserva.status,
                                    color=ft.Colors.WHITE,
                                    weight=ft.FontWeight.BOLD
                                ),
                                padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                border_radius=ft.border_radius.all(15),
                                bgcolor=cor_status,
                                margin=ft.margin.only(top=5)
                            )
                        ])
                    ),
                    ft.Row([
                        ft.ElevatedButton(
                            "Editar",
                            icon=ft.Icons.EDIT,
                            on_click=lambda e, r=reserva: editar_reserva(r),
                            disabled=not botoes_habilitados
                        ),
                        ft.ElevatedButton(
                            "Cancelar Reserva",
                            icon=ft.Icons.CANCEL,
                            on_click=lambda e, r=reserva: cancelar_reserva(r),
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.RED if botoes_habilitados else ft.Colors.GREY,
                                color=ft.Colors.WHITE
                            ),
                            disabled=not botoes_habilitados
                        )
                    ], alignment=ft.MainAxisAlignment.END, spacing=10)
                ]),
                padding=15,
                border_radius=10,
                border=ft.border.all(1, cor_status),
                margin=ft.margin.only(bottom=10)
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
        cliente_selecionado.current =  cliente
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
            # Corrigido: Garantir que o cancelamento seja processado e salvo
            if gerenciador.cancelar_reserva(reserva.id):
                mostrar_snackbar("Reserva cancelada com sucesso!")
                # Atualizar a lista de reservas imediatamente após o cancelamento
                atualizar_lista_reservas()
                fechar_dialogo(e)
            else:
                mostrar_snackbar("Erro ao cancelar a reserva!")
        
        def fechar_dialogo(e):
            dialogo.open = False
            page.update()
        
        # Criar o diálogo de confirmação com visual melhorado
        dialogo = ft.AlertDialog(
            title=ft.Text("Confirmar Cancelamento"),
            content=ft.Column([
                ft.Icon(
                    name=ft.Icons.WARNING_AMBER_ROUNDED,
                    color=ft.Colors.AMBER,
                    size=50
                ),
                ft.Text(
                    "Tem certeza que deseja cancelar esta reserva?",
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "Esta ação não pode ser desfeita.",
                    size=12,
                    color=ft.Colors.GREY,
                    text_align=ft.TextAlign.CENTER
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            actions=[
                ft.TextButton(
                    "Não",
                    on_click=fechar_dialogo
                ),
                ft.ElevatedButton(
                    "Sim, Cancelar",
                    on_click=confirmar_cancelamento,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.RED,
                        color=ft.Colors.WHITE
                    )
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        page.dialog = dialogo
        dialogo.open = True
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
    
    # Funções para mostrar telas
    def mostrar_tela_inicial():
        atualizar_lista_quartos()
        
        # Botões de ação para a tela inicial
        botoes_acao = ft.Row([
            ft.ElevatedButton(
                text="Fazer Nova Reserva",
                icon=ft.Icons.ADD_CIRCLE,
                on_click=lambda e: navegar_para("nova_reserva"),
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.BLUE_700,
                    color=ft.Colors.WHITE
                )
            ),
            ft.ElevatedButton(
                text="Gerenciar Clientes",
                icon=ft.Icons.PEOPLE,
                on_click=lambda e: navegar_para("clientes"),
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.GREEN_700,
                    color=ft.Colors.WHITE
                )
            ),
            ft.ElevatedButton(
                text="Ver Reservas",
                icon=ft.Icons.LIST_ALT,
                on_click=lambda e: navegar_para("reservas"),
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.ORANGE_700,
                    color=ft.Colors.WHITE
                )
            )
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        
        # Estatísticas rápidas
        quartos_disponiveis = len(gerenciador.listar_quartos_disponiveis())
        total_quartos = len(gerenciador.listar_quartos())
        reservas_ativas = len([r for r in gerenciador.listar_reservas() if r.status in ["Confirmada", "Pendente"]])
        
        estatisticas = ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Text("Quartos Disponíveis", size=14, color=ft.Colors.GREEN),
                    ft.Text(f"{quartos_disponiveis}/{total_quartos}", size=24, weight=ft.FontWeight.BOLD)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
                border_radius=10,
                bgcolor=ft.Colors.GREEN_50,
                width=200
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Reservas Ativas", size=14, color=ft.Colors.BLUE),
                    ft.Text(f"{reservas_ativas}", size=24, weight=ft.FontWeight.BOLD)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
                border_radius=10,
                bgcolor=ft.Colors.BLUE_50,
                width=200
            )
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        
        # Título da página com estilo melhorado
        titulo = ft.Container(
            content=ft.Text(
                "Visão Geral dos Quartos",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE
            ),
            padding=ft.padding.symmetric(vertical=15),
            border_radius=ft.border_radius.only(bottom_left=10, bottom_right=10),
            bgcolor=ft.Colors.BLUE_700,
            alignment=ft.alignment.center
        )
        
        # Subtítulo com informações
        subtitulo = ft.Container(
            content=ft.Text(
                "Clique em um quarto disponível para ver opções",
                size=16,
                italic=True,
                color=ft.Colors.GREY_700
            ),
            margin=ft.margin.only(bottom=10),
            alignment=ft.alignment.center
        )
        
        conteudo_principal.content = ft.Column([
            titulo,
            ft.Container(height=20),  # Espaçamento
            estatisticas,
            ft.Container(height=20),  # Espaçamento
            botoes_acao,
            ft.Container(height=20),  # Espaçamento
            subtitulo,
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
            on_click=salvar_reserva,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE_700,
                color=ft.Colors.WHITE
            )
        )
        
        botao_cancelar = ft.OutlinedButton(
            text="Cancelar",
            on_click=lambda e: navegar_para("reservas")
        )
        
        # Formulário centralizado e com visual melhorado
        formulario = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Informações da Reserva",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_700
                ),
                dropdown_clientes,
                ft.Container(
                    content=ft.Row([
                        ft.Column([
                            ft.Text("Check-in:", weight=ft.FontWeight.BOLD),
                            texto_check_in,
                            ft.ElevatedButton(
                                "Selecionar Data",
                                icon=ft.Icons.CALENDAR_MONTH,
                                on_click=selecionar_data_check_in
                            )
                        ]),
                        ft.Column([
                            ft.Text("Check-out:", weight=ft.FontWeight.BOLD),
                            texto_check_out,
                            ft.ElevatedButton(
                                "Selecionar Data",
                                icon=ft.Icons.CALENDAR_MONTH,
                                on_click=selecionar_data_check_out
                            )
                        ])
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    margin=ft.margin.symmetric(vertical=10)
                ),
                ft.Text(
                    "Quartos disponíveis para o período selecionado:",
                    weight=ft.FontWeight.BOLD
                ),
                dropdown_quartos,
                ft.Container(
                    content=ft.Row([
                        botao_cancelar,
                        botao_salvar
                    ], alignment=ft.MainAxisAlignment.END),
                    margin=ft.margin.only(top=20)
                )
            ], spacing=15),
            padding=30,
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLUE_200),
            bgcolor=ft.Colors.WHITE,
            width=550,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.2, ft.Colors.BLUE_GREY)
            )
        )
        
        conteudo_principal.content = ft.Column([
            ft.Container(
                content=ft.Text(
                    "Nova Reserva",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE
                ),
                padding=ft.padding.symmetric(vertical=15),
                border_radius=ft.border_radius.only(bottom_left=10, bottom_right=10),
                bgcolor=ft.Colors.BLUE_700,
                alignment=ft.alignment.center,
                margin=ft.margin.only(bottom=30)
            ),
            formulario
        ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
        
        page.update()
    
    def mostrar_tela_reservas():
        atualizar_lista_reservas()
        
        # Título da página com estilo melhorado
        titulo = ft.Container(
            content=ft.Text(
                "Gerenciamento de Reservas",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE
            ),
            padding=ft.padding.symmetric(vertical=15),
            border_radius=ft.border_radius.only(bottom_left=10, bottom_right=10),
            bgcolor=ft.Colors.BLUE_700,
            alignment=ft.alignment.center,
            margin=ft.margin.only(bottom=20)
        )
        
        # Botão para nova reserva
        botao_nova_reserva = ft.ElevatedButton(
            text="Nova Reserva",
            icon=ft.Icons.ADD,
            on_click=lambda e: navegar_para("nova_reserva"),
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN_700,
                color=ft.Colors.WHITE
            )
        )
        
        conteudo_principal.content = ft.Column([
            titulo,
            ft.Row([botao_nova_reserva], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=20),  # Espaçamento
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
        ]
    )
    
    # Configurar a página
    page.appbar = barra_navegacao
    page.add(conteudo_principal)
    
    # Iniciar com a tela inicial
    navegar_para("inicial")


ft.app(target=main)