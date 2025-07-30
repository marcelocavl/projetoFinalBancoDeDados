import pyodbc
from datetime import datetime

from pessoa_database import *
from objeto_database import *

connection=None
cursor_var=None

def connect_database():
	global conection
	global cursor_var
	data_conection=(	
		"Driver={MariaDB ODBC 3.1 Driver};"
		"Server=localhost;"
		"Database=AchadosEPerdidos;"
		"UID=root;"
		"PWD=123;"
		"Port=3306;"
	)
	connection=pyodbc.connect(data_conection);
	cursor_var=connection.cursor()
	print("conexão bem sucedida");



