# main.py
import flet as ft
import json
import uuid
from datetime import datetime, timedelta
import os
from typing import List, Dict, Optional, Any
import traceback # Import traceback for detailed error logging

# ==============================================================================
# Classes do modelo de dados
# (Idealmente em arquivos separados na pasta models)
# ==============================================================================
class Cliente:
    # ... (código da classe Cliente sem alterações) ...
    def __init__(self, nome: str, telefone: str, email: str, id: str = None):
        self._nome = nome
        self._telefone = telefone
        self._email = email
        self._id = id if id else str(uuid.uuid4())

    @property
    def nome(self) -> str: return self._nome
    @nome.setter
    def nome(self, valor: str) -> None: self._nome = valor
    @property
    def telefone(self) -> str: return self._telefone
    @telefone.setter
    def telefone(self, valor: str) -> None: self._telefone = valor
    @property
    def email(self) -> str: return self._email
    @email.setter
    def email(self, valor: str) -> None: self._email = valor
    @property
    def id(self) -> str: return self._id

    def to_dict(self) -> Dict[str, Any]:
        return {"nome": self._nome, "telefone": self._telefone, "email": self._email, "id": self._id}
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Cliente':
        return cls(nome=data["nome"], telefone=data["telefone"], email=data["email"], id=data["id"])

class Quarto:
    # ... (código da classe Quarto sem alterações) ...
    TIPOS = ["Single", "Double", "Suite"]
    def __init__(self, numero: int, tipo: str, preco: float, disponivel: bool = True):
        self._numero = numero
        self._tipo = tipo if tipo in self.TIPOS else "Single"
        self._preco = preco
        self._disponivel = disponivel # Flag geral (manutenção, etc.)

    @property
    def numero(self) -> int: return self._numero
    @property
    def tipo(self) -> str: return self._tipo
    @tipo.setter
    def tipo(self, valor: str) -> None:
        if valor in self.TIPOS: self._tipo = valor
    @property
    def preco(self) -> float: return self._preco
    @preco.setter
    def preco(self, valor: float) -> None:
        if valor > 0: self._preco = valor
    @property
    def disponivel(self) -> bool: return self._disponivel
    @disponivel.setter
    def disponivel(self, valor: bool) -> None: self._disponivel = valor

    def to_dict(self) -> Dict[str, Any]:
        return {"numero": self._numero, "tipo": self._tipo, "preco": self._preco, "disponivel": self._disponivel}
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Quarto':
        return cls(numero=data["numero"], tipo=data["tipo"], preco=data["preco"], disponivel=data.get("disponivel", True))

class Reserva:
    # ... (código da classe Reserva sem alterações) ...
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
    def cliente_id(self) -> str: return self._cliente_id
    @property
    def quarto_numero(self) -> int: return self._quarto_numero
    @property
    def check_in(self) -> str: return self._check_in
    @check_in.setter
    def check_in(self, valor: str) -> None: self._check_in = valor
    @property
    def check_out(self) -> str: return self._check_out
    @check_out.setter
    def check_out(self, valor: str) -> None: self._check_out = valor
    @property
    def status(self) -> str: return self._status
    @status.setter
    def status(self, valor: str) -> None:
        if valor in self.STATUS: self._status = valor
    @property
    def id(self) -> str: return self._id

    def to_dict(self) -> Dict[str, Any]:
        return {"cliente_id": self._cliente_id, "quarto_numero": self._quarto_numero, "check_in": self._check_in,
                "check_out": self._check_out, "status": self._status, "id": self._id}
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Reserva':
        return cls(cliente_id=data["cliente_id"], quarto_numero=data["quarto_numero"], check_in=data["check_in"],
                   check_out=data["check_out"], status=data["status"], id=data["id"])

# ==============================================================================
# Classe Gerenciadora
# ==============================================================================
class GerenciadorDeReservas:
    # ... (código do Gerenciador SEM ALTERAÇÕES NECESSÁRIAS para este request) ...
    def __init__(self):
        self._clientes: List[Cliente] = []
        self._quartos: List[Quarto] = []
        self._reservas: List[Reserva] = []
        self._arquivo_dados = "dados_hotel.json"
        self._carregar_dados()

    # --- Métodos Cliente ---
    def adicionar_cliente(self, cliente: Cliente) -> None:
        if not any(c.id == cliente.id or c.email == cliente.email for c in self._clientes):
            self._clientes.append(cliente); self._salvar_dados()
            print(f"--- [GERENCIADOR] Cliente {cliente.nome} adicionado. ---")
        else: print(f"--- [GERENCIADOR] Cliente com ID ou e-mail já existente não adicionado: {cliente.nome} ---")
    def obter_cliente_por_id(self, cliente_id: str) -> Optional[Cliente]:
        return next((c for c in self._clientes if c.id == cliente_id), None)
    def atualizar_cliente(self, cliente_id: str, nome: str, telefone: str, email: str) -> bool:
        cliente = self.obter_cliente_por_id(cliente_id)
        if cliente: cliente.nome = nome; cliente.telefone = telefone; cliente.email = email; self._salvar_dados(); return True
        return False
    def remover_cliente(self, cliente_id: str) -> bool:
        cliente = self.obter_cliente_por_id(cliente_id)
        if cliente: self._clientes.remove(cliente); self._reservas = [r for r in self._reservas if r.cliente_id != cliente_id]; self._salvar_dados(); return True
        return False

    # --- Métodos Quarto ---
    def adicionar_quarto(self, quarto: Quarto) -> None:
        if not any(q.numero == quarto.numero for q in self._quartos):
            self._quartos.append(quarto); self._salvar_dados()
            print(f"--- [GERENCIADOR] Quarto {quarto.numero} adicionado. ---")
        else: print(f"--- [GERENCIADOR] Quarto {quarto.numero} já existe. ---")
    def obter_quarto_por_numero(self, numero: int) -> Optional[Quarto]:
        return next((q for q in self._quartos if q.numero == numero), None)
    def atualizar_quarto(self, numero: int, tipo: str, preco: float, disponivel: bool) -> bool:
        quarto = self.obter_quarto_por_numero(numero)
        if quarto: quarto.tipo = tipo; quarto.preco = preco; quarto.disponivel = disponivel; self._salvar_dados(); return True
        return False
    def remover_quarto(self, numero: int) -> bool:
        quarto = self.obter_quarto_por_numero(numero)
        if quarto: self._quartos.remove(quarto); self._reservas = [r for r in self._reservas if r.quarto_numero != numero]; self._salvar_dados(); return True
        return False

    # --- Métodos Reserva ---
    def criar_reserva(self, cliente_id: str, quarto_numero: int, check_in: str, check_out: str) -> Optional[Reserva]:
        cliente = self.obter_cliente_por_id(cliente_id); quarto = self.obter_quarto_por_numero(quarto_numero)
        if not cliente or not quarto: print("--- [GERENCIADOR] Erro criar reserva: Cliente ou Quarto não encontrado. ---"); return None
        if not self._verificar_disponibilidade(quarto_numero, check_in, check_out): print(f"--- [GERENCIADOR] Erro criar reserva: Quarto {quarto_numero} indisponível para {check_in} a {check_out}. ---"); return None
        if not quarto.disponivel: print(f"--- [GERENCIADOR] Erro criar reserva: Quarto {quarto_numero} está marcado como indisponível (ex: manutenção). ---"); return None
        reserva = Reserva(cliente_id, quarto_numero, check_in, check_out, status="Confirmada"); self._reservas.append(reserva); self._salvar_dados()
        print(f"--- [GERENCIADOR] Reserva criada com sucesso para cliente {cliente.id[:8]} no quarto {quarto_numero}. ---"); return reserva

    def _verificar_disponibilidade(self, quarto_numero: int, check_in_str: str, check_out_str: str) -> bool:
        quarto = self.obter_quarto_por_numero(quarto_numero)
        if not quarto or not quarto.disponivel: return False
        try:
            formato_data = "%d-%m-%Y"
            data_check_in = datetime.strptime(check_in_str, formato_data); data_check_out = datetime.strptime(check_out_str, formato_data)
            if data_check_out <= data_check_in: return False
            for reserva in self._reservas:
                if reserva.quarto_numero == quarto_numero and reserva.status not in ["Cancelada", "Concluída"]:
                    try:
                        reserva_check_in = datetime.strptime(reserva.check_in, formato_data); reserva_check_out = datetime.strptime(reserva.check_out, formato_data)
                        if max(data_check_in, reserva_check_in) < min(data_check_out, reserva_check_out): return False
                    except ValueError: continue
            return True
        except ValueError: print(f"--- [GERENCIADOR] Erro ao converter datas em _verificar_disponibilidade: {check_in_str}, {check_out_str}. ---"); return False

    def obter_reserva_por_id(self, reserva_id: str) -> Optional[Reserva]:
        return next((r for r in self._reservas if r.id == reserva_id), None)
    def atualizar_reserva(self, reserva_id: str, check_in: str, check_out: str, status: str) -> bool:
        reserva = self.obter_reserva_por_id(reserva_id)
        if reserva: reserva.check_in = check_in; reserva.check_out = check_out; reserva.status = status; self._salvar_dados(); return True
        return False
    def cancelar_reserva(self, reserva_id: str) -> Dict[str, Any]:
        try:
            print(f"--- [GERENCIADOR] Tentando cancelar reserva ID: {reserva_id[:8]} ---")
            reserva = self.obter_reserva_por_id(reserva_id)
            if not reserva: print(f"--- [GERENCIADOR] Reserva não encontrada ID: {reserva_id[:8]} ---"); return {"success": False, "message": "Reserva não encontrada"}
            if reserva.status in ["Cancelada", "Concluída"]: print(f"--- [GERENCIADOR] Reserva já está {reserva.status} ID: {reserva_id[:8]} ---"); return {"success": False, "message": f"Reserva já está {reserva.status}"}
            quarto = self.obter_quarto_por_numero(reserva.quarto_numero); cliente = self.obter_cliente_por_id(reserva.cliente_id)
            quarto_info = f"{quarto.numero} - {quarto.tipo}" if quarto else "desconhecido"; cliente_nome = cliente.nome if cliente else "desconhecido"
            print(f"--- [GERENCIADOR] Alterando status de '{reserva.status}' para 'Cancelada' ID: {reserva_id[:8]} ---")
            reserva.status = "Cancelada"
            print(f"--- [GERENCIADOR] Status da reserva {reserva_id[:8]} alterado para Cancelada. ---")
            print(f"--- [GERENCIADOR] Salvando dados após cancelamento ID: {reserva_id[:8]} ---"); self._salvar_dados()
            print(f"--- [GERENCIADOR] Reserva cancelada com sucesso ID: {reserva_id[:8]} ---")
            return {"success": True, "message": "Reserva cancelada com sucesso", "quarto_info": quarto_info, "cliente_nome": cliente_nome, "check_in": reserva.check_in, "check_out": reserva.check_out}
        except Exception as e: print(f"!!! [GERENCIADOR] ERRO ao cancelar reserva: {e} !!!"); print(traceback.format_exc()); return {"success": False, "message": f"Erro ao cancelar reserva: {str(e)}"}

    # --- Métodos de Listagem ---
    def listar_clientes(self) -> List[Cliente]: return self._clientes
    def listar_quartos(self) -> List[Quarto]: return sorted(self._quartos, key=lambda q: q.numero)
    def listar_reservas(self) -> List[Reserva]: return sorted(self._reservas, key=lambda r: r.check_in)
    def listar_reservas_por_cliente(self, cliente_id: str) -> List[Reserva]: return sorted([r for r in self._reservas if r.cliente_id == cliente_id], key=lambda r: r.check_in)
    def listar_reservas_por_quarto(self, quarto_numero: int) -> List[Reserva]: return sorted([r for r in self._reservas if r.quarto_numero == quarto_numero], key=lambda r: r.check_in)
    def listar_quartos_disponiveis(self, check_in: str = None, check_out: str = None) -> List[Quarto]:
        if not check_in or not check_out: return [q for q in self._quartos if q.disponivel]
        return [q for q in self.listar_quartos() if self._verificar_disponibilidade(q.numero, check_in, check_out)]

    # --- Persistência ---
    def _salvar_dados(self) -> None:
        dados = {"clientes": [c.to_dict() for c in self._clientes], "quartos": [q.to_dict() for q in self._quartos], "reservas": [r.to_dict() for r in self._reservas]}
        try:
            with open(self._arquivo_dados, "w") as arquivo: json.dump(dados, arquivo, indent=4)
            print(f"--- [GERENCIADOR] Dados salvos com sucesso em {self._arquivo_dados} ---")
        except Exception as e: print(f"!!! [GERENCIADOR] ERRO ao salvar dados: {e} !!!")

    def _carregar_dados(self) -> None:
        if not os.path.exists(self._arquivo_dados): self._criar_dados_iniciais(); return
        try:
            with open(self._arquivo_dados, "r") as arquivo: dados = json.load(arquivo)
            self._clientes = [Cliente.from_dict(c) for c in dados.get("clientes", [])]; self._quartos = [Quarto.from_dict(q) for q in dados.get("quartos", [])]; self._reservas = [Reserva.from_dict(r) for r in dados.get("reservas", [])]
            print(f"--- [GERENCIADOR] Dados carregados de {self._arquivo_dados} ---")
        except Exception as e: print(f"!!! [GERENCIADOR] ERRO ao carregar dados de {self._arquivo_dados}: {e} !!!"); self._criar_dados_iniciais()

    def _criar_dados_iniciais(self) -> None:
        print("--- [GERENCIADOR] Criando dados iniciais... ---"); self._clientes = []; self._quartos = [Quarto(101, "Single", 150.0), Quarto(102, "Single", 150.0), Quarto(201, "Double", 250.0), Quarto(202, "Double", 250.0), Quarto(301, "Suite", 400.0)]; self._reservas = []
        self._salvar_dados()

# ==============================================================================
# Função auxiliar para formatar data
# ==============================================================================
def formatar_data(data: datetime) -> str:
    return data.strftime("%d-%m-%Y")

# ==============================================================================
# Interface gráfica Flet
# ==============================================================================
def main(page: ft.Page):
    # Configurações da página
    page.title = "Refúgio dos Sonhos - Sistema de Gerenciamento"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1000
    page.window_height = 800
    page.padding = 15
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    gerenciador = GerenciadorDeReservas()

    # --- Variáveis de Estado e Controles UI ---
    cliente_selecionado_para_edicao = ft.Ref[Optional[Cliente]]()
    campo_nome_cliente = ft.TextField(label="Nome Completo", width=400, border_radius=8)
    campo_telefone_cliente = ft.TextField(label="Telefone", width=300, border_radius=8)
    campo_email_cliente = ft.TextField(label="E-mail", width=400, border_radius=8)
    dropdown_clientes_reserva = ft.Dropdown(label="Selecione o Cliente", width=450, border_radius=8)
    dropdown_quartos_reserva = ft.Dropdown(label="Selecione o Quarto", width=450, hint_text="Selecione as datas primeiro", border_radius=8, disabled=True)
    data_check_in_ref = ft.Ref[Optional[datetime]]()
    data_check_out_ref = ft.Ref[Optional[datetime]]()
    texto_check_in = ft.Text("Check-in: Não selecionado")
    texto_check_out = ft.Text("Check-out: Não selecionado")
    lista_quartos_view = ft.ListView(expand=True, spacing=8, padding=10, auto_scroll=True)
    lista_clientes_view = ft.ListView(expand=True, spacing=8, padding=10, auto_scroll=True)
    lista_reservas_view = ft.ListView(expand=True, spacing=8, padding=10, auto_scroll=True)
    conteudo_principal = ft.Column(expand=True, scroll=ft.ScrollMode.ADAPTIVE)

    # --- Funções Auxiliares da UI ---
    def mostrar_snackbar(mensagem: str, erro: bool = False):
        page.snack_bar = ft.SnackBar(ft.Text(mensagem), bgcolor=ft.Colors.RED_ACCENT_700 if erro else ft.Colors.GREEN_700, action="OK")
        page.snack_bar.open = True
        page.update()

    # --- Funções de Atualização de Listas/Dropdowns ---
    def atualizar_lista_quartos():
        print("--- [UI] Atualizando lista de quartos ---")
        lista_quartos_view.controls.clear()
        quartos = gerenciador.listar_quartos()
        if not quartos: lista_quartos_view.controls.append(ft.Text("Nenhum quarto cadastrado.", italic=True, color=ft.Colors.GREY))
        else:
            for quarto in quartos:
                status_base = quarto.disponivel
                cor_borda = ft.Colors.GREEN if status_base else ft.Colors.ORANGE
                icone = ft.Icons.CHECK_CIRCLE_OUTLINE if status_base else ft.Icons.CONSTRUCTION_OUTLINED
                status_texto = "Disponível" if status_base else "Manutenção"
                card_quarto = ft.Container(
                    content=ft.Row([
                        ft.Row([ft.Icon(name=ft.Icons.BED_OUTLINED, size=24, color=ft.Colors.BLUE_GREY_700),
                                ft.Column([ft.Text(f"Quarto {quarto.numero} - {quarto.tipo}", weight=ft.FontWeight.BOLD),
                                            ft.Text(f"R$ {quarto.preco:.2f} / diária", size=11, color=ft.Colors.GREY_700)], spacing=1)], spacing=8),
                        ft.Container(content=ft.Row([ft.Icon(name=icone, color=cor_borda, size=14), ft.Text(status_texto, size=9, weight=ft.FontWeight.BOLD)], spacing=3), padding=ft.padding.symmetric(horizontal=6, vertical=3), border_radius=8, bgcolor=ft.colors.with_opacity(0.1, cor_borda))
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=10, border_radius=6, border=ft.border.all(1, ft.colors.with_opacity(0.3, cor_borda)), margin=ft.margin.only(bottom=5), bgcolor=ft.Colors.WHITE,
                    # Removido on_click para simplificar dashboard
                )
                lista_quartos_view.controls.append(card_quarto)
        print(f"--- [UI] Lista de quartos atualizada com {len(lista_quartos_view.controls)} itens ---")
        # page.update() # Atualização será feita pelo navegar_para

    def atualizar_lista_clientes():
        print("--- [UI] Atualizando lista de clientes ---")
        lista_clientes_view.controls.clear()
        clientes = gerenciador.listar_clientes()
        if not clientes: lista_clientes_view.controls.append(ft.Text("Nenhum cliente cadastrado.", italic=True, color=ft.Colors.GREY))
        else:
            for cliente in clientes:
                card_cliente = ft.Card(elevation=1, margin=ft.margin.only(bottom=5),
                    content=ft.Container(
                        content=ft.Row([
                            ft.ListTile(leading=ft.Icon(ft.Icons.PERSON_PIN), title=ft.Text(cliente.nome, weight=ft.FontWeight.BOLD), subtitle=ft.Text(f"Tel: {cliente.telefone} | Email: {cliente.email}", size=11), dense=True, expand=True),
                            ft.Row([ft.IconButton(icon=ft.Icons.EDIT_NOTE, tooltip="Editar", on_click=lambda e, c=cliente: editar_cliente(c), icon_color=ft.Colors.BLUE),
                                    ft.IconButton(icon=ft.Icons.DELETE_FOREVER, tooltip="Excluir", on_click=lambda e, c=cliente: excluir_cliente(c), icon_color=ft.Colors.RED)], spacing=0)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), padding=ft.padding.symmetric(vertical=0, horizontal=8)
                    )
                )
                lista_clientes_view.controls.append(card_cliente)
        print(f"--- [UI] Lista de clientes atualizada com {len(lista_clientes_view.controls)} itens ---")
        # page.update() # Atualização será feita pelo navegar_para

    def atualizar_dropdown_clientes():
        # ... (código como na versão anterior) ...
        dropdown_clientes_reserva.options.clear()
        clientes = gerenciador.listar_clientes()
        if not clientes:
             dropdown_clientes_reserva.hint_text = "Nenhum cliente cadastrado"
             dropdown_clientes_reserva.value = None
             dropdown_clientes_reserva.disabled = True
        else:
            dropdown_clientes_reserva.hint_text = "Selecione..."
            dropdown_clientes_reserva.disabled = False
            for cliente in clientes:
                dropdown_clientes_reserva.options.append(
                    ft.dropdown.Option(key=cliente.id, text=cliente.nome)
                )
            # Não auto-seleciona, deixa o usuário escolher
            # if clientes and dropdown_clientes_reserva.value is None:
            #     dropdown_clientes_reserva.value = clientes[0].id
        # page.update() # Atualização será feita pelo navegar_para ou on_change dp

    def atualizar_dropdown_quartos(check_in_dt: Optional[datetime], check_out_dt: Optional[datetime]):
        # ... (código como na versão anterior) ...
        dropdown_quartos_reserva.options.clear()
        dropdown_quartos_reserva.value = None
        dropdown_quartos_reserva.disabled = True
        if not check_in_dt or not check_out_dt: dropdown_quartos_reserva.hint_text = "Selecione as datas"; page.update(); return
        if check_out_dt <= check_in_dt: dropdown_quartos_reserva.hint_text = "Check-out inválido"; page.update(); return
        check_in_str = formatar_data(check_in_dt); check_out_str = formatar_data(check_out_dt)
        quartos_disponiveis = gerenciador.listar_quartos_disponiveis(check_in_str, check_out_str)
        if not quartos_disponiveis: dropdown_quartos_reserva.hint_text = "Nenhum quarto disponível neste período"
        else:
            dropdown_quartos_reserva.hint_text = "Selecione..."; dropdown_quartos_reserva.disabled = False
            for quarto in quartos_disponiveis:
                dropdown_quartos_reserva.options.append(ft.dropdown.Option(key=str(quarto.numero), text=f"Quarto {quarto.numero} ({quarto.tipo}) - R${quarto.preco:.2f}"))
            # Não auto-seleciona, deixa o usuário escolher
            # if quartos_disponiveis: dropdown_quartos_reserva.value = str(quartos_disponiveis[0].numero)
        page.update() # Precisa atualizar o dropdown aqui

    def ocultar_e_cancelar_reserva(e, reserva_obj: Reserva, card_container: ft.Container):
        # ... (código como na versão anterior) ...
        print(f"--- [UI] Ocultar e cancelar chamado para ID: {reserva_obj.id[:8]} ---")
        card_container.visible = False; page.update()
        print(f"--- [UI] Card {reserva_obj.id[:8]} ocultado. ---")
        resultado_dict = gerenciador.cancelar_reserva(reserva_obj.id)
        print(f"--- [UI] Resultado do gerenciador.cancelar_reserva: {resultado_dict} ---")
        if isinstance(resultado_dict, dict) and resultado_dict.get("success"):
            mostrar_snackbar(f"Reserva de {resultado_dict.get('cliente_nome','')} cancelada.")
            atualizar_lista_reservas() # Reconstrói a lista
        else:
            mensagem_erro = resultado_dict.get("message", "Falha") if isinstance(resultado_dict, dict) else "Falha"
            mostrar_snackbar(f"Erro ao cancelar: {mensagem_erro}", erro=True)
            card_container.visible = True; page.update()
            print(f"--- [UI] Falha ao cancelar. Card {reserva_obj.id[:8]} re-exibido. ---")

    def atualizar_lista_reservas():
        # ... (código como na versão anterior, usando ocultar_e_cancelar_reserva) ...
        print("--- [UI] Atualizando lista de reservas (com ocultar/cancelar) ---")
        lista_reservas_view.controls.clear()
        reservas = gerenciador.listar_reservas()
        if not reservas: lista_reservas_view.controls.append(ft.Text("Nenhuma reserva encontrada.", italic=True, color=ft.Colors.GREY))
        else:
            for reserva in reservas:
                cliente = gerenciador.obter_cliente_por_id(reserva.cliente_id); quarto = gerenciador.obter_quarto_por_numero(reserva.quarto_numero)
                if not cliente or not quarto: continue
                cor_status_map = {"Confirmada": ft.Colors.GREEN, "Pendente": ft.Colors.ORANGE, "Cancelada": ft.Colors.RED, "Concluída": ft.Colors.BLUE_GREY}
                cor_status = cor_status_map.get(reserva.status, ft.Colors.GREY)
                opacity = 1.0 if reserva.status not in ["Cancelada", "Concluída"] else 0.6
                botoes_habilitados = reserva.status not in ["Cancelada", "Concluída"]
                card_reserva = ft.Container(padding=15, border_radius=8, border=ft.border.all(1, cor_status), margin=ft.margin.only(bottom=10), opacity=opacity, bgcolor=ft.Colors.WHITE, shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.colors.with_opacity(0.1, ft.Colors.BLACK)), visible=True)
                botoes_acao = ft.Row([
                    ft.IconButton(icon=ft.Icons.EDIT_NOTE, tooltip="Editar Reserva", on_click=lambda e, r=reserva: editar_reserva(r), disabled=not botoes_habilitados, icon_color=ft.Colors.BLUE if botoes_habilitados else ft.Colors.GREY),
                    ft.IconButton(icon=ft.Icons.CANCEL_OUTLINED, tooltip="Cancelar Reserva", on_click=lambda e, r=reserva, card=card_reserva: ocultar_e_cancelar_reserva(e, r, card), disabled=not botoes_habilitados, icon_color=ft.Colors.RED if botoes_habilitados else ft.Colors.GREY)
                ], alignment=ft.MainAxisAlignment.END, spacing=5)
                card_reserva.content=ft.Column([
                    ft.ListTile(leading=ft.Icon(ft.Icons.BOOKMARK_BORDER, color=cor_status, size=30), title=ft.Text(f"Reserva de {cliente.nome}", weight=ft.FontWeight.BOLD),
                                subtitle=ft.Column([ft.Text(f"Quarto: {quarto.numero} ({quarto.tipo})"), ft.Text(f"Check-in: {reserva.check_in} | Check-out: {reserva.check_out}"),
                                                    ft.Container(content=ft.Text(reserva.status, color=ft.Colors.WHITE, size=10, weight=ft.FontWeight.BOLD), padding=ft.padding.symmetric(horizontal=8, vertical=3), border_radius=10, bgcolor=cor_status, margin=ft.margin.only(top=5))], spacing=2)),
                    botoes_acao
                ], spacing=5)
                lista_reservas_view.controls.append(card_reserva)
        print(f"--- [UI] Lista de reservas atualizada com {len(lista_reservas_view.controls)} itens ---")
        # page.update() # Atualização é feita pelo navegar_para


    # --- Funções de Manipulação e Ação ---
    def editar_reserva(reserva: Reserva):
        mostrar_snackbar(f"Editar Reserva ID {reserva.id[:8]} - AINDA NÃO IMPLEMENTADO", erro=True)
        pass

    def editar_cliente(cliente: Cliente):
        cliente_selecionado_para_edicao.current = cliente
        campo_nome_cliente.value = cliente.nome; campo_telefone_cliente.value = cliente.telefone; campo_email_cliente.value = cliente.email
        navegar_para("formulario_cliente")

    def excluir_cliente(cliente: Cliente):
        # Ideal: Adicionar diálogo de confirmação
        def confirmar_exclusao(e):
             if gerenciador.remover_cliente(cliente.id):
                 mostrar_snackbar("Cliente excluído com sucesso.")
                 atualizar_lista_clientes()
                 atualizar_dropdown_clientes()
             else: mostrar_snackbar("Erro ao excluir cliente.", erro=True)
             page.dialog.open = False; page.dialog = None; page.update()

        def fechar_dialogo(e):
             page.dialog.open = False; page.dialog = None; page.update()

        dialogo = ft.AlertDialog(title=ft.Text("Confirmar Exclusão"), content=ft.Text(f"Excluir cliente {cliente.nome}? Isso removerá suas reservas."),
                                 actions=[ft.TextButton("Cancelar", on_click=fechar_dialogo), ft.TextButton("Excluir", on_click=confirmar_exclusao, style=ft.ButtonStyle(color=ft.Colors.RED))])
        page.dialog = dialogo; page.dialog.open = True; page.update()


    def salvar_novo_ou_editar_cliente(e):
        nome = campo_nome_cliente.value.strip(); telefone = campo_telefone_cliente.value.strip(); email = campo_email_cliente.value.strip().lower()
        if not nome or not telefone or not email: mostrar_snackbar("Preencha todos os campos.", erro=True); return
        if cliente_selecionado_para_edicao.current:
            cliente_id = cliente_selecionado_para_edicao.current.id
            if gerenciador.atualizar_cliente(cliente_id, nome, telefone, email): mostrar_snackbar("Cliente atualizado."); cliente_selecionado_para_edicao.current = None; navegar_para("clientes"); atualizar_dropdown_clientes()
            else: mostrar_snackbar("Erro ao atualizar.", erro=True)
        else:
            if any(c.email == email for c in gerenciador.listar_clientes()): mostrar_snackbar(f"E-mail '{email}' já cadastrado.", erro=True); return
            novo_cliente = Cliente(nome=nome, telefone=telefone, email=email); gerenciador.adicionar_cliente(novo_cliente); mostrar_snackbar("Cliente adicionado.")
            campo_nome_cliente.value = ""; campo_telefone_cliente.value = ""; campo_email_cliente.value = ""
            navegar_para("clientes"); atualizar_dropdown_clientes()

    def salvar_nova_reserva(e):
         cliente_id = dropdown_clientes_reserva.value; quarto_numero_str = dropdown_quartos_reserva.value
         check_in_dt = data_check_in_ref.current; check_out_dt = data_check_out_ref.current
         if not cliente_id or not quarto_numero_str or not check_in_dt or not check_out_dt: mostrar_snackbar("Selecione Cliente, Quarto e Datas!", erro=True); return
         if check_out_dt <= check_in_dt: mostrar_snackbar("Data de Check-out deve ser após Check-in!", erro=True); return
         try:
              quarto_numero = int(quarto_numero_str); check_in_str = formatar_data(check_in_dt); check_out_str = formatar_data(check_out_dt)
              nova_reserva = gerenciador.criar_reserva(cliente_id, quarto_numero, check_in_str, check_out_str)
              if nova_reserva: mostrar_snackbar("Reserva criada!"); navegar_para("reservas")
              else: mostrar_snackbar("Falha ao criar reserva.", erro=True)
         except ValueError: mostrar_snackbar("Erro: Número do quarto inválido.", erro=True)
         except Exception as ex: mostrar_snackbar(f"Erro inesperado: {ex}", erro=True); print(traceback.format_exc())

    # --- Date Pickers ---
    def abrir_datepicker_checkin(e):
        page.open(ft.DatePicker(first_date=datetime.now() - timedelta(days=1), last_date=datetime.now() + timedelta(days=365 * 2), current_date=data_check_in_ref.current or datetime.now(), on_change=lambda dp_e: on_change_datepicker(dp_e, data_check_in_ref, texto_check_in, "Check-in")))
    def abrir_datepicker_checkout(e):
         page.open(ft.DatePicker(first_date=data_check_in_ref.current + timedelta(days=1) if data_check_in_ref.current else datetime.now(), last_date=datetime.now() + timedelta(days=365 * 2), current_date=data_check_out_ref.current or (data_check_in_ref.current + timedelta(days=1) if data_check_in_ref.current else datetime.now() + timedelta(days=1)), on_change=lambda dp_e: on_change_datepicker(dp_e, data_check_out_ref, texto_check_out, "Check-out")))
    def on_change_datepicker(e: ft.ControlEvent, ref_data: ft.Ref[Optional[datetime]], controle_texto: ft.Text, label: str):
        if e.control.value:
            data_selecionada = e.control.value.replace(hour=0, minute=0, second=0, microsecond=0); ref_data.current = data_selecionada; controle_texto.value = f"{label}: {formatar_data(data_selecionada)}"
            print(f"Data {label} selecionada: {ref_data.current}")
            if data_check_in_ref.current and data_check_out_ref.current: atualizar_dropdown_quartos(data_check_in_ref.current, data_check_out_ref.current)
            else: atualizar_dropdown_quartos(None, None)
        else: ref_data.current = None; controle_texto.value = f"{label}: Não selecionado"; print(f"Data {label} deselecionada"); atualizar_dropdown_quartos(None, None)
        page.update()


    # --- FUNÇÕES PARA MONTAR AS TELAS (VIEWS) ---
    def criar_view_inicial():
        print("--- Montando View Inicial (Dashboard) ---")
        atualizar_lista_quartos() # Prepara a lista de quartos

        # Calcula estatísticas
        total_quartos = len(gerenciador.listar_quartos())
        # Simplificado: usa o flag base para "Disponível" no dashboard
        quartos_disp_base = len([q for q in gerenciador.listar_quartos() if q.disponivel])
        total_clientes = len(gerenciador.listar_clientes())
        reservas_ativas = len([r for r in gerenciador.listar_reservas() if r.status == 'Confirmada'])

        # Widgets de Estatística
        def criar_stat_card(valor, rotulo, icone, cor):
            return ft.Container(
                content=ft.Row([
                        ft.Icon(icone, color=cor, size=24),
                        ft.Column([
                            ft.Text(str(valor), size=20, weight=ft.FontWeight.BOLD),
                            ft.Text(rotulo, size=11, color=ft.Colors.BLACK54)], spacing=0)],spacing=10),
                 padding=15, border_radius=8, bgcolor=ft.colors.with_opacity(0.05, cor), width=180, alignment=ft.alignment.center_left
            )

        stats_row = ft.Row([
            criar_stat_card(total_quartos, "Total Quartos", ft.Icons.HOTEL, ft.Colors.BLUE),
            criar_stat_card(quartos_disp_base, "Quartos Livres*", ft.Icons.BED, ft.Colors.GREEN), # *Baseado no status geral
            criar_stat_card(total_clientes, "Clientes", ft.Icons.PEOPLE, ft.Colors.PURPLE),
            criar_stat_card(reservas_ativas, "Reservas Ativas", ft.Icons.BOOKMARK, ft.Colors.ORANGE),
        ], alignment=ft.MainAxisAlignment.SPACE_AROUND, wrap=True) # Wrap para telas menores

        # Botões de Ação
        botoes_acao = ft.Row([
            ft.ElevatedButton("Nova Reserva", icon=ft.Icons.ADD_CIRCLE_OUTLINE, on_click=lambda e: navegar_para("formulario_reserva"), style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE)),
            ft.ElevatedButton("Novo Cliente", icon=ft.Icons.PERSON_ADD_ALT_1, on_click=lambda e: navegar_para("formulario_cliente"), style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

         # Monta a Coluna da View
        return ft.Column([
            ft.Text("Dashboard - Refúgio dos Sonhos", size=26, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Divider(height=20),
            stats_row,
            ft.Divider(height=30),
            botoes_acao,
            ft.Divider(height=30),
            ft.Text("Status Geral dos Quartos", size=18, weight=ft.FontWeight.W_500 ),
            lista_quartos_view, # Adiciona a lista de quartos
         ], expand=True, scroll=ft.ScrollMode.ADAPTIVE)

    def criar_view_clientes():
         atualizar_lista_clientes()
         return ft.Column([
             ft.Row([ft.Text("Clientes", size=24, weight=ft.FontWeight.BOLD),
                    ft.ElevatedButton("Novo Cliente", icon=ft.Icons.ADD, on_click=lambda e: navegar_para("formulario_cliente")) ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
             ft.Divider(),
             lista_clientes_view,
         ], expand=True, scroll=ft.ScrollMode.ADAPTIVE)

    def criar_view_formulario_cliente():
        titulo = "Novo Cliente" if not cliente_selecionado_para_edicao.current else f"Editar Cliente: {cliente_selecionado_para_edicao.current.nome}"
        return ft.Column([ ft.Text(titulo, size=24, weight=ft.FontWeight.BOLD), ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                          campo_nome_cliente, ft.Container(height=5), campo_telefone_cliente, ft.Container(height=5), campo_email_cliente, ft.Container(height=15),
                          ft.Row([ ft.OutlinedButton("Cancelar", on_click=lambda e: navegar_para("clientes")),
                                  ft.ElevatedButton("Salvar Cliente", icon=ft.Icons.SAVE, on_click=salvar_novo_ou_editar_cliente, style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE))],
                                 alignment=ft.MainAxisAlignment.END) ], expand=True, scroll=ft.ScrollMode.ADAPTIVE, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def criar_view_reservas():
         atualizar_lista_reservas()
         return ft.Column([
             ft.Row([ft.Text("Reservas", size=24, weight=ft.FontWeight.BOLD),
                    # REMOVIDO: Botão Nova Reserva daqui
                   ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
             ft.Divider(),
             lista_reservas_view,
         ], expand=True, scroll=ft.ScrollMode.ADAPTIVE)

    def criar_view_formulario_reserva():
        dropdown_clientes_reserva.value = None; atualizar_dropdown_clientes()
        data_check_in_ref.current = None; data_check_out_ref.current = None
        texto_check_in.value = "Check-in: Não selecionado"; texto_check_out.value = "Check-out: Não selecionado"
        atualizar_dropdown_quartos(None, None) # Limpa e desabilita quartos
        return ft.Column([
            ft.Text("Nova Reserva", size=24, weight=ft.FontWeight.BOLD), ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            dropdown_clientes_reserva, ft.Container(height=15),
            ft.Row([ ft.Column([texto_check_in, ft.ElevatedButton("Selecionar Data", icon=ft.Icons.CALENDAR_MONTH, on_click=abrir_datepicker_checkin)]),
                     ft.Column([texto_check_out, ft.ElevatedButton("Selecionar Data", icon=ft.Icons.CALENDAR_MONTH, on_click=abrir_datepicker_checkout)]) ],
                   alignment=ft.MainAxisAlignment.SPACE_EVENLY), ft.Container(height=15),
            dropdown_quartos_reserva, ft.Container(height=20),
            ft.Row([ ft.OutlinedButton("Cancelar", on_click=lambda e: navegar_para("reservas")),
                    ft.ElevatedButton("Criar Reserva", icon=ft.Icons.CHECK, on_click=salvar_nova_reserva, style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE)) ],
                   alignment=ft.MainAxisAlignment.END)
            ], expand=True, scroll=ft.ScrollMode.ADAPTIVE, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # --- FUNÇÃO DE NAVEGAÇÃO PRINCIPAL ---
    def navegar_para(destino: str):
        print(f"--- Navegando para: {destino} ---")
        conteudo_principal.controls.clear()
        if destino != "formulario_cliente": cliente_selecionado_para_edicao.current = None
        view_content = None
        try: # Adiciona try-except na construção da view
            if destino == "inicial": view_content = criar_view_inicial()
            elif destino == "clientes": view_content = criar_view_clientes()
            elif destino == "formulario_cliente": view_content = criar_view_formulario_cliente()
            elif destino == "reservas": view_content = criar_view_reservas()
            elif destino == "formulario_reserva": view_content = criar_view_formulario_reserva()
            else: view_content = ft.Text(f"Erro: Tela '{destino}' desconhecida.", color=ft.Colors.RED)

            if view_content: conteudo_principal.controls.append(view_content)
            page.update() # Atualiza a página após adicionar o conteúdo
            print(f"--- Navegação para {destino} concluída. ---")
        except Exception as e_nav:
             print(f"!!! ERRO AO CONSTRUIR VIEW para {destino}: {e_nav} !!!")
             print(traceback.format_exc())
             conteudo_principal.controls.append(ft.Text(f"Erro ao carregar a tela '{destino}'. Verifique os logs.", color=ft.Colors.RED))
             page.update()


    # --- Barra de Navegação Superior (AppBar) ---
    barra_navegacao = ft.AppBar(
        title=ft.Text("Refúgio dos Sonhos"), center_title=True, bgcolor=ft.Colors.BLUE_GREY_700,
        actions=[
            ft.IconButton(icon=ft.Icons.DASHBOARD_OUTLINED, tooltip="Dashboard", on_click=lambda e: navegar_para("inicial")),
            ft.IconButton(icon=ft.Icons.PEOPLE_OUTLINE, tooltip="Clientes", on_click=lambda e: navegar_para("clientes")),
            # --- ÍCONE ALTERADO ---
            ft.IconButton(icon=ft.Icons.BED_OUTLINED, tooltip="Ver Reservas", on_click=lambda e: navegar_para("reservas")),
            # --------------------
            ft.IconButton(icon=ft.Icons.ADD_BOX_OUTLINED, tooltip="Nova Reserva", on_click=lambda e: navegar_para("formulario_reserva")),
        ]
    )

    # --- Configuração Inicial da Página ---
    page.appbar = barra_navegacao
    page.add(conteudo_principal)
    navegar_para("inicial")


# --- Ponto de Entrada da Aplicação ---
if __name__ == "__main__":
    ft.app(target=main)