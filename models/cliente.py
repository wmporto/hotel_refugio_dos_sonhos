# models/cliente.py
import uuid
from .pessoa import Pessoa # Importa a classe base

class Cliente(Pessoa):
    """Classe para representar um cliente do hotel, herdando de Pessoa."""
    def __init__(self, nome: str, telefone: str, email: str):
        super().__init__(nome, telefone, email) # Chama o construtor da classe pai
        # Adiciona o atributo específico do Cliente
        self._id_unico = str(uuid.uuid4()) # Gera um ID único universal

    # --- Getter para o ID ---
    def get_id_unico(self) -> str:
        return self._id_unico

    # --- Polimorfismo (Sobrescrevendo o método da classe pai) ---
    @property # Forma alternativa e pythonica de criar getter
    def id_unico(self) -> str:
        return self._id_unico

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def telefone(self) -> str:
        return self._telefone

    @property
    def email(self) -> str:
        return self._email

    def exibir_informacoes(self) -> str:
        """Retorna uma string com as informações do cliente, incluindo o ID."""
        info_base = super().exibir_informacoes() # Reutiliza o método da classe pai
        return f"{info_base}\\nID Cliente: {self.get_id_unico()}"

    def __str__(self) -> str:
        """Representação em string do objeto Cliente."""
        return f"{self.get_nome()} (ID: {self.get_id_unico()[:8]}...)" # Mostra nome e parte do ID

    def __repr__(self) -> str:
        """Representação 'oficial' do objeto."""
        return f"Cliente(nome='{self.get_nome()}', telefone='{self.get_telefone()}', email='{self.get_email()}', id_unico='{self.get_id_unico()}')"

