import psycopg2 as ps
import random


class acessar():
    def __init__(self):
        self.conectar = {
            'postgres': {
                'database': 'c_ponto',
                'user': 'postgres',lo
                'password':'102030',
                'host':'127.0.0.1'
            }
        }


class conectar(acessar):
    def __init__(self):
       acessar.__init__(self)
       try:
           self.conn = ps.connect(**self.conectar['postgres'])
           self.cur = self.conn.cursor()
           #print('Conectado com sucesso.')

       except Exception as e:
           print(f'Conexão falhou {e}')
           exit(1)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.conectar.close()

    @property
    def conect(self):
        return self.conn
    @property
    def cur_sor(self):
        return self.cur

    def commit(self):
        self.conn.commit()

    def fetchall(self):
        return self.cur_sor.fetchall()

    def executar(self, sql, params=None):
        self.cur_sor.execute(sql, params or ())

    def query(self, sql, params=None):
        self.cur_sor.execute(sql, params or ())
        return self.fetchall()

class gerenciar(conectar):
    def __init__(self):
        conectar.__init__(self)

    def cadastrar(self, *args):
        rfid = random.randint(0000,9999)
        nome = str(input('Insira o nome: '))
        func = str(input('Função: '))
        turno = str(input('Turno de trabalho: '))
        local = str(input('Alocação: '))
        try:
            sql = f"INSERT INTO matriculas (rfid,nome,funcao,turno,local) VALUES ({rfid},'{nome}','{func}','{turno}','{local}')"
            self.executar(sql, args)
            self.commit()
        except Exception as e:
            print(f'Erro ao inserir {e}')

    def atualizar(self, *args):
        campo = input('Qual campo deseja atualizar? ')
        colunas = ['nome','funcao','turno','local']
        while campo not in colunas:
            print('Campo invalido')
            campo = input('Digite um campo valido (Nome, Funçao, Turno, Local: ')
        rfid = int(input('Digite o numero RFID: '))
        try:
            sql = f"SELECT {campo} FROM matriculas WHERE rfid={rfid}"
            self.executar(sql, args)
            retorno = self.fetchall()
            if retorno == []:
                print('RFID não cadastrado')
                exit(0)
            up_data = input(f'Digite o novo valor para {campo}: ')
            sql = f"UPDATE matriculas SET {campo}='{up_data}' WHERE rfid={rfid}"
            self.executar(sql, args)
            self.commit()
        except Exception as e:
            print(e)

    def consulta(self, item, *args):
        self.item = item
        if item == 0:
            sql = 'SELECT * from matriculas'
            self.executar(sql)
            retorno = self.fetchall()
            for i in retorno:
                print(f'''RFID: {i[0]}
                    Nome: {i[1]}
                    Funcao: {i[2]}
                    Turno: {i[3]}
                    Local: {i[4]}\n''')
        else:
            sql = f'SELECT * FROM matriculas WHERE rfid={item}'
            self.executar(sql)
            retorno = self.fetchall()
            if retorno == []:
                print('RFID nao cadastrado')
            else:
                print(f'''RFID: {retorno[0][0]}
    Nome: {retorno[0][1]}
    Funcao: {retorno[0][2]}
    Turno: {retorno[0][3]}
    Local: {retorno[0][4]}''')



class bater_ponto(conectar):
    def __init__(self):
        conectar.__init__(self)

    def validar(self, rfid):
        self.rfid = rfid
        sql = f'SELECT rfid FROM matriculas WHERE rfid={rfid}'
        self.executar(sql)
        retorno = self.fetchall()
        try:
            if rfid in retorno[0]:
                return True
        except IndexError:
            print('Funcionario não cadastrado!')

    def imprimir(self, rfid, data, hora):
        self.rfid = rfid
        sql = f'SELECT * FROM matriculas WHERE rfid={rfid}'
        self.executar(sql)
        retorno = self.fetchall()
        print(f'''RFID: {retorno[0][0]}\nNome: {retorno[0][1]}\nFunção: {retorno[0][2]}\nTurno: {retorno[0][3]}\nLocal: {retorno[0][4]}\nDATA:{data}\nHORA: {hora}''')

    def registro_e(self, rfid, data, hora):
        sql = f'SELECT * FROM matriculas WHERE rfid={rfid}'
        self.executar(sql)
        retorno = self.fetchall()
        sql = (f"INSERT INTO registro (rfid,nome,funcao,data,entrada,ativo,local) VALUES({rfid},'{retorno[0][1]}','{retorno[0][2]}','{data}','{hora}',{1}, '{retorno[0][4]}')")
        self.executar(sql)
        self.commit()

    def registro_s(self, rfid, data, hora):
        sql = (f"UPDATE registro SET saida='{hora}', ativo=0 WHERE rfid={rfid} AND data='{data}'")
        self.executar(sql)
        self.commit()

    def consulta_m(self, rfid):
        self.rfid = rfid
        sql = f'SELECT * FROM matriculas WHERE rfid={rfid}'
        self.executar(sql)
        retorno = self.fetchall()
        return retorno

    def consulta_r(self, rfid):
        self.rfid = rfid
        sql = f'SELECT * FROM registro WHERE rfid={rfid}'
        self.executar(sql)
        retorno = self.fetchall()
        return retorno