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
    opcao = input(menu)
    if opcao == 0:
        break