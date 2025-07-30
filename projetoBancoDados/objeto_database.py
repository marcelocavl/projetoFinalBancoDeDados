from connection import *

# ------------------------------- CRUD objetos -------------------------------
# Adicionar objeto ao banco de dados
def insert_objeto_database(Otitulo, Ocor, Odescricao, Olocal_encontrado, Opessoa_entregou=None, Oreinvidicado=False):
		from connection import cursor_var
		from connection import connection


    data_encontrado = datetime.now().strftime('%Y-%m-%d')
    cor_sql = f"'{Ocor}'" if Ocor else "NULL"
    pessoa_entregou_sql = f"'{Opessoa_entregou}'" if Opessoa_entregou else "NULL"
    reinvidicado_sql = 1 if Oreinvidicado else 0
    comando = f"""INSERT INTO Objeto(Titulo, Cor, Descricao, Data_encontrado, Local_encontrado, Pessoa_entregou, Reinvidicado)
                  VALUE
                  ('{Otitulo}', {cor_sql}, '{Odescricao}', '{data_encontrado}', '{Olocal_encontrado}', {pessoa_entregou_sql}, {reinvidicado_sql})"""

    try:
        cursor_var.execute(comando)
        connection.commit()
        print("Inserção de objeto bem sucedida.")
    except Exception as e:
        print(f"Erro ao inserir objeto: {e}")
        connection.rollback()

# Remover objeto do banco de dados        
def remove_objeto_database(ObjetoID):
		from connection import cursor_var
		from connection import connection


    comando = f"""DELETE FROM Objeto WHERE ObjetoID = {ObjetoID}"""

    try:
        cursor_var.execute(comando)
        connection.commit()
        if cursor_var.rowcount > 0:
            print(f"Objeto com ID {ObjetoID} removido com sucesso.")
        else:
            print(f"Nenhum objeto encontrado com o ID {ObjetoID}.")
    except Exception as e:
        print(f"Erro ao remover objeto: {e}")
        connection.rollback()

# Editar campos do objeto no banco de dados
def update_objeto_database(objeto_id, campo_a_editar, novo_valor):
		from connection import cursor_var
		from connection import connection


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
        cursor_var.execute(comando)
        connection.commit()
        if cursor_var.rowcount > 0:
            print(f"Objeto com ID {objeto_id} atualizado com sucesso no campo '{campo_a_editar}'.")
        else:
            print(f"Nenhum objeto encontrado com o ID {objeto_id} para atualizar.")
    except Exception as e:
        print(f"Erro ao atualizar objeto: {e}")
        connection.rollback()

# Marcar objeto como reivindicado      
def set_objeto_reivindicado(objeto_id):
		from connection import cursor_var
		from connection import connection


    comando = f"""UPDATE Objeto SET Reinvidicado = TRUE WHERE ObjetoID = {objeto_id}"""

    try:
        cursor_var.execute(comando)
        connection.commit()
        if cursor_var.rowcount > 0:
            print(f"Objeto com ID {objeto_id} marcado como 'Reivindicado'.")
        else:
            print(f"Nenhum objeto encontrado com o ID {objeto_id} para marcar como 'Reivindicado'.")
    except Exception as e:
        print(f"Erro ao marcar objeto como 'Reivindicado': {e}")
        connection.rollback()

# Ler e imprimir todos os objetos do banco de dados        
def read_and_print_objetos():
		from connection import cursor_var
		from connection import connection


    comando = """SELECT * FROM Objeto"""

    try:
        cursor_var.execute(comando)
        registros = cursor_var.fetchall()

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
        connection.rollback()
