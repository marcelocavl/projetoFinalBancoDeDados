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
		
