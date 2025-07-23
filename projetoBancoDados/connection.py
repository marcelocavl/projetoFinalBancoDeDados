import pyodbc

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


