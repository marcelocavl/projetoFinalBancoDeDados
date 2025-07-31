from ocorrencia_database import *

# ------------------------------- MENUS ocorrências -------------------------------

# Menu de Opções de Ocorrências
def menu_ocorrencias():
    while True:
        print("\n--- OCORRÊNCIAS DE PERDA ---")
        print("[1] Adicionar Ocorrência de Perda")
        print("[2] Remover Ocorrência de Perda")
        print("[3] Editar Ocorrência de Perda")
        print("[4] Listar Ocorrências de Perda")
        print("[5] Voltar ao Menu Principal")
        opt = input("Escolha uma opção: ")
        if opt == "1":
            prompt_add_ocorrencia()
        elif opt == "2":
            prompt_remove_ocorrencia()
        elif opt == "3":
            prompt_edit_ocorrencia()
        elif opt == "4":
            read_and_print_ocorrencias()
        elif opt == "5":
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

# Menu de adicionar ocorrência
def prompt_add_ocorrencia():
    print("\n--- Adicionar Nova Ocorrência de Perda ---")
    tipo_objeto = input("Qual o tipo do objeto perdido? ")
    while True:
        data_perdido = input("Qual a data da perda? (YYYY-MM-DD) ")
        from datetime import datetime
        try:
            datetime.strptime(data_perdido, "%Y-%m-%d")
            break
        except ValueError:
            print("Data inválida! Digite no formato YYYY-MM-DD.")
    local_perdido = input("Onde o objeto foi perdido? (opcional) ")
    if not local_perdido:
        local_perdido = None
    pessoa_perdeu = input("Matrícula da pessoa que perdeu (opcional, deixe em branco se não houver): ")
    while pessoa_perdeu:
        from connection import cursor_var
        comando_check = f"SELECT PessoaMatricula FROM Pessoa WHERE PessoaMatricula = '{pessoa_perdeu}'"
        cursor_var.execute(comando_check)
        resultado = cursor_var.fetchone()
        if resultado:
            break
        print("Matrícula não encontrada. Por favor, digite uma matrícula válida ou deixe em branco.")
        pessoa_perdeu = input("Matrícula da pessoa que perdeu (opcional, deixe em branco se não houver): ")
    if not pessoa_perdeu:
        pessoa_perdeu = None

    insert_ocorrencia_database(
        tipo_objeto=tipo_objeto,
        data_perdido=data_perdido,
        local_perdido=local_perdido,
        pessoa_perdeu=pessoa_perdeu
    )
    print("Transação de adição de ocorrência finalizada.")

# Menu de remover ocorrência
def prompt_remove_ocorrencia():
    print("\n--- Remover Ocorrência de Perda ---")
    try:
        ocorrencia_id = int(input("Qual o ID da ocorrência a ser removida? "))
        remove_ocorrencia_database(ocorrencia_id)
        print("Transação de remoção de ocorrência finalizada.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número inteiro para o ID.")

# Menu de editar ocorrência
def prompt_edit_ocorrencia():
    print("\n--- Editar Ocorrência de Perda ---")
    read_and_print_ocorrencias()
    try:
        ocorrencia_id = int(input("Qual o ID da ocorrência a ser editada? "))
        read_and_print_unica_ocorrencia(ocorrencia_id)
        print("\nEscolha o campo a ser editado:")
        print("[1] Tipo do Objeto")
        print("[2] Data da Perda")
        print("[3] Local da Perda")
        print("[4] Pessoa que Perdeu")

        campos_menu = {
            "1": "tipo_objeto",
            "2": "data_perdido",
            "3": "local_perdido",
            "4": "pessoa_perdeu"
        }

        opcao = input("Digite o número da opção: ")
        campo_a_editar = campos_menu.get(opcao)

        if not campo_a_editar:
            print("Opção inválida. Por favor, escolha uma opção válida.")
            return

        # Validação da data se for campo data_perdido
        if campo_a_editar == "data_perdido":
            from datetime import datetime
            while True:
                novo_valor = input("Digite o novo valor para 'data_perdido' (YYYY-MM-DD): ")
                try:
                    datetime.strptime(novo_valor, "%Y-%m-%d")
                    break
                except ValueError:
                    print("Data inválida! Digite no formato YYYY-MM-DD.")
        else:
            novo_valor = input(f"Digite o novo valor para '{campo_a_editar}': ")

        if campo_a_editar == "pessoa_perdeu" and novo_valor:
            while novo_valor:
                from connection import cursor_var
                comando_check = f"SELECT PessoaMatricula FROM Pessoa WHERE PessoaMatricula = '{novo_valor}'"
                cursor_var.execute(comando_check)
                resultado = cursor_var.fetchone()
                if resultado:
                    break
                print("Matrícula não encontrada. Por favor, digite uma matrícula válida ou deixe em branco.")
                novo_valor = input("Matrícula da pessoa que perdeu (opcional, deixe em branco se não houver): ")
            if not novo_valor:
                novo_valor = None
        if novo_valor.strip() == "":
            novo_valor = None

        update_ocorrencia_database(ocorrencia_id, campo_a_editar, novo_valor)
        print("Transação de edição de ocorrência finalizada.")
    except ValueError:
        print("Entrada inválida. Por favor, tente novamente.")