from reivindicacao_database import *
from objeto_database import read_and_print_objetos
from ocorrencia_database import read_and_print_ocorrencias

# ------------------------------- MENUS Reivindicações -------------------------------

def menu_reivindicacoes():
    """
    Exibe o menu de opções para o gerenciamento de reivindicações.
    """
    while True:
        print("\n--- REIVINDICAÇÕES DE OBJETOS ---")
        print("[1] Adicionar Reivindicação")
        print("[2] Remover Reivindicação")
        print("[3] Editar Reivindicação")
        print("[4] Listar Reivindicações")
        print("[5] Voltar ao Menu Principal")
        opt = input("Escolha uma opção: ")
        if opt == "1":
            prompt_add_reivindicacao()
        elif opt == "2":
            prompt_remove_reivindicacao()
        elif opt == "3":
            prompt_edit_reivindicacao()
        elif opt == "4":
            read_and_print_reivindicacoes()
        elif opt == "5":
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

def prompt_add_reivindicacao():
    """
    Solicita ao usuário as informações para adicionar uma nova reivindicação.
    """
    from connection import cursor_var # Importação corrigida
    print("\n--- Adicionar Nova Reivindicação ---")
    
    # Lista os objetos disponíveis (que ainda não foram reivindicados)
    print("Por favor, escolha um objeto da lista de não reivindicados abaixo:")
    read_and_print_objetos()

    # Valida o ID do objeto
    objeto_id = None
    while True:
        try:
            objeto_id_input = input("Qual o ID do objeto a ser reivindicado? ")
            objeto_id = int(objeto_id_input)
            
            # Verifica se o objeto existe e se não foi reivindicado
            cursor_var.execute(f"SELECT Reinvidicado FROM Objeto WHERE ObjetoID = {objeto_id}")
            resultado = cursor_var.fetchone()

            if not resultado:
                print(f"Erro: Objeto com ID {objeto_id} não encontrado.")
            elif resultado[0]: # Se resultado[0] for TRUE (1)
                print(f"Erro: Objeto com ID {objeto_id} já foi reivindicado.")
            else:
                break # Objeto válido e disponível
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro para o ID do objeto.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return

    # Valida a matrícula da pessoa
    pessoa_retirou = None
    while True:
        pessoa_retirou_input = input("Matrícula da pessoa que está retirando o objeto: ")
        cursor_var.execute(f"SELECT Pnome FROM Pessoa WHERE PessoaMatricula = '{pessoa_retirou_input}'")
        resultado = cursor_var.fetchone()
        if resultado:
            pessoa_retirou = pessoa_retirou_input
            print(f"Pessoa encontrada: {resultado[0]}")
            break
        else:
            print("Matrícula não encontrada. Por favor, digite uma matrícula válida.")

    # Valida a ocorrência (opcional)
    read_and_print_ocorrencias()
    ocorrencia_id = None
    while True:
        ocorrencia_id_input = input("Qual o ID da ocorrência de perda associada? (opcional, deixe em branco se não houver) ")
        if not ocorrencia_id_input:
            break # O usuário não quer associar uma ocorrência
        try:
            ocorrencia_id = int(ocorrencia_id_input)
            cursor_var.execute(f"SELECT OcorrenciaID FROM Ocorrencia_Perda WHERE OcorrenciaID = {ocorrencia_id}")
            if cursor_var.fetchone():
                break # Ocorrência válida
            else:
                print(f"Ocorrência com ID {ocorrencia_id} não encontrada.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro para o ID da ocorrência.")

    # Insere a reivindicação no banco de dados
    insert_reivindicacao_database(
        objeto_reivindicado_id=objeto_id,
        pessoa_retirou=pessoa_retirou,
        ocorrencia_id=ocorrencia_id
    )
    print("Transação de adição de reivindicação finalizada.")

def prompt_remove_reivindicacao():
    """
    Solicita ao usuário o ID de uma reivindicação para ser removida.
    """
    print("\n--- Remover Reivindicação ---")
    read_and_print_reivindicacoes()
    try:
        reivindicacao_id = int(input("Qual o ID da reivindicação a ser removida? "))
        # Adicionar uma confirmação seria uma boa prática
        confirm = input(f"Tem certeza que deseja remover a reivindicação {reivindicacao_id}? Isso tornará o objeto disponível novamente. (s/n): ")
        if confirm.lower() == 's':
            remove_reivindicacao_database(reivindicacao_id)
            print("Transação de remoção de reivindicação finalizada.")
        else:
            print("Remoção cancelada.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número inteiro para o ID.")

def prompt_edit_reivindicacao():
    """
    Solicita ao usuário as informações para editar uma reivindicação existente.
    """
    from connection import cursor_var # Importação corrigida
    print("\n--- Editar Reivindicação ---")
    read_and_print_reivindicacoes()
    try:
        reivindicacao_id = int(input("Qual o ID da reivindicação a ser editada? "))
        read_and_print_unica_reivindicacao(reivindicacao_id)
        
        print("\nEscolha o campo a ser editado:")
        print("[1] Pessoa que Retirou")
        print("[2] Ocorrência de Perda Associada")

        campos_menu = {
            "1": "pessoa_retirou",
            "2": "ocorrencia_id"
        }

        opcao = input("Digite o número da opção: ")
        campo_a_editar = campos_menu.get(opcao)

        if not campo_a_editar:
            print("Opção inválida.")
            return

        novo_valor = input(f"Digite o novo valor para '{campo_a_editar}': ")
        
        # Validação do novo valor
        if campo_a_editar == "pessoa_retirou":
            while True:
                cursor_var.execute(f"SELECT Pnome FROM Pessoa WHERE PessoaMatricula = '{novo_valor}'")
                if cursor_var.fetchone():
                    break
                print("Matrícula não encontrada.")
                novo_valor = input(f"Digite a nova matrícula para '{campo_a_editar}': ")
        
        elif campo_a_editar == "ocorrencia_id":
             if novo_valor:
                while True:
                    try:
                        id_ocorrencia = int(novo_valor)
                        cursor_var.execute(f"SELECT OcorrenciaID FROM Ocorrencia_Perda WHERE OcorrenciaID = {id_ocorrencia}")
                        if cursor_var.fetchone():
                            break
                        else:
                             print(f"Ocorrência com ID {id_ocorrencia} não encontrada.")
                             novo_valor = input("Digite o novo ID da ocorrência (ou deixe em branco): ")
                             if not novo_valor: break
                    except ValueError:
                        print("ID inválido.")
                        novo_valor = input("Digite o novo ID da ocorrência (ou deixe em branco): ")
                        if not novo_valor: break
             else:
                novo_valor = None


        update_reivindicacao_database(reivindicacao_id, campo_a_editar, novo_valor)
        print("Transação de edição de reivindicação finalizada.")
    except ValueError:
        print("Entrada inválida. Por favor, tente novamente.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
