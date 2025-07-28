from connection import *

def menu():
	while True:
		print("ola usuario!")
		print("bem vindo ao banco de dados dos achados e perdidos")
		print("[1]adicionar pessoa")
		print("[2]remover pessoa")
		print("[3]sair")
		opt=int(input("o que deseja fazer?"))
		if opt==1:
			prompt_add_pessoa()
		if opt==2:
			prompt_remove_pessoa()
		if opt==3:
			 break


def prompt_add_pessoa():
	PessoaMatricula=input("qual a matricula da pessoa a ser adicionada? ")
	Pnome=input("qual o nome da pessoa a ser adicionada? ")
	Pcontato=input("qual o numero de contato da pessoa a ser adicionada? ")	
	insert_pessoa_database(PessoaMatricula,Pnome,Pcontato)		
	print("transação finalizada")		

def prompt_remove_pessoa():
	PessoaMatricula=input("qual a matricula da pessoa que voce deseja remover? ")
	remove_pessoa_database(PessoaMatricula)
	print("finalizado")
		
def prompt_add_objeto():
    print("\n--- Adicionar Novo Objeto Perdido ---")

    # Campos obrigatórios
    Otitulo = input("Qual o título/nome do objeto? (Ex: 'Chave', 'Celular', 'Mochila') ")
    Odescricao = input("Descreva o objeto detalhadamente: ")
    Olocal_encontrado = input("Onde o objeto foi encontrado? ")

    # Campos opcionais
    Ocor = input("Qual a cor do objeto? (Deixe em branco se não souber ou não se aplica) ")
    if not Ocor:
        Ocor = None
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