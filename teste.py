import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash
from pprint import pprint
print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='admin'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `Carhub`;")

cursor.execute("CREATE DATABASE `Carhub`;")

cursor.execute("USE `Carhub`;")

# criando tabelas
TABLES = {}
TABLES['Servisos'] = ('''
      CREATE TABLE `Servisos` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) NOT NULL,
      `valor` int NOT NULL,
      `email` varchar(100) NOT NULL,
      `categoria` varchar(40) NOT NULL,
      `descricao` varchar(250),
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Clientes'] = ('''
      CREATE TABLE `Clientes` (
      `cpf` varchar(11) NOT NULL,
      `nome` varchar(50) NOT NULL,
      `data` varchar(50) NOT NULL,
      `telefone` varchar(11) NOT NULL,
      `email` varchar(100) NOT NULL,
      `endereco` varchar(250) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`email`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['PrestadorServico'] = ('''
      CREATE TABLE `PrestadorServico` (
      `cnpj` varchar(14) NOT NULL,
      `nome` varchar(50) NOT NULL,
      `telefone` varchar(11) NOT NULL,
      `email` varchar(100) NOT NULL,
      `localidade` varchar(250) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`email`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')



for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

# inserindo Clientes
cliente_sql = 'INSERT INTO clientes (cpf, nome, data, telefone, email, endereco, senha)' \
              ' VALUES (%s, %s, %s,%s,%s,%s,%s)'
cliente = [
      ("99999999956", "Rodrigo", "11/05/1998 ", "11964802626",
       "rodrigo_7_4_7@hotmail.com", "Rua do retiro 2251", generate_password_hash("123").decode("utf-8")),
      ("99999889956", "Diego", "11/05/1998 ", "11970867253",
       "oliver.diegoramos@hotmail.com", "pass ", generate_password_hash("123").decode("utf-8"))
]

cursor.executemany(cliente_sql, cliente)

cursor.execute('select * from Carhub.clientes')
print(' -------------  cliente:  -------------')
for cliente in cursor.fetchall():
    pprint(cliente)


# inserindo Prestadores de serviço
prestadores_sql = 'INSERT INTO PrestadorServico (cnpj, nome, telefone, email, localidade, senha)' \
                  ' VALUES (%s, %s, %s,%s,%s,%s)'
prestadores = [
      ("99999999999999", "Cleber", "11970867253",
       "rodrigo_7_4_7@hotmail.com", " Henrique Felipe da Costa, 682 - Vila Guilherme",
       generate_password_hash("1234").decode("utf-8")),
      ("99999999999946", "Hubens", "11970867253",
       "oliver.diegoramos@hotmail.com", "pass ", generate_password_hash("1234").decode("utf-8"))
]
cursor.executemany(prestadores_sql, prestadores)

cursor.execute('select * from Carhub.PrestadorServico')
print(' -------------  PrestadorServico:  -------------')
for user in cursor.fetchall():
    pprint(user)



# inserindo Serviços
Servisos_sql = 'INSERT INTO Servisos (nome, valor,email, categoria,descricao) VALUES (%s, %s ,%s, %s,%s)'
Servisos = [
      ('Jogo de peneu', '50', 'rodrigo_7_4_7@hotmail.com', 'Troca', 'troca os quatros peneus do caro'),
      ('God of War', '15', 'oliver.diegoramos@hotmail.com', 'PS2', 'pass'),
      ('Mortal Kombat', '10', 'rodrigo_7_4_7@hotmail.com', 'PS2', 'pass'),
      ('Valorant', '123', 'oliver.diegoramos@hotmail.com', 'PC', 'pass'),
      ('Crash Bandicoot', '645', 'rodrigo_7_4_7@hotmail.com', 'PS2', 'pass'),
      ('Need for Speed', '879', 'rodrigo_7_4_7@hotmail.com', 'PS2', 'pass'),
]
cursor.executemany(Servisos_sql, Servisos)

cursor.execute('select * from Carhub.Servisos')
print(' -------------  Jogos:  -------------')
for servisos in cursor.fetchall():
   pprint(servisos)

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()
