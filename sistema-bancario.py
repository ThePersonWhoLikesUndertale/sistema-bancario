from datetime import datetime, timezone, timedelta

menu = """
Bem-vindo! O que deseja fazer?
      
Opções:
[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair

=> """
saldo = 0
limite = 500
extrato = ""
numero_transacao = 0
LIMITE_TRANSACAO = 10
data_hora_atual = datetime.now(timezone(timedelta(hours=-3)))
mascara = "%d/%m/%Y %H:%M"
data_hora_str = data_hora_atual.strftime(mascara)

while True:
    opcao = float(input(menu))
    
    if opcao == 1:
        deposito = float(input("Informe o valor do depósito: "))
        if deposito > 0 and numero_transacao < LIMITE_TRANSACAO:
            saldo += deposito
            extrato += f"Depósito\nValor: R$ {deposito:.2f}\nData e Hora: {data_hora_str}\n\n"
            numero_transacao += 1
            print("Depósito bem sucedido!")
        elif numero_transacao >= LIMITE_TRANSACAO:
            print("Você esgotou suas transações diárias! Tente novamente outro dia.")
        else:
            print("Valor inválido, por favor tente novamente.")
        
    elif opcao == 2:
        saque = float(input("Informe o valor do saque: "))
        if saque <= saldo and saque <= limite and saque > 0 and numero_transacao < LIMITE_TRANSACAO:
            saldo -= saque
            extrato += f"Saque\nValor: R$ {saque:.2f}\nData e Hora: {data_hora_str}\n\n"
            numero_transacao += 1
            print("Saque bem sucedido!")
        elif numero_transacao >= LIMITE_TRANSACAO:
            print("Você esgotou suas transações diárias! Tente novamente outro dia.")
        elif saque > limite:
            print("Seu saque não pode ultrapassar R$ 500.00. Por favor, insira outro valor.")
        elif saque > saldo:
            print("Seu saldo atual é insuficiente.")
        else:
            print("Valor inválido. Por favor, tente novamente.")
            
    elif opcao == 3:
        print("\n========== EXTRATO ==========")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"Saldo atual: R$ {saldo:.2f}")
        print("=============================")
    
    elif opcao == 0:
        break
    
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")