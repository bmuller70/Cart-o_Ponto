import datetime
import config2

while True:
      d = datetime.datetime.now()
      h = datetime.datetime.now()
      data = d.strftime('%d/%m/%y')
      hora = h.strftime('%H:%M')
      print(f'Bem vindo a Pet Salva\n'
            f'Data         Hora\n'
            f'{data} / {hora}')


      rfid = int(input('Aproxime o cartão: '))              #bate o cartao
      acao = config2.bater_ponto()                          #seta a funcao
      if rfid != 5060708090:                                 #O numero serve para entrar no modo de gerenciamento

            #Bate ou atualiza o ponto
            if acao.validar(rfid) == True:                  #Consulta o RFID na base de cadastro de funcionarios
                  a = acao.consulta_m(rfid)                 #Consulta o RFID na lista de funcionarios
                  b = []                                    #Cria a lista onde sera dada a entrada dos dados do funcionario
                  for item in a[0]:
                        b.append(item)
                  a = acao.consulta_r(b[0])                 #Consulta o RFID na base de registros e retorna uma lista de tuplas com todos os registros
                  dia = [i[3] for i in a]                   #Cria uma lista com as datas dos registros
                  if data in dia:                           #Se a data de hoje ja estiver presente no registro
                        acao.registro_s(b[0], data, hora)   #Atualiza o registro do dia com o horario de saida
                        print('Comprovante de Saida')
                        acao.imprimir(rfid, data, hora)
                  else:
                        acao.registro_e(rfid,data,hora)
                        print('Comprovante de entrada')
                        acao.imprimir(rfid, data, hora)

            else: print('Funcionario nao cadastrado')

      else:
            g = 0
            while g != 4:
                  a = config2.gerenciar()
                  print('''Bem Vindo ao gerenciador do ponto.
                  Digite a opção desejada:
                  1 - Cadastrar      2 - Atualizar      3 - Consulta     4 - Sair''')
                  opcao = int(input('>>>'))
                  if opcao == 1:
                      cadastro = a.cadastrar()
                  elif opcao == 2:
                      atualizar = a.atualizar()
                  elif opcao == 3:
                      rfid = int(input('Digite o RFID ou 0 para listar todos: '))
                      consulta = a.consulta(rfid)
                  elif opcao == 4:
                        break