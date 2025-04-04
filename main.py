# main.py
import flet as ft
from datetime import date, timedelta, datetime
from typing import Optional # Import Optional
from models import ( # Importa tudo do __init__.py de models
    Cliente,
    Quarto,
    Reserva,
    GerenciadorDeReservas
)

# --- Instância Global do Gerenciador (simplificação para este exemplo) ---
gerenciador = GerenciadorDeReservas()

# --- Dados Iniciais de Exemplo ---
def carregar_dados_iniciais():
    # Clientes
    c1 = Cliente("Alice Silva", "(11) 98765-4321", "alice.silva@email.com")
    c2 = Cliente("Bruno Costa", "(21) 91234-5678", "bruno.costa@email.com")
    c3 = Cliente("Carla Dias", "(31) 99999-0000", "carla.dias@provider.net")
    gerenciador.adicionar_cliente(c1)
    gerenciador.adicionar_cliente(c2)
    gerenciador.adicionar_cliente(c3)

    # Quartos
    q101 = Quarto(numero=101, tipo="single", preco_diaria=150.00)
    q102 = Quarto(numero=102, tipo="double", preco_diaria=250.00)
    q201 = Quarto(numero=201, tipo="suite", preco_diaria=400.00)
    q202 = Quarto(numero=202, tipo="double", preco_diaria=260.00)
    gerenciador.adicionar_quarto(q101)
    gerenciador.adicionar_quarto(q102)
    gerenciador.adicionar_quarto(q201)
    gerenciador.adicionar_quarto(q202)
    q202.set_status_disponibilidade("manutenção") # Exemplo de status

    # Reservas (Exemplo)
    try:
        hoje = date.today()
        amanha = hoje + timedelta(days=1)
        daqui_tres_dias = hoje + timedelta(days=3)
        gerenciador.criar_reserva(c1.id_unico, 101, hoje, amanha)
        # Tentativa de reservar quarto em manutenção (deve falhar no gerenciador)
        # gerenciador.criar_reserva(c2.id_unico, 202, amanha, daqui_tres_dias)
        gerenciador.criar_reserva(c2.id_unico, 102, amanha, daqui_tres_dias)
    except Exception as e:
        print(f"Erro ao criar reservas iniciais: {e}")

# --- Funções Auxiliares da Interface ---
def mostrar_snackbar(page: ft.Page, mensagem: str, error: bool = False):
    """Exibe uma mensagem rápida na parte inferior da tela."""
    page.show_snack_bar(
        ft.SnackBar(
            ft.Text(mensagem),
            # CORREÇÃO: Use ft.Colors
            bgcolor=ft.Colors.RED_ACCENT_700 if error else ft.Colors.GREEN_700,
            open=True
        )
    )

# --- Componentes Reutilizáveis da Interface ---

# --- Telas (Views) da Aplicação ---

def criar_tela_inicial(page: ft.Page) -> ft.View:
    """Cria a View da tela inicial."""
    print("Criando Tela Inicial")
    quartos_disponiveis = gerenciador.listar_quartos() # Lista todos por padrão

    lista_quartos_ui = ft.ListView(expand=True, spacing=10)
    if quartos_disponiveis:
        for quarto in quartos_disponiveis:
            # CORREÇÃO: Use ft.Colors
            cor_status = ft.Colors.GREEN_500 if quarto.esta_disponivel() else (ft.Colors.RED_500 if quarto.status_disponibilidade == 'ocupado' else ft.Colors.ORANGE_500)
            lista_quartos_ui.controls.append(
                ft.Card(
                    ft.Container(
                        padding=10, # Container aceita padding numérico
                        content=ft.Column([
                            ft.Text(f"Quarto {quarto.numero} ({quarto.tipo.capitalize()})", weight=ft.FontWeight.BOLD),
                            ft.Text(f"Preço: R$ {quarto.preco_diaria:.2f}/noite"),
                            ft.Row([
                                ft.Text("Status:"),
                                ft.Text(quarto.status_disponibilidade.capitalize(), color=cor_status, weight=ft.FontWeight.BOLD)
                            ])
                        ])
                    )
                )
            )
    else:
        lista_quartos_ui.controls.append(ft.Text("Nenhum quarto cadastrado."))

    return ft.View(
        "/",
        controls=[
            # CORREÇÃO: Usar NOME da cor do tema como string
            ft.AppBar(title=ft.Text("Refúgio dos Sonhos - Início"), bgcolor="surfaceVariant"),
            # ... (restante dos controles ok) ...
             ft.Padding(padding=ft.padding.all(10), content=ft.Text("Quartos:", style=ft.TextThemeStyle.HEADLINE_SMALL)),
            ft.Container(content=lista_quartos_ui, expand=True, padding=ft.padding.only(left=10, right=10, bottom=10)),
            ft.Padding(padding=ft.padding.all(10), content=
                ft.Row(
                    controls=[
                        ft.ElevatedButton("Nova Reserva", icon=ft.icons.ADD_CIRCLE_OUTLINE, on_click=lambda _: page.go("/nova_reserva")),
                        ft.ElevatedButton("Gerenciar Clientes", icon=ft.icons.PEOPLE_OUTLINE, on_click=lambda _: page.go("/clientes")),
                        ft.ElevatedButton("Ver Reservas", icon=ft.icons.LIST_ALT_OUTLINED, on_click=lambda _: page.go("/reservas")),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND
                )
           )
        ],
        vertical_alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

def criar_tela_gerenciar_clientes(page: ft.Page) -> ft.View:
    """Cria a View para gerenciar clientes."""
    print("Criando Tela Gerenciar Clientes")

    # Campos do formulário para adicionar novo cliente
    txt_nome = ft.TextField(label="Nome Completo", width=300)
    txt_telefone = ft.TextField(label="Telefone (ex: (XX) XXXXX-XXXX)", width=200)
    txt_email = ft.TextField(label="E-mail", width=300)

    # Tabela para exibir clientes
    tabela_clientes = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Telefone")),
            ft.DataColumn(ft.Text("E-mail")),
            ft.DataColumn(ft.Text("ID Cliente")),
        ],
        rows=[],
        expand=True,
    )

    def preencher_tabela_clientes():
        """Atualiza as linhas da tabela de clientes."""
        tabela_clientes.rows.clear()
        clientes = gerenciador.listar_clientes()
        for cliente in clientes:
            tabela_clientes.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(cliente.nome)),
                        ft.DataCell(ft.Text(cliente.telefone)),
                        ft.DataCell(ft.Text(cliente.email)),
                        ft.DataCell(ft.Text(cliente.id_unico[:8] + "...")),
                    ]
                )
            )
        if page.views and page.views[-1].route == "/clientes":
             tabela_clientes.update()


    def adicionar_cliente_click(e):
        """Callback para o botão de adicionar cliente."""
        nome = txt_nome.value.strip()
        telefone = txt_telefone.value.strip()
        email = txt_email.value.strip().lower()

        if not nome or not telefone or not email:
            mostrar_snackbar(page, "Erro: Preencha todos os campos!", error=True)
            return

        try:
            novo_cliente = Cliente(nome=nome, telefone=telefone, email=email)
            sucesso = gerenciador.adicionar_cliente(novo_cliente)
            if sucesso:
                mostrar_snackbar(page, f"Cliente '{nome}' adicionado com sucesso!")
                txt_nome.value = ""
                txt_telefone.value = ""
                txt_email.value = ""
                preencher_tabela_clientes()
                txt_nome.update()
                txt_telefone.update()
                txt_email.update()
            else:
                mostrar_snackbar(page, "Erro ao adicionar cliente (verifique console ou dados duplicados).", error=True)
        except (ValueError, TypeError) as ex:
             mostrar_snackbar(page, f"Erro nos dados do cliente: {ex}", error=True)

    preencher_tabela_clientes()

    return ft.View(
        "/clientes",
        controls=[
            # CORREÇÃO: Usar NOME da cor do tema como string
            ft.AppBar(title=ft.Text("Gerenciar Clientes"), bgcolor="surfaceVariant"),
            # ... (restante dos controles ok) ...
            ft.Padding(padding=ft.padding.all(10), content=
                ft.Column([
                    ft.Text("Adicionar Novo Cliente", style=ft.TextThemeStyle.TITLE_MEDIUM),
                    txt_nome,
                    txt_telefone,
                    txt_email,
                    ft.ElevatedButton("Adicionar Cliente", icon=ft.icons.ADD, on_click=adicionar_cliente_click)
                ])
            ),
            ft.Divider(),
            ft.Padding(padding=ft.padding.all(10), content=
                ft.Column([
                    ft.Text("Clientes Cadastrados", style=ft.TextThemeStyle.TITLE_MEDIUM),
                    ft.Container(content=tabela_clientes, expand=True)
                ], expand=True)
            )
        ],
    )

def criar_tela_nova_reserva(page: ft.Page) -> ft.View:
    """Cria a View para realizar uma nova reserva."""
    print("Criando Tela Nova Reserva")

    # --- Controles do Formulário ---
    dropdown_cliente = ft.Dropdown(
        label="Selecione o Cliente",
        options=[
            ft.dropdown.Option(cliente.id_unico, cliente.nome)
            for cliente in gerenciador.listar_clientes()
        ],
        width=400
    )

    dropdown_quarto = ft.Dropdown(
        label="Selecione o Quarto Disponível",
        options=[
            ft.dropdown.Option(str(quarto.numero), f"Quarto {quarto.numero} ({quarto.tipo.capitalize()}) - R${quarto.preco_diaria:.2f}")
            for quarto in gerenciador.listar_quartos()
        ],
        width=400
    )

    data_checkin_selecionada = ft.Text("Selecione...")
    data_checkout_selecionada = ft.Text("Selecione...")
    data_checkin_val: Optional[date] = None
    data_checkout_val: Optional[date] = None

    def atualizar_data_checkin(e):
        nonlocal data_checkin_val
        data_checkin_val = date.fromisoformat(e.control.value.strftime('%Y-%m-%d')) if e.control.value else None
        data_checkin_selecionada.value = data_checkin_val.strftime('%d/%m/%Y') if data_checkin_val else "Selecione..."
        data_checkin_selecionada.update()
        print(f"Data Check-in selecionada: {data_checkin_val}")

    def atualizar_data_checkout(e):
        nonlocal data_checkout_val
        data_checkout_val = date.fromisoformat(e.control.value.strftime('%Y-%m-%d')) if e.control.value else None
        data_checkout_selecionada.value = data_checkout_val.strftime('%d/%m/%Y') if data_checkout_val else "Selecione..."
        data_checkout_selecionada.update()
        print(f"Data Check-out selecionada: {data_checkout_val}")

    date_picker_checkin = ft.DatePicker(
        on_change=atualizar_data_checkin,
        first_date=datetime.now() - timedelta(days=0),
        last_date=datetime.now() + timedelta(days=365),
        help_text="Selecione a data de check-in"
    )
    date_picker_checkout = ft.DatePicker(
        on_change=atualizar_data_checkout,
        first_date=datetime.now() - timedelta(days=0),
        last_date=datetime.now() + timedelta(days=365*2),
        help_text="Selecione a data de check-out"
    )

    page.overlay.append(date_picker_checkin)
    page.overlay.append(date_picker_checkout)

    def confirmar_reserva_click(e):
        nonlocal data_checkin_val, data_checkout_val # CORREÇÃO ANTERIOR MANTIDA

        id_cliente = dropdown_cliente.value
        numero_quarto_str = dropdown_quarto.value
        checkin = data_checkin_val
        checkout = data_checkout_val

        if not id_cliente or not numero_quarto_str or not checkin or not checkout:
            mostrar_snackbar(page, "Erro: Preencha todos os campos (Cliente, Quarto, Datas)!", error=True)
            return

        try:
            numero_quarto = int(numero_quarto_str)
            reserva_criada = gerenciador.criar_reserva(id_cliente, numero_quarto, checkin, checkout)

            if reserva_criada:
                mostrar_snackbar(page, f"Reserva para {reserva_criada.cliente.nome} no quarto {numero_quarto} confirmada!")
                dropdown_cliente.value = None
                dropdown_quarto.value = None
                data_checkin_val = None
                data_checkout_val = None
                data_checkin_selecionada.value = "Selecione..."
                data_checkout_selecionada.value = "Selecione..."
                dropdown_cliente.update()
                dropdown_quarto.update()
                data_checkin_selecionada.update()
                data_checkout_selecionada.update()
            else:
                mostrar_snackbar(page, "Erro ao criar reserva (verifique console ou disponibilidade).", error=True)

        except ValueError:
            mostrar_snackbar(page, "Erro: Número do quarto inválido.", error=True)
        except Exception as ex:
            mostrar_snackbar(page, f"Erro inesperado: {ex}", error=True)

    return ft.View(
        "/nova_reserva",
        controls=[
            # CORREÇÃO: Usar NOME da cor do tema como string
            ft.AppBar(title=ft.Text("Criar Nova Reserva"), bgcolor="surfaceVariant"),
            # ... (restante dos controles ok) ...
            ft.Padding(padding=ft.padding.all(20), content=
                ft.Column(
                    controls=[
                        dropdown_cliente,
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        dropdown_quarto,
                        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                        ft.Text("Período da Estadia:", style=ft.TextThemeStyle.TITLE_MEDIUM),
                        ft.Row([
                            ft.Text("Check-in:"),
                            data_checkin_selecionada,
                            ft.IconButton(
                                ft.icons.CALENDAR_MONTH,
                                tooltip="Selecionar data de Check-in",
                                on_click=lambda _: date_picker_checkin.pick_date(),
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Row([
                             ft.Text("Check-out:"),
                             data_checkout_selecionada,
                             ft.IconButton(
                                ft.icons.CALENDAR_MONTH,
                                tooltip="Selecionar data de Check-out",
                                on_click=lambda _: date_picker_checkout.pick_date(),
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                        ft.ElevatedButton(
                            "Confirmar Reserva",
                            icon=ft.icons.CHECK_CIRCLE_OUTLINE,
                            on_click=confirmar_reserva_click,
                            width=250
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15
                )
            )
        ]
    )


def criar_tela_visualizar_reservas(page: ft.Page) -> ft.View:
    """Cria a View para visualizar e cancelar reservas."""
    print("Criando Tela Visualizar Reservas")

    gerenciador.atualizar_status_reservas_concluidas()
    lista_reservas = gerenciador.listar_reservas()

    # CORREÇÃO: padding com ft.padding.all()
    reservas_ui = ft.ListView(expand=True, spacing=10, padding=ft.padding.all(10))

    def cancelar_reserva_click(reserva_id: str):
        """Callback para o botão de cancelar."""
        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Cancelamento"),
            content=ft.Text(f"Tem certeza que deseja cancelar a reserva ID {reserva_id[:8]}...?"),
            actions=[
                ft.TextButton("Sim", on_click=lambda _: confirmar_cancelamento(reserva_id)),
                ft.TextButton("Não", on_click=lambda _: fechar_dialog(confirm_dialog)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = confirm_dialog
        confirm_dialog.open = True
        page.update()

    def fechar_dialog(dialog: ft.AlertDialog):
        dialog.open = False
        page.update()

    def confirmar_cancelamento(reserva_id: str):
        sucesso = gerenciador.cancelar_reserva(reserva_id)
        if sucesso:
            mostrar_snackbar(page, f"Reserva {reserva_id[:8]}... cancelada.")
            page.go("/reservas")
        else:
            mostrar_snackbar(page, f"Erro ao cancelar reserva {reserva_id[:8]}...", error=True)
        fechar_dialog(page.dialog)


    if lista_reservas:
        for reserva in lista_reservas:
            # CORREÇÃO: Use ft.Colors
            cor_status = {
                "confirmada": ft.Colors.GREEN_700,
                "cancelada": ft.Colors.RED_700,
                "concluída": ft.Colors.GREY_700,
                "pendente": ft.Colors.ORANGE_700,
            }.get(reserva.status_reserva, ft.Colors.BLACK)

            botao_cancelar = ft.IconButton(
                    icon=ft.icons.CANCEL_OUTLINED,
                    tooltip="Cancelar Reserva",
                    # CORREÇÃO: Use ft.Colors
                    icon_color=ft.Colors.RED_ACCENT_700,
                    data=reserva.reserva_id,
                    on_click=lambda e: cancelar_reserva_click(e.control.data),
                    visible=(reserva.status_reserva == "confirmada")
            )

            reservas_ui.controls.append(
                ft.Card(
                    ft.Container(
                        padding=15, # Container aceita padding numérico
                        content=ft.Row(
                            [
                                ft.Column(
                                    [
                                        # CORREÇÃO: Use ft.Colors
                                        ft.Text(f"ID: {reserva.reserva_id[:8]}...", size=12, color=ft.Colors.SECONDARY),
                                        ft.Text(f"Cliente: {reserva.cliente.nome}", weight=ft.FontWeight.BOLD),
                                        ft.Text(f"Quarto: {reserva.quarto.numero} ({reserva.quarto.tipo.capitalize()})"),
                                        ft.Text(f"Período: {reserva.data_checkin.strftime('%d/%m/%y')} a {reserva.data_checkout.strftime('%d/%m/%y')}"),
                                        ft.Row([
                                            ft.Text("Status: "),
                                            ft.Text(reserva.status_reserva.capitalize(), color=cor_status, weight=ft.FontWeight.BOLD)
                                        ]),
                                    ],
                                    expand=True
                                ),
                                botao_cancelar
                            ],
                           alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    )
                )
            )
    else:
        reservas_ui.controls.append(ft.Text("Nenhuma reserva encontrada."))


    return ft.View(
        "/reservas",
        controls=[
            # CORREÇÃO: Use ft.Colors
            ft.AppBar(title=ft.Text("Visualizar Reservas"), bgcolor="surfaceVariant"),
            ft.Container(content=reservas_ui, expand=True)
        ]
    )


# --- Função Principal da Aplicação Flet ---
def main(page: ft.Page):
    page.title = "Sistema de Reservas - Refúgio dos Sonhos"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme = ft.Theme()
    page.dark_theme = ft.Theme()
    # page.theme_mode = ft.ThemeMode.SYSTEM

    if not gerenciador.listar_clientes():
        print("Carregando dados iniciais...")
        carregar_dados_iniciais()
        print("Dados carregados.")

    # --- Lógica de Roteamento ---
    def route_change(route):
        # Mensagem movida para o final para indicar sucesso ou falha
        # print(f"Mudando para rota: {page.route}")
        page.views.clear()

        try:
            if page.route == "/":
                page.views.append(criar_tela_inicial(page))
            elif page.route == "/clientes":
                page.views.append(criar_tela_gerenciar_clientes(page))
            elif page.route == "/nova_reserva":
                 page.views.append(criar_tela_nova_reserva(page))
            elif page.route == "/reservas":
                page.views.append(criar_tela_visualizar_reservas(page))
            else:
                 print(f"Rota desconhecida: {page.route}. Redirecionando para /")
                 page.views.append(criar_tela_inicial(page))

            page.update()
            print(f"View para rota {page.route} construída e exibida com sucesso.") # Mensagem de sucesso

        except Exception as e:
            print(f"Erro CRÍTICO ao construir a view para a rota {page.route}: {e}")
            try:
                page.views.clear()
                page.views.append(ft.View("/", [
                        ft.AppBar(title=ft.Text("Erro"), bgcolor=ft.Colors.RED_700), # Cor estática OK
                        ft.Text(f"Ocorreu um erro ao carregar a página '{page.route}':"),
                        ft.Text(str(e))
                    ],
                    # CORREÇÃO: Usar cor estática para background da tela de erro
                    bgcolor=ft.Colors.WHITE)
                )
                page.update()
                print(f"Tela de erro exibida para a falha na rota {page.route}.") # Mensagem de fallback
            except Exception as inner_e:
                 print(f"Erro GRAVE ao tentar exibir a tela de erro: {inner_e}")


    def view_pop(view):
        """Chamado quando o botão 'voltar' do Flet (ou do OS) é pressionado."""
        print("Voltando da view:", view.route)
        if len(page.views) > 1: # Garante que não tentemos remover a última view
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)
        else:
            print("Não é possível voltar além da view inicial.")


    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go("/")


# --- Execução da Aplicação ---
if __name__ == "__main__":
    ft.app(target=main)
    # Para rodar como web app (opcional):
    # ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8080)