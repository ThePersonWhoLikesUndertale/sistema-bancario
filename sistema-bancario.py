from datetime import datetime, timezone, timedelta
import textwrap

class Cliente:
    def __init__(self, cpf, nome, data_nascimento, endereco, contas):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.contas = contas
    
    def realizar_transacao(self, conta, transacao):
        pass
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class Conta:
    def __init__(self, saldo, numero, agencia, cliente, historico, limite, limite_saque):
        self.saldo = saldo
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = historico
        self.limite = limite
        self.limite_saque = limite_saque
    
    def nova_conta(self, cliente, numero):
        pass
    
    def sacar(self, valor):
        pass
    
    def depositar(self, valor):
        pass

class Transacao:
    def registrar(self, conta):
        pass

class Historico:
    def adicionar_transacao(self, transacao):
        pass

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

def depositar(valor, saldo, extrato, numero_transacao, limite_transacao, data_hora_str, /):
    if valor > 0 and numero_transacao < limite_transacao:
        saldo += valor
        extrato += f"Depósito\nValor: R$ {valor:.2f}\nData e Hora: {data_hora_str}\n\n"
        numero_transacao += 1
        print("Depósito bem sucedido!")
    elif numero_transacao >= limite_transacao:
        print("Você esgotou suas transações diárias! Tente novamente outro dia.")
    else:
        print("Valor inválido, por favor tente novamente.")
    
    return saldo, extrato, numero_transacao

def sacar(*, valor, saldo, extrato, limite, numero_transacao, limite_transacao, data_hora_str):
    if valor <= saldo and valor <= limite and valor > 0 and numero_transacao < limite_transacao:
        saldo -= valor
        extrato += f"Saque\nValor: R$ {valor:.2f}\nData e Hora: {data_hora_str}\n\n"
        numero_transacao += 1
        print("Saque bem sucedido!")
    elif numero_transacao >= limite_transacao:
        print("Você esgotou suas transações diárias! Tente novamente outro dia.")
    elif valor > limite:
        print("Seu saque não pode ultrapassar R$ 500.00. Por favor, insira outro valor.")
    elif valor > saldo:
        print("Seu saldo atual é insuficiente.")
    else:
        print("Valor inválido. Por favor, tente novamente.")
    
    return saldo, extrato, numero_transacao

def mostrar_extrato(saldo, /, *, extrato):
    print("\n========== EXTRATO ==========")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"Saldo atual: R$ {saldo:.2f}")
    print("=============================")

def criar_usuario(usuarios):
    cpf = float(input("Informe seu CPF (Só números): "))
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        print("Esse usuário já existe!")
        return
    
    nome = input("Informe seu nome completo: ")
    data_nascimento = input("Informe sua data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe seu endereço (logradouro, número - bairro - cidade/sigla estado): ")
    
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    
    print("Usuário criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(contas, agencia, numero_conta, usuarios):
    cpf = float(input("Informe seu CPF (Só números): "))
    usuario = filtrar_usuario(cpf, usuarios)
    
    if not usuario:
        print("Esse usuário não existe, por favor tente novamente.")
        return numero_conta
    
    contas.append({"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario})
    numero_conta += 1
    
    print("Conta criada com sucesso!")
    return numero_conta

def listar_contas(contas):
    for conta in contas:
        linha = f"""\n
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

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