import pyodbc
from datetime import datetime

conection=None
cursor=None

def connect_database():
	global conection
	global cursor
	data_conection=(	
		"Driver={MariaDB ODBC 3.1 Driver};"
		"Server=localhost;"
		"Database=AchadosEPerdidos;"
		"UID=root;"
		"PWD=123;"
		"Port=3306;"
	)
	conection=pyodbc.connect(data_conection);
	cursor=conection.cursor()
	print("conexão bem sucedida");


def insert_pessoa_database(Pmatricula,Pnome,Pcontato):
		global conection
		global cursor
		comando= f"""INSERT INTO Pessoa(PessoaMatricula,Pnome,Contato)
								 VALUE
								 ('{Pmatricula}','{Pnome}','{Pcontato}')"""
		cursor.execute(comando)
		cursor.commit()
		print("inserção bem sucedida")

def remove_pessoa_database(Pmatricula):
	global conection
	global cursor
	comando=f"""DELETE FROM Pessoa WHERE PessoaMatricula='{Pmatricula}'"""
	cursor.execute(comando)
	cursor.commit()
	print("remoção bem sucedida")
     

# ------------------------------- CRUD objetos -------------------------------

def insert_objeto_database(Otitulo, Ocor, Odescricao, Olocal_encontrado, Opessoa_entregou=None, Oreinvidicado=False):
    global conection
    global cursor

    data_encontrado = datetime.now().strftime('%Y-%m-%d')
    cor_sql = f"'{Ocor}'" if Ocor else "NULL"
    pessoa_entregou_sql = f"'{Opessoa_entregou}'" if Opessoa_entregou else "NULL"
    reinvidicado_sql = 1 if Oreinvidicado else 0
    comando = f"""INSERT INTO Objeto(Titulo, Cor, Descricao, Data_encontrado, Local_encontrado, Pessoa_entregou, Reinvidicado)
                  VALUE
                  ('{Otitulo}', {cor_sql}, '{Odescricao}', '{data_encontrado}', '{Olocal_encontrado}', {pessoa_entregou_sql}, {reinvidicado_sql})"""

    try:
        cursor.execute(comando)
        conection.commit()
        print("Inserção de objeto bem sucedida.")
    except Exception as e:
        print(f"Erro ao inserir objeto: {e}")
        conection.rollback()
        
def remove_objeto_database(ObjetoID):
    global conection
    global cursor

    comando = f"""DELETE FROM Objeto WHERE ObjetoID = {ObjetoID}"""

    try:
        cursor.execute(comando)
        conection.commit()
        if cursor.rowcount > 0:
            print(f"Objeto com ID {ObjetoID} removido com sucesso.")
        else:
            print(f"Nenhum objeto encontrado com o ID {ObjetoID}.")
    except Exception as e:
        print(f"Erro ao remover objeto: {e}")
        conection.rollback()

