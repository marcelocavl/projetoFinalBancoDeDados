from datetime import datetime

# ------------------------------- CRUD Reivindicações -------------------------------

# Adicionar uma nova reivindicação ao banco de dados
def insert_reivindicacao_database(objeto_reivindicado_id, pessoa_retirou, ocorrencia_id=None):
    """
    Insere uma nova reivindicação no banco de dados.
    Ao inserir, também marca o objeto correspondente como reivindicado.

    Args:
        objeto_reivindicado_id (int): O ID do objeto que está sendo reivindicado.
        pessoa_retirou (str): A matrícula da pessoa que retirou o objeto.
        ocorrencia_id (int, optional): O ID da ocorrência de perda associada. Defaults to None.
    """

    # A importação foi movida para dentro da função para evitar conflitos
    from connection import get_connection, get_cursor
    connection = get_connection()
    cursor_var = get_cursor()
    from objeto_database import set_objeto_reivindicado
    data_retirada = datetime.now().strftime('%Y-%m-%d')
    
    # Trata o caso de ocorrencia_id ser opcional
    ocorrencia_sql = f"'{ocorrencia_id}'" if ocorrencia_id else "NULL"
    pessoa_retirou_sql = f"'{pessoa_retirou}'" if pessoa_retirou else "NULL"

    comando = f"""INSERT INTO Reivindicacao(Objeto_reivindicado_ID, Pessoa_retirou, Ocorrencia_ID, Data_retirada)
                  VALUES
                  ({objeto_reivindicado_id}, {pessoa_retirou_sql}, {ocorrencia_sql}, '{data_retirada}')"""

    try:
        cursor_var.execute(comando)
        connection.commit()
        print(f"Inserção de reivindicação para o objeto ID {objeto_reivindicado_id} bem sucedida.")
        
        # Após criar a reivindicação, marca o objeto como reivindicado na tabela Objeto
        set_objeto_reivindicado(objeto_reivindicado_id)

    except Exception as e:
        print(f"Erro ao inserir reivindicação: {e}")
        connection.rollback()

# Remover uma reivindicação do banco de dados
def remove_reivindicacao_database(reivindicacao_id):
    """
    Remove uma reivindicação do banco de dados usando seu ID.

    Args:
        reivindicacao_id (int): O ID da reivindicação a ser removida.
    """
    from connection import get_connection, get_cursor
    connection = get_connection()
    cursor_var = get_cursor()
    comando = f"""DELETE FROM Reivindicacao WHERE ReivindicacaoID = {reivindicacao_id}"""

    try:
        cursor_var.execute(comando)
        connection.commit()
        if cursor_var.rowcount > 0:
            print(f"Reivindicação com ID {reivindicacao_id} removida com sucesso.")
        else:
            print(f"Nenhuma reivindicação encontrada com o ID {reivindicacao_id}.")
    except Exception as e:
        print(f"Erro ao remover reivindicação: {e}")
        connection.rollback()

# Editar campos de uma reivindicação no banco de dados
def update_reivindicacao_database(reivindicacao_id, campo_a_editar, novo_valor):
    """
    Atualiza um campo específico de uma reivindicação.

    Args:
        reivindicacao_id (int): O ID da reivindicação a ser atualizada.
        campo_a_editar (str): O nome do campo a ser editado ('pessoa_retirou' ou 'ocorrencia_id').
        novo_valor (any): O novo valor para o campo.
    """
    from connection import get_connection, get_cursor
    connection = get_connection()
    cursor_var = get_cursor()
    campos_permitidos = {
        "pessoa_retirou": "Pessoa_retirou",
        "ocorrencia_id": "Ocorrencia_ID"
    }

    campo_db = campos_permitidos.get(campo_a_editar.lower())

    if not campo_db:
        print("Campo inválido ou não editável. Os campos editáveis são: pessoa_retirou, ocorrencia_id.")
        return

    # Formata o valor para SQL, tratando strings e valores nulos
    if novo_valor is None or str(novo_valor).strip() == "":
        valor_para_sql = "NULL"
    else:
        valor_para_sql = f"'{novo_valor}'"

    comando = f"""UPDATE Reivindicacao SET {campo_db} = {valor_para_sql} WHERE ReivindicacaoID = {reivindicacao_id}"""
  

    try:
        cursor_var.execute(comando)
        connection.commit()
        if cursor_var.rowcount > 0:
            print(f"Reivindicação com ID {reivindicacao_id} atualizada com sucesso no campo '{campo_a_editar}'.")
        else:
            print(f"Nenhuma reivindicação encontrada com o ID {reivindicacao_id} para atualizar.")
    except Exception as e:
        print(f"Erro ao atualizar reivindicação: {e}")
        connection.rollback()

# Ler e imprimir todas as reivindicações do banco de dados
def read_and_print_reivindicacoes():
    """
    Lê e exibe todas as reivindicações registradas no banco de dados.
    """
    from connection import get_connection, get_cursor
    connection = get_connection()
    cursor_var = get_cursor()
    comando = """SELECT * FROM Reivindicacao"""

    try:
        cursor_var.execute(comando)
        registros = cursor_var.fetchall()

        if not registros:
            print("Nenhuma reivindicação encontrada no banco de dados.")
            return

        print("\n--- Lista de Reivindicações ---")
        print(f"{'ID Reiv.':<10} | {'ID Objeto':<10} | {'Pessoa (Matrícula)':<20} | {'ID Ocorrência':<15} | {'Data Retirada':<15}")
        print("-" * 85)

        for registro in registros:
            reivindicacao_id = registro[0]
            objeto_id = registro[1]
            pessoa_retirou = registro[2] if registro[2] else "N/A"
            ocorrencia_id = registro[3] if registro[3] else "N/A"
            data_retirada = registro[4].strftime("%Y-%m-%d") if hasattr(registro[4], 'strftime') else str(registro[4])

            print(f"{reivindicacao_id:<10} | {objeto_id:<10} | {pessoa_retirou:<20} | {str(ocorrencia_id):<15} | {data_retirada:<15}")

        print("\nLeitura de reivindicações finalizada.")

    except Exception as e:
        print(f"Erro ao ler reivindicações do banco de dados: {e}")
        connection.rollback()

# Ler e imprimir uma única reivindicação do banco de dados
def read_and_print_unica_reivindicacao(reivindicacao_id):
    """
    Busca e exibe os detalhes de uma única reivindicação pelo seu ID.

    Args:
        reivindicacao_id (int): O ID da reivindicação a ser exibida.
    """
    from connection import get_connection, get_cursor
    connection = get_connection()
    cursor_var = get_cursor()
    comando = f"""SELECT * FROM Reivindicacao WHERE ReivindicacaoID = {reivindicacao_id}"""

    try:
        cursor_var.execute(comando)
        registro = cursor_var.fetchone()

        if not registro:
            print(f"Nenhuma reivindicação encontrada com o ID {reivindicacao_id}.")
            return

        print(f"\n--- Detalhes da Reivindicação (ID: {reivindicacao_id}) ---")
        print(f"{'Campo':<25} | {'Valor'}")
        print("-" * 50)

        colunas = [
            "ID da Reivindicação", "ID do Objeto Reivindicado", "Pessoa que Retirou",
            "ID da Ocorrência", "Data da Retirada"
        ]

        valores = list(registro)
        # Formata a data
        if hasattr(valores[4], 'strftime'):
            valores[4] = valores[4].strftime("%Y-%m-%d")
        else:
            valores[4] = str(valores[4])

        # Trata valores nulos para exibição
        valores[2] = valores[2] if valores[2] is not None else "N/A"
        valores[3] = valores[3] if valores[3] is not None else "N/A"

        for i, campo in enumerate(colunas):
            print(f"{campo:<25} | {valores[i]}")

        print("\nLeitura de reivindicação finalizada.")

    except Exception as e:
        print(f"Erro ao ler reivindicação do banco de dados: {e}")
        connection.rollback()
