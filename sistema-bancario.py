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
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = float(input(menu))
    
    if opcao == 1:
        deposito = float(input("Informe o valor do depósito: "))
        if deposito > 0:
            saldo += deposito
            extrato += f"Depósito\nValor: R$ {deposito:.2f}\n\n"
            print("Depósito bem sucedido!")
        else:
            print("Valor inválido, por favor tente novamente.")
        
    elif opcao == 2:
        saque = float(input("Informe o valor do saque: "))
        if saque <= saldo and saque <= limite and saque > 0 and numero_saques < LIMITE_SAQUES:
            saldo -= saque
            extrato += f"Saque\nValor: R$ {saque:.2f}\n\n"
            numero_saques += 1
            print("Saque bem sucedido!")
        elif numero_saques >= LIMITE_SAQUES:
            print("Você esgotou seus saques diários! Tente novamente outro dia.")
        elif saque > limite:
            print("Seu saque não pode ultrapassar R$ 500.00. Por favor, insira outro valor.")
        elif saque > saldo:
            print("Seu saldo atual é insuficiente.")
        else:
            print("Valor inválido. Por favor, tente novamente.")
            
    elif opcao == 3:
        print(extrato+f"Saldo atual: R$ {saldo:.2f}")
    
    elif opcao == 0:
        break
    
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")