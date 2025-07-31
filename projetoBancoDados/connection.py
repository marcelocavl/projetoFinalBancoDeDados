import pyodbc

# Essas variáveis globais serão inicializadas pela função connect_database()
# e importadas por outros módulos.
connection = None
cursor_var = None

def connect_database():
	"""
	Estabelece a conexão com o banco de dados MySQL e inicializa
	as variáveis globais de conexão e cursor.
	"""
	global connection
	global cursor_var
	try:
		data_conection = (	
			"Driver={MariaDB ODBC 3.1 Driver};"
			"Server=localhost;"
			"Database=AchadosEPerdidos;"
			"UID=root;"
			"PWD=123;"
			"Port=3306;"
		)
		connection = pyodbc.connect(data_conection)
		cursor_var = connection.cursor()
		print("conexão bem sucedida")
	except Exception as e:
		print(f"Falha na conexão com o banco de dados: {e}")
		# Se a conexão falhar, o programa não pode continuar.
		exit()


def get_connection():
	"""
	Retorna a conexão com o banco de dados.
	"""
	if connection is None:
		connect_database()
	return connection
def get_cursor():
	"""
	Retorna o cursor do banco de dados.
	"""
	if cursor_var is None:
		connect_database()
	return cursor_var

