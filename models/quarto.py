# models/quarto.py
from typing import Literal # Para tipagem mais restrita

# Tipos de quarto permitidos
TipoQuarto = Literal["single", "double", "suite"]
StatusDisponibilidade = Literal["disponível", "ocupado", "manutenção"]

class Quarto:
    """Classe para representar um quarto do hotel."""
    def __init__(self, numero: int, tipo: TipoQuarto, preco_diaria: float):
        if not isinstance(numero, int) or numero <= 0:
            raise ValueError("Número do quarto deve ser um inteiro positivo.")
        if tipo not in ["single", "double", "suite"]:
            raise ValueError("Tipo de quarto inválido. Use 'single', 'double' ou 'suite'.")
        if not isinstance(preco_diaria, (int, float)) or preco_diaria <= 0:
            raise ValueError("Preço da diária deve ser um número positivo.")

        self._numero = numero
        self._tipo = tipo
        self._preco_diaria = float(preco_diaria)
        # Encapsulamento do status
        self._status_disponibilidade: StatusDisponibilidade = "disponível"

    # --- Getters usando @property (forma Pythonica) ---
    @property
    def numero(self) -> int:
        return self._numero

    @property
    def tipo(self) -> TipoQuarto:
        return self._tipo

    @property
    def preco_diaria(self) -> float:
        return self._preco_diaria

    @property
    def status_disponibilidade(self) -> StatusDisponibilidade:
        return self._status_disponibilidade

    # --- Setter para o status com validação ---
    def set_status_disponibilidade(self, status: StatusDisponibilidade):
        """Define o status de disponibilidade do quarto."""
        if status in ["disponível", "ocupado", "manutenção"]:
            self._status_disponibilidade = status
        else:
            print(f"Erro: Status '{status}' inválido para o quarto {self.numero}.")
            # Ou raise ValueError("Status de disponibilidade inválido.")

    # --- Outros Métodos ---
    def esta_disponivel(self) -> bool:
        """Verifica se o quarto está disponível."""
        return self._status_disponibilidade == "disponível"

    def exibir_informacoes(self) -> str:
        """Retorna uma string com as informações do quarto."""
        return (f"Quarto Nº: {self.numero}\\n"
                f"Tipo: {self.tipo.capitalize()}\\n"
                f"Preço Diária: R$ {self.preco_diaria:.2f}\\n"
                f"Status: {self.status_disponibilidade.capitalize()}")

    def __str__(self) -> str:
        """Representação em string do objeto Quarto."""
        return f"Quarto {self.numero} ({self.tipo.capitalize()}) - {self.status_disponibilidade.capitalize()}"

    def __repr__(self) -> str:
        """Representação 'oficial' do objeto."""
        return f"Quarto(numero={self.numero}, tipo='{self.tipo}', preco_diaria={self.preco_diaria}, status='{self.status_disponibilidade}')"

