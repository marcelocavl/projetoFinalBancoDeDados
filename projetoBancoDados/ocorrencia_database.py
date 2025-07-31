from connection import *

# ------------------------------- CRUD ocorrências de perda -------------------------------

# Adicionar ocorrência de perda ao banco de dados
def insert_ocorrencia_database(tipo_objeto, data_perdido, local_perdido, pessoa_perdeu):
    from connection import cursor_var
    from connection import connection

    pessoa_sql = f"'{pessoa_perdeu}'" if pessoa_perdeu else "NULL"
    local_sql = f"'{local_perdido}'" if local_perdido else "NULL"
    comando = f"""INSERT INTO Ocorrencia_Perda(Tipo_objeto, Data_perdido, Local_perdido, Pessoa_perdeu)
                  VALUE
                  ('{tipo_objeto}', '{data_perdido}', {local_sql}, {pessoa_sql})"""

    try:
        cursor_var.execute(comando)
        cursor_var.commit()
        print("Inserção de ocorrência de perda bem sucedida.")
    except Exception as e:
        print(f"Erro ao inserir ocorrência: {e}")
        cursor_var.rollback()

# Remover ocorrência de perda do banco de dados
def remove_ocorrencia_database(ocorrencia_id):
    from connection import cursor_var
    from connection import connection

    comando = f"""DELETE FROM Ocorrencia_Perda WHERE OcorrenciaID = {ocorrencia_id}"""

    try:
        cursor_var.execute(comando)
        cursor_var.commit()
        if cursor_var.rowcount > 0:
            print(f"Ocorrência com ID {ocorrencia_id} removida com sucesso.")
        else:
            print(f"Nenhuma ocorrência encontrada com o ID {ocorrencia_id}.")
    except Exception as e:
        print(f"Erro ao remover ocorrência: {e}")
        cursor_var.rollback()

# Editar campos da ocorrência de perda no banco de dados
def update_ocorrencia_database(ocorrencia_id, campo_a_editar, novo_valor):
    from connection import cursor_var
    from connection import connection

    campos_permitidos = {
        "tipo_objeto": "Tipo_objeto",
        "data_perdido": "Data_perdido",
        "local_perdido": "Local_perdido",
        "pessoa_perdeu": "Pessoa_perdeu"
    }

    campo_db = campos_permitidos.get(campo_a_editar.lower())

    if not campo_db:
        print("Campo inválido ou não editável. Os campos editáveis são: tipo_objeto, data_perdido, local_perdido, pessoa_perdeu.")
        return

    if novo_valor is None or str(novo_valor).strip() == "":
        valor_para_sql = "NULL"
    else:
        valor_para_sql = f"'{novo_valor}'"

    comando = f"""UPDATE Ocorrencia_Perda SET {campo_db} = {valor_para_sql} WHERE OcorrenciaID = {ocorrencia_id}"""

    try:
        cursor_var.execute(comando)
        cursor_var.commit()
        if cursor_var.rowcount > 0:
            print(f"Ocorrência com ID {ocorrencia_id} atualizada com sucesso no campo '{campo_a_editar}'.")
        else:
            print(f"Nenhuma ocorrência encontrada com o ID {ocorrencia_id} para atualizar.")
    except Exception as e:
        print(f"Erro ao atualizar ocorrência: {e}")
        cursor_var.rollback()

# Ler e imprimir todas as ocorrências de perda
def read_and_print_ocorrencias():
    from connection import cursor_var
    from connection import connection

    comando = """SELECT * FROM Ocorrencia_Perda"""

    try:
        cursor_var.execute(comando)
        registros = cursor_var.fetchall()

        if not registros:
            print("Nenhuma ocorrência encontrada no banco de dados.")
            return

        print("\n--- Lista de Ocorrências de Perda ---")
        print(f"{'ID':<5} | {'Tipo Objeto':<20} | {'Data Perdido':<15} | {'Local Perdido':<20} | {'Pessoa Perdeu':<15}")
        print("-" * 80)

        for registro in registros:
            ocorrencia_id = registro[0]
            tipo_objeto = registro[1]
            data_perdido = registro[2].strftime("%Y-%m-%d") if hasattr(registro[2], 'strftime') else str(registro[2])
            local_perdido = registro[3] if registro[3] is not None else "N/A"
            pessoa_perdeu = registro[4] if registro[4] is not None else "N/A"
            print(f"{ocorrencia_id:<5} | {tipo_objeto:<20} | {data_perdido:<15} | {local_perdido:<20} | {pessoa_perdeu:<15}")

        print("\nLeitura de ocorrências finalizada.")

    except Exception as e:
        print(f"Erro ao ler ocorrências do banco de dados: {e}")
        cursor_var.rollback()

# Ler e imprimir uma ocorrência específica
def read_and_print_unica_ocorrencia(ocorrencia_id):
    from connection import cursor_var
    from connection import connection

    comando = f"""SELECT * FROM Ocorrencia_Perda WHERE OcorrenciaID = {ocorrencia_id}"""

    try:
        cursor_var.execute(comando)
        registro = cursor_var.fetchone()

        if not registro:
            print(f"Nenhuma ocorrência encontrada com o ID {ocorrencia_id}.")
            return

        print(f"\n--- Detalhes da Ocorrência (ID: {ocorrencia_id}) ---")
        print(f"{'Campo':<20} | {'Valor'}")
        print("-" * 50)

        colunas = [
            "ID da Ocorrência", "Tipo Objeto", "Data Perdido",
            "Local Perdido", "Pessoa Perdeu"
        ]

        valores = list(registro)
        if hasattr(valores[2], 'strftime'):
            valores[2] = valores[2].strftime("%Y-%m-%d")
        else:
            valores[2] = str(valores[2])

        valores[3] = valores[3] if valores[3] is not None else "N/A"
        valores[4] = valores[4] if valores[4] is not None else "N/A"

        for i, campo in enumerate(colunas):
            print(f"{campo:<20} | {valores[i]}")

        print("\nLeitura de ocorrência finalizada.")

    except Exception as e:
        print(f"Erro ao ler ocorrência do banco de dados: {e}")
        cursor_var.rollback()