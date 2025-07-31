from connection import *
from objeto_database import *

# ------------------------------- MENUS objetos -------------------------------

# Menu de Opções de Objetos
def menu_objetos():
		while True:
				print("\n--- OBJETOS ---")
				print("[1] Adicionar Objeto Perdido")
				print("[2] Remover Objeto Perdido")
				print("[3] Editar Objeto Perdido")
				print("[4] Listar Objetos Perdidos")
				print("[5] Voltar ao Menu Principal")
				opt = input("Escolha uma opção: ")
				if opt == "1":
						prompt_add_objeto()
				elif opt == "2":
						prompt_remove_objeto()
				elif opt == "3":
						prompt_edit_objeto()
				elif opt == "4":
						read_and_print_objetos()
				elif opt == "5":
						break
				else:
						print("Opção inválida. Por favor, escolha uma opção válida.")

# Menu de adicionar objeto 
def prompt_add_objeto():
    print("\n--- Adicionar Novo Objeto Perdido ---")

    # Campos obrigatórios
    Otitulo = input("Qual o título/nome do objeto? ")
    Odescricao = input("Descreva o objeto detalhadamente: ")
    Olocal_encontrado = input("Onde o objeto foi encontrado? ")

    # Campos opcionais
    Ocor = input("Qual a cor do objeto? (Deixe em branco se não souber ou não se aplica) ")
    if not Ocor:
        Ocor = None
    Opessoa_entregou = input("Matrícula da pessoa que entregou (opcional, deixe em branco se não houver): ")
    while Opessoa_entregou:
        from connection import cursor_var
        comando_check = f"SELECT PessoaMatricula FROM Pessoa WHERE PessoaMatricula = '{Opessoa_entregou}'"
        cursor_var.execute(comando_check)
        resultado = cursor_var.fetchone()
        if resultado:
            break
        print("Matrícula não encontrada. Por favor, digite uma matrícula válida ou deixe em branco.")
        Opessoa_entregou = input("Matrícula da pessoa que entregou (opcional, deixe em branco se não houver): ")
    if not Opessoa_entregou:
        Opessoa_entregou = None

    insert_objeto_database(
        Otitulo=Otitulo,
        Ocor=Ocor,
        Odescricao=Odescricao,
        Olocal_encontrado=Olocal_encontrado,
        Opessoa_entregou=Opessoa_entregou,
        Oreinvidicado=False
    )

    print("Transação de adição de objeto finalizada.")

# Menu de remover objeto
def prompt_remove_objeto():
    print("\n--- Remover Objeto Perdido ---")
    try:
        objeto_id = int(input("Qual o ID do objeto a ser removido? "))
        remove_objeto_database(objeto_id)
        print("Transação de remoção de objeto finalizada.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número inteiro para o ID.")

# Menu de editar objeto
def prompt_edit_objeto():
    print("\n--- Editar Objeto Perdido ---")
    read_and_print_objetos()
    try:
        objeto_id = int(input("Qual o ID do objeto a ser editado? "))

        read_and_print_unico_objeto(objeto_id)

        print("\nEscolha o campo a ser editado:")
        print("[1] Título")
        print("[2] Cor")
        print("[3] Descrição")
        print("[4] Local Encontrado")
        print("[5] Pessoa que Entregou")

        opcao = input("Digite o número da opção: ")

        campos_menu = {
            "1": "titulo",
            "2": "cor",
            "3": "descricao",
            "4": "local_encontrado",
            "5": "pessoa_entregou"
        }

        campo_a_editar = campos_menu.get(opcao)

        if not campo_a_editar:
            print("Opção inválida. Por favor, escolha uma opção válida.")
            return

        novo_valor = input(f"Digite o novo valor para '{campo_a_editar}': ")

        # Checagem de matrícula válida se campo for pessoa_entregou
        if campo_a_editar == "pessoa_entregou" and novo_valor:
            while novo_valor:
                from connection import cursor_var
                comando_check = f"SELECT PessoaMatricula FROM Pessoa WHERE PessoaMatricula = '{novo_valor}'"
                cursor_var.execute(comando_check)
                resultado = cursor_var.fetchone()
                if resultado:
                    break
                print("Matrícula não encontrada. Por favor, digite uma matrícula válida ou deixe em branco.")
                novo_valor = input("Matrícula da pessoa que entregou (opcional, deixe em branco se não houver): ")
            if not novo_valor:
                novo_valor = None

        if novo_valor.strip() == "":
            novo_valor = None

        update_objeto_database(objeto_id, campo_a_editar, novo_valor)
        print("Transação de edição de objeto finalizada.")
    except ValueError:
        print("Entrada inválida. Por favor, tente novamente.")
       
