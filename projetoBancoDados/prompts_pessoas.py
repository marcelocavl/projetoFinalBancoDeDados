from pessoa_database import *

def prompt_add_pessoa():
	PessoaMatricula=input("qual a matricula da pessoa a ser adicionada? ")
	Pnome=input("qual o nome da pessoa a ser adicionada? ")
	Pcontato=input("qual o numero de contato da pessoa a ser adicionada? ")	

	insert_pessoa_database(
		PessoaMatricula,
		Pnome,
		Pcontato
	)		

	print("transação finalizada")		

def prompt_update_pessoa():


		print("\n--- Editar Pessoa ---")

		#dicionario informando os campos na entidade Pessoa
		campos_menu={
			"1": "PessoaMatricula",
			"2": "Pnome",
			"3": "Contato",
		}

		pessoa_matricula=input("qual a matricula da pessoa a ser editada")

		print("\nEscolha o campo a ser editado:")
		print("1. PessoaMatricula")
		print("2. Pnome")
		print("3. Contato")
	
		opt=input("escolha uma opcao");

		campo=campos_menu.get(opt)	

		novo_valor=input(f"digite o novo valor a ser escrito em {campo} ")

		if novo_valor.strip() == "":
			novo_valor = None

		update_pessoa_database(pessoa_matricula,campo,novo_valor)




def prompt_remove_pessoa():
	PessoaMatricula=input("qual a matricula da pessoa que voce deseja remover? ")
	remove_pessoa_database(
		PessoaMatricula
	)
	print("finalizado")
      
