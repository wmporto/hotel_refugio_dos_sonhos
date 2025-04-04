# models/pessoa.py
import re # Para validação de email/telefone (opcional)

class Pessoa:
    """Classe base para representar uma pessoa com informações básicas."""
    def __init__(self, nome: str, telefone: str, email: str):
        # Encapsulamento com atributos "privados" (convenção _ ou __)
        self._nome = nome
        self.set_telefone(telefone) # Usa setter para validação inicial
        self.set_email(email)       # Usa setter para validação inicial

    # --- Getters ---
    def get_nome(self) -> str:
        return self._nome

    def get_telefone(self) -> str:
        return self._telefone

    def get_email(self) -> str:
        return self._email

    # --- Setters com Validação (Exemplo) ---
    def set_nome(self, nome: str):
        if nome and isinstance(nome, str):
            self._nome = nome
        else:
            # Em uma aplicação real, seria melhor lançar uma exceção
            print("Erro: Nome inválido.")

    def set_telefone(self, telefone: str):
        # Exemplo simples de validação (pode ser mais robusto)
        # if telefone and isinstance(telefone, str) and re.match(r"^\\+?[0-9\\s\\-()]{7,}$", telefone):
        if telefone and isinstance(telefone, str): # Validação simplificada
             self._telefone = telefone
        else:
            print("Erro: Telefone inválido.")
            # self._telefone = "" # Ou define um valor padrão/lança exceção

    def set_email(self, email: str):
        # Exemplo simples de validação de e-mail
        if email and isinstance(email, str) and "@" in email and "." in email.split("@")[1]:
             self._email = email
        else:
             print(f"Erro: E-mail inválido fornecido: {email}")
             # self._email = "" # Ou define um valor padrão/lança exceção

    # --- Polimorfismo (Método base) ---
    def exibir_informacoes(self) -> str:
        """Retorna uma string com as informações básicas da pessoa."""
        return f"Nome: {self.get_nome()}\\nTelefone: {self.get_telefone()}\\nE-mail: {self.get_email()}"

    def __str__(self) -> str:
        """Representação em string do objeto Pessoa."""
        return self.get_nome() # Retorna o nome por padrão

    def __repr__(self) -> str:
        """Representação 'oficial' do objeto."""
        return f"Pessoa(nome='{self.get_nome()}', telefone='{self.get_telefone()}', email='{self.get_email()}')"

