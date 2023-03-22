import config2

a = config2.gerenciar()
print('''Bem Vindo ao gerenciador do ponto.
Digite a opção desejada:
1 - Cadastrar      2 - Atualizar      3 - Consulta''')
opcao = int(input('>>>'))
if opcao == 1:
    cadastro = a.cadastrar()
elif opcao == 2:
    atualizar = a.atualizar()
elif opcao == 3:
    rfid = int(input('Digite o RFID ou 0 para listar todos: '))
    consulta = a.consulta(rfid)


