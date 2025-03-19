from datetime import datetime, timezone, timedelta
import textwrap
from abc import ABC, abstractmethod

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []
    
    @property
    def endereco(self):
        return self._endereco
    
    @property
    def contas(self):
        return self._contas
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento
    
    @property
    def cpf(self):
        return self._cpf
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def data_nascimento(self):
        self._data_nascimento

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(self, cliente, numero):
        return self(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        
        if valor > saldo:
            print("\nOperação falhou! Seu saldo atual é insuficiente.")
        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso!")
            return True
        else:
            print("\nOperação falhou! O valor informado é inválido.")
        
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\nDepósito realizado com sucesso!")
            return True
        else:
            print("\nOperação falhou! O valor informado é inválido.")
        
        return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saque=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saque = limite_saque
    
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self._historico.transacoes if transacao["tipo"] == Saque.__name__]
        )
        
        if numero_saques > self._limite_saque:
            print("\nOperação falhou! Você excedeu seu limite de saques diários. Tente novamente outro dia.")
        elif valor > self._limite:
            print("\nOperação falhou! O valor do saque excede o limite.")
        elif valor > self._saldo:
            print("\nOperação falhou! Seu saldo atual é insuficiente.")
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self._agencia}
            C/C:\t\t{self._numero}
            Titular:\t{self._cliente._nome}    
        """

class Historico:
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%s"),
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    
    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():
    menu = """\n
    ========== MENU ==========
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNovo Usuário
    [5]\tNova Conta
    [6]\tListar Contas
    [0]\tSair
    => """
    return input(textwrap.dedent(menu))

def main():
    LIMITE_TRANSACAO = 10
    AGENCIA = "0001"
    
    saldo = 0
    limite = 500
    extrato = ""
    numero_transacao = 0
    usuarios = []
    contas = []
    numero_conta = 1
    data_hora_atual = datetime.now(timezone(timedelta(hours=-3)))
    mascara = "%d/%m/%Y %H:%M:%S"
    data_hora_str = data_hora_atual.strftime(mascara)
    
    while True:
        opcao = float(menu())
        
        if opcao == 1:
            deposito = float(input("Informe o valor do depósito: "))
            saldo, extrato, numero_transacao = depositar(deposito, saldo, extrato, numero_transacao, LIMITE_TRANSACAO, data_hora_str)
            
        elif opcao == 2:
            saque = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_transacao = sacar(
                valor=saque, 
                saldo=saldo, 
                extrato=extrato, 
                limite=limite, 
                numero_transacao=numero_transacao, 
                limite_transacao=LIMITE_TRANSACAO, 
                data_hora_str=data_hora_str
                )
                
        elif opcao == 3:
            mostrar_extrato(saldo, extrato=extrato)
        
        elif opcao == 4:
            criar_usuario(usuarios)
        
        elif opcao == 5:
            numero_conta = criar_conta(contas, AGENCIA, numero_conta, usuarios)
        
        elif opcao == 6:
            listar_contas(contas)
        
        elif opcao == 0:
            break
        
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()