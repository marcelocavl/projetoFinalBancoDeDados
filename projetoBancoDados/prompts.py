from connection import *
from prompts_pessoas import *
from prompts_objetos import *


def menu():
	while True:
		print("ola usuario!")
		print("bem vindo ao banco de dados dos achados e perdidos")
		print("[1]adicionar pessoa")
		print("[2]remover pessoa")
		print("[3]editar pessoa")
		print("[4]sair")
		opt=int(input("o que deseja fazer?"))
		if opt==1:
			prompt_add_pessoa()
		if opt==2:
			prompt_remove_pessoa()
		if opt==3:
			 prompt_update_pessoa()
		if opt==4:
			 break



