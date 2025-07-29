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

# Adicionar objeto ao banco de dados
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

# Remover objeto do banco de dados        
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

# Editar campos do objeto no banco de dados
def update_objeto_database(objeto_id, campo_a_editar, novo_valor):
    global conection
    global cursor

    campos_permitidos = {
        "titulo": "Titulo",
        "cor": "Cor",
        "descricao": "Descricao",
        "local_encontrado": "Local_encontrado",
        "pessoa_entregou": "Pessoa_entregou"
    }

    campo_db = campos_permitidos.get(campo_a_editar.lower())

    if not campo_db:
        print("Campo inválido ou não editável. Os campos editáveis são: titulo, cor, descricao, local_encontrado, pessoa_entregou.")
        return

    if campo_db in ["Cor", "Pessoa_entregou"] and (novo_valor is None or str(novo_valor).strip() == ""):
        valor_para_sql = "NULL"
    else:
        valor_para_sql = f"'{novo_valor}'"

    comando = f"""UPDATE Objeto SET {campo_db} = {valor_para_sql} WHERE ObjetoID = {objeto_id}"""

    try:
        cursor.execute(comando)
        conection.commit()
        if cursor.rowcount > 0:
            print(f"Objeto com ID {objeto_id} atualizado com sucesso no campo '{campo_a_editar}'.")
        else:
            print(f"Nenhum objeto encontrado com o ID {objeto_id} para atualizar.")
    except Exception as e:
        print(f"Erro ao atualizar objeto: {e}")
        conection.rollback()

# Marcar objeto como reivindicado      
def set_objeto_reivindicado(objeto_id):
    global conection
    global cursor

    comando = f"""UPDATE Objeto SET Reinvidicado = TRUE WHERE ObjetoID = {objeto_id}"""

    try:
        cursor.execute(comando)
        conection.commit()
        if cursor.rowcount > 0:
            print(f"Objeto com ID {objeto_id} marcado como 'Reivindicado'.")
        else:
            print(f"Nenhum objeto encontrado com o ID {objeto_id} para marcar como 'Reivindicado'.")
    except Exception as e:
        print(f"Erro ao marcar objeto como 'Reivindicado': {e}")
        conection.rollback()

# Ler e imprimir todos os objetos do banco de dados        
def read_and_print_objetos():
    global conection
    global cursor

    comando = """SELECT * FROM Objeto"""

    try:
        cursor.execute(comando)
        registros = cursor.fetchall()

        if not registros:
            print("Nenhum objeto encontrado no banco de dados.")
            return

        print("\n--- Lista de Objetos Perdidos ---")
        print(f"{'ID':<5} | {'Título':<25} | {'Cor':<15} | {'Descrição':<30} | {'Data Encontrado':<20} | {'Local':<20} | {'Entregue Por':<15} | {'Reivindicado':<12}")
        print("-" * 170)

        for registro in registros:
            objeto_id = registro[0]
            titulo = registro[1]
            cor = registro[2] if registro[2] is not None else "N/A"
            descricao = registro[3]
            data_encontrado = registro[4].strftime("%Y-%m-%d %H:%M:%S") if hasattr(registro[4], 'strftime') else str(registro[4]) # Formata data
            local_encontrado = registro[5]
            pessoa_entregou = registro[6] if registro[6] is not None else "N/A"
            reinvidicado = "Sim" if registro[7] else "Não"

            print(f"{objeto_id:<5} | {titulo:<25} | {cor:<15} | {descricao:<30} | {data_encontrado:<20} | {local_encontrado:<20} | {pessoa_entregou:<15} | {reinvidicado:<12}")

        print("\nLeitura de objetos finalizada.")

    except Exception as e:
        print(f"Erro ao ler objetos do banco de dados: {e}")
        conection.rollback()

def read_and_print_unico_objeto(objeto_id):
    global conection
    global cursor

    comando = f"""SELECT * FROM Objeto WHERE ObjetoID = {objeto_id}"""

    try:
        cursor.execute(comando)
        registro = cursor.fetchone()

        if not registro:
            print(f"Nenhum objeto encontrado com o ID {objeto_id}.")
            return

        print(f"\n--- Detalhes do Objeto (ID: {objeto_id}) ---")
        print(f"{'Campo':<20} | {'Valor'}")
        print("-" * 50)

        colunas = [
            "ID do Objeto", "Título", "Cor", "Descrição",
            "Data Encontrado", "Local Encontrado", "Entregue Por", "Reivindicado"
        ]

        valores = list(registro)
        if hasattr(valores[4], 'strftime'):
            valores[4] = valores[4].strftime("%Y-%m-%d %H:%M:%S")
        else:
            valores[4] = str(valores[4])

        valores[2] = valores[2] if valores[2] is not None else "N/A"
        valores[6] = valores[6] if valores[6] is not None else "N/A"
        valores[7] = "Sim" if valores[7] else "Não"

        for i, campo in enumerate(colunas):
            print(f"{campo:<20} | {valores[i]}")

        print("\nLeitura de objeto finalizada.")

    except Exception as e:
        print(f"Erro ao ler objeto do banco de dados: {e}")
        conection.rollback()