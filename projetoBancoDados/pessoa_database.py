#from connection import cursor_var


def insert_pessoa_database(Pmatricula,Pnome,Pcontato):
		from connection import cursor_var
		from connection import connection
		comando= f"""INSERT INTO Pessoa(PessoaMatricula,Pnome,Contato)
								 VALUE
								 ('{Pmatricula}','{Pnome}','{Pcontato}')"""
		cursor_var.execute(comando)
		cursor_var.commit()
		print("inserção bem sucedida")

def update_pessoa_database(pessoa_matricula,campo,novo_valor):
		from connection import cursor_var
		from connection import connection
		comando=f"""UPDATE Pessoa SET {campo} = '{novo_valor}' WHERE PessoaMatricula = {pessoa_matricula}"""
		cursor_var.execute(comando)
		cursor_var.commit()
	
		print("update bem sucedido")


def remove_pessoa_database(Pmatricula):
	from connection import cursor_var
	from connection import connection
	comando=f"""DELETE FROM Pessoa WHERE PessoaMatricula='{Pmatricula}'"""
	cursor_var.execute(comando)
	cursor_var.commit()
	print("remoção bem sucedida")
     

