#from connection import cursor_var

# ------------------------------- CRUD pessoas -------------------------------

# Adicionar pessoa ao banco de dados
def insert_pessoa_database(Pmatricula,Pnome,Pcontato):
		from connection import cursor_var
		from connection import connection
		comando= f"""INSERT INTO Pessoa(PessoaMatricula,Pnome,Contato)
								 VALUE
								 ('{Pmatricula}','{Pnome}','{Pcontato}')"""
		
		try:
			cursor_var.execute(comando)
			cursor_var.commit()
			print("Inserção de pessoa bem sucedida.")
		except Exception as e:
			print(f"Erro ao inserir pessoa: {e}")
			cursor_var.rollback()

# Atualizar campos da pessoa no banco de dados
def update_pessoa_database(pessoa_matricula, campo_a_editar, novo_valor):
		from connection import cursor_var
		from connection import connection
		campos_permitidos = {
			"pnome": "Pnome",
			"contato": "Contato"
		}
		campo_db = campos_permitidos.get(campo_a_editar.lower())
		if not campo_db:
			print("Campo inválido ou não editável. Os campos editáveis são: Nome, Contato.")
			return
		if novo_valor.strip() == "":
			valor_para_sql = "NULL"
		else:
			valor_para_sql = f"'{novo_valor}'"
		
		try:
			comando = f"""UPDATE Pessoa SET {campo_db} = {valor_para_sql} WHERE PessoaMatricula = '{pessoa_matricula}'"""
			cursor_var.execute(comando)
			cursor_var.commit()
			if cursor_var.rowcount > 0:
				print("Atualização bem sucedida")
			else:
				print("Nenhuma pessoa encontrada com a matrícula fornecida.")
		except Exception as e:
			print(f"Erro ao atualizar pessoa: {e}")
			cursor_var.rollback()
		
# Remover pessoa do banco de dados		
def remove_pessoa_database(Pmatricula):
	from connection import cursor_var
	from connection import connection
	comando=f"""DELETE FROM Pessoa WHERE PessoaMatricula='{Pmatricula}'"""
	try:
		cursor_var.execute(comando)
		cursor_var.commit()
		if cursor_var.rowcount > 0:
			print(f"Pessoa com matrícula {Pmatricula} removida com sucesso.")
		else:
			print(f"Nenhuma pessoa encontrada com a matrícula {Pmatricula}.")
	except Exception as e:
		print(f"Erro ao remover pessoa: {e}")
		cursor_var.rollback()
     
# Ler e imprimir uma pessoa específica
def read_and_print_unica_pessoa(pessoa_matricula):
    from connection import cursor_var
    from connection import connection

    comando = f"""SELECT * FROM Pessoa WHERE PessoaMatricula = '{pessoa_matricula}'"""

    try:
        cursor_var.execute(comando)
        registro = cursor_var.fetchone()

        if not registro:
            print(f"Nenhuma pessoa encontrada com a matrícula {pessoa_matricula}.")
            return

        print(f"\n--- Detalhes da Pessoa (Matrícula: {pessoa_matricula}) ---")
        print(f"{'Campo':<15} | {'Valor'}")
        print("-" * 40)

        colunas = ["Matrícula", "Nome", "Contato"]
        for i, campo in enumerate(colunas):
            print(f"{campo:<15} | {registro[i]}")

        print("\nLeitura de pessoa finalizada.")

    except Exception as e:
        print(f"Erro ao ler pessoa do banco de dados: {e}")
        cursor_var.rollback()
	
# Ler e imprimir todas as pessoas
def read_and_print_pessoas():
    from connection import cursor_var
    from connection import connection

    comando = """SELECT * FROM Pessoa"""

    try:
        cursor_var.execute(comando)
        registros = cursor_var.fetchall()

        if not registros:
            print("Nenhuma pessoa encontrada no banco de dados.")
            return

        print("\n--- Lista de Pessoas ---")
        print(f"{'Matrícula':<15} | {'Nome':<25} | {'Contato':<25}")
        print("-" * 70)

        for registro in registros:
            matricula = registro[0]
            nome = registro[1]
            contato = registro[2]
            print(f"{matricula:<15} | {nome:<25} | {contato:<25}")

        print("\nLeitura de pessoas finalizada.")

    except Exception as e:
        print(f"Erro ao ler pessoas do banco de dados: {e}")
        cursor_var.rollback()
