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
    def numero(self):
        return self._numero
    
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
    def __init__(self, numero, cliente, limite=500, limite_saque=2):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saque = limite_saque
    
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
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
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}    
        """

class Historico:
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now(timezone(timedelta(hours=-3))).strftime("%d/%m/%Y %H:%M:%S"),
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
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def login():
    menu = """\n
    ========== MENU ==========
    [1]\tLogin
    [2]\tNovo Usuário
    [3]\tNova Conta
    [4]\tListar Contas
    [0]\tSair
    => """
    return input(textwrap.dedent(menu))

def menu():
    menu = """\n
    ========== MENU ==========
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [0]\tVoltar
    => """
    return input(textwrap.dedent(menu))

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario.cpf == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_usuario(usuarios):
    cpf = float(input("Informe seu CPF (Só números): "))
    
    if len(str(cpf)) < 11:
        print("\nO CPF não pode ter menos de 11 dígitos. Por favor, tente novamente.")
        return
    
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        print("\nEsse usuário já existe!")
        return
    
    nome = input("Informe seu nome completo: ")
    data_nascimento = input("Informe sua data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe seu endereço (logradouro, número - bairro - cidade/sigla estado): ")
    
    usuarios.append(PessoaFisica(cpf, nome, data_nascimento, endereco))
    
    print("\nUsuário criado com sucesso!")

def filtrar_conta(numero, contas):
    contas_filtradas = [conta for conta in contas if conta.numero == numero]
    return contas_filtradas[0] if contas_filtradas else None

def criar_conta(numero, usuarios):
    cpf = float(input("Informe seu CPF (Só números): "))
    usuario = filtrar_usuario(cpf, usuarios)
    
    if not usuario:
        print("\nEsse usuário não existe, por favor tente novamente.")
        return numero
    else:
        usuario.adicionar_conta(ContaCorrente(numero, usuario))
        numero += 1
        print("\nConta criada com sucesso!")
        return numero

def listar_contas(usuarios):
    cpf = float(input("Informe seu CPF (Só números): "))
    usuario = filtrar_usuario(cpf, usuarios)
    
    if not usuario:
        print("\nEsse usuário não existe, por favor tente novamente.")
    else:
        for conta in usuario.contas:
            print("=" * 85)
            print(textwrap.dedent(conta.__str__()))

def mostrar_extrato(conta):
    print("\n========== EXTRATO ==========")
    if conta.historico.transacoes == []:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in conta.historico.transacoes:
            print(f"Tipo: {transacao["tipo"]}\nValor: R$ {transacao["valor"]:.2f}\nData e Hora: {transacao["data"]}\n\n")
    print(f"Saldo atual: R$ {conta.saldo:.2f}")
    print("=============================")

def main():
    usuarios = []
    numero_conta = 1
    
    while True:
        opcao = float(login())
        
        if opcao == 1:
            cpf = float(input("Informe seu CPF (Só números): "))
            usuario = filtrar_usuario(cpf, usuarios)
    
            if not usuario:
                print("\nEsse usuário não existe, por favor tente novamente.")
                pass
            elif usuario.contas == []:
                print("\nVocê ainda não tem uma conta! Tente criar uma nova.")
            else:
                conta_numero = float(input("Informe o número da conta que deseja usar: "))
                conta = filtrar_conta(conta_numero, usuario.contas)
                
                if not conta:
                    print("\nEssa conta não existe, por favor tente novamente.")
                else:
                    while True:
                        opcao2 = float(menu())
                
                        if opcao2 == 1:
                            valor = float(input("Digite o valor que deseja depositar: "))
                            Deposito(valor).registrar(conta)
                
                        elif opcao2 == 2:
                            valor = float(input("Digite o valor que deseja sacar: "))
                            Saque(valor).registrar(conta)
                
                        elif opcao2 == 3:
                            mostrar_extrato(conta)
                
                        elif opcao2 == 0:
                            break
                
                        else:
                            print("\nOperação inválida! Por favor, selecione novamente a operação desejada.")
        
        elif opcao == 2:
            criar_usuario(usuarios)
        
        elif opcao == 3:
            numero_conta = criar_conta(numero_conta, usuarios)
        
        elif opcao == 4:
            listar_contas(usuarios)
        
        elif opcao == 0:
            break
        
        else:
            print("\nOperação inválida! Por favor, selecione novamente a operação desejada.")

main()