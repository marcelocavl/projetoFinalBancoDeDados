from connection import *
from prompts_pessoas import *
from prompts_objetos import *


def menu():
	print("Ola usuario!")
	("Bem vindo ao banco de dados dos achados e perdidos")
	while True:
		print("\n--- ACHADOS E PERDIDOS ---")
		print("[1] Pessoas")
		print("[2] Objetos")
		print("[3] Ocorrencias de perda")
		print("[4] Reivindicações")
		print("[5] sair")
		opt = input("Qual registro deseja acessar? ")
		if opt=="1":
			menu_pessoas()
		elif opt=="2":
			menu_objetos()
		elif opt=="3":
			menu_objetos()
		elif opt=="4":
			menu_objetos()
		elif opt=="5":
			print("Obrigado por usar o sistema de achados e perdidos")
			break
		else:
			print("Opção inválida. Por favor, escolha uma opção válida.")
