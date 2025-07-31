from pessoa_database import *


# Menu de Opções de Pessoas
def menu_pessoas():
		while True:
				print("\n--- PESSOAS ---")
				print("[1] Adicionar Pessoa")
				print("[2] Remover Pessoa")
				print("[3] Editar Pessoa")
				print("[4] Listar Pessoas")
				print("[5] Voltar ao Menu Principal")
				opt = input("Escolha uma opção: ")
				if opt == "1":
						prompt_add_pessoa()
				elif opt == "2":
						prompt_remove_pessoa()
				elif opt == "3":
						prompt_edit_pessoa()
				elif opt == "4":
						read_and_print_pessoas()
				elif opt == "5":
						break
				else:
						print("Opção inválida. Por favor, escolha uma opção válida.")

# Menu de adicionar pessoa
def prompt_add_pessoa():
	print("\n--- Adicionar Nova Pessoa ---")

	PessoaMatricula=input("Qual a matricula da pessoa a ser adicionada? ")
	Pnome=input("Qual o nome da pessoa a ser adicionada? ")
	Pcontato=input("Qual o numero de contato da pessoa a ser adicionada? ")	

	insert_pessoa_database(
		PessoaMatricula,
		Pnome,
		Pcontato
	)		
	print("Transação finalizada")		

def prompt_edit_pessoa():
		print("\n--- Editar Pessoa ---")
		try:
			read_and_print_pessoas()
			pessoa_matricula=input("Qual a matricula da pessoa a ser editada? ")

			read_and_print_unica_pessoa(pessoa_matricula)

			print("\nEscolha o campo a ser editado:")
			print("[1] Matricula")
			print("[2] Nome")
			print("[3] Contato")
		
			opcao=input("Digite o número da opção: ")
			
			#dicionario informando os campos na entidade Pessoa
			campos_menu={
				"1": "PessoaMatricula",
				"2": "Pnome",
				"3": "Contato",
			}

			campo=campos_menu.get(opcao)	

			novo_valor=input(f"Digite o novo valor para {campo}: ")

			if novo_valor.strip() == "":
				novo_valor = None

			update_pessoa_database(pessoa_matricula,campo,novo_valor)
		except ValueError:
			print("Entrada inválida. Por favor, tente novamente.")


def prompt_remove_pessoa():
	print("\n--- Remover Pessoa ---")
	PessoaMatricula=input("Qual a matricula da pessoa que voce deseja remover? ")
	remove_pessoa_database(
		PessoaMatricula
	)
	print("Transação finalizada")
      
