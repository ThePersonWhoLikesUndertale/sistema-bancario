from datetime import datetime, timezone, timedelta
import textwrap

def menu():
    menu = """\n
    ========== MENU ==========
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [0]\tSair
    => """
    return input(textwrap.dedent(menu))

def depositar(valor, saldo, extrato, numero_transacao, limite_transacao, data_hora_str):
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

def sacar(valor, saldo, extrato, limite, numero_transacao, limite_transacao, data_hora_str):
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

def mostrar_extrato(extrato, saldo):
    print("\n========== EXTRATO ==========")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"Saldo atual: R$ {saldo:.2f}")
    print("=============================")

def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_transacao = 0
    LIMITE_TRANSACAO = 10
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
            saldo, extrato, numero_transacao = sacar(saque, saldo, extrato, limite, numero_transacao, LIMITE_TRANSACAO, data_hora_str)
                
        elif opcao == 3:
            mostrar_extrato(extrato, saldo)
        
        elif opcao == 0:
            break
        
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()