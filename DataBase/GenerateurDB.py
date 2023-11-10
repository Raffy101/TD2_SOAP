import sqlite3

# Il s'agit ici d'un fichier qui va nous permettre de créer une dataBAse pour les clients d'une banque ! 
# Il nous servira donc principalement à créer des dossiers pour clients qui souhaite faire des demandes de prêts immobilié

# Créer une connexion à la base de données (ou se connecter à une base de données existante)
conn = sqlite3.connect('./DataBase/BaseDeDonneesClients.db')

# Créer un curseur pour exécuter des requêtes
cur = conn.cursor()

# Créer la table clients
cur.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY,
        nom TEXT,
        total_credit INTEGER,
        nb_faillites INTEGER,
        nb_retards INTEGER
    )
''')

# Créer la table transactions
cur.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        client_id INTEGER,
        montant INTEGER,
        date_payement TEXT,
        FOREIGN KEY(client_id) REFERENCES clients(id)
    )
''')

# Ajouter des clients
clients = [('Jean Dupont',5, 2, 5), ('John Doe',1, 1000, 10), ('Client3',3, 0, 2), ('Client4',5, 3, 7), ('Client5',7, 2, 4)]
cur.executemany("INSERT INTO clients (nom, total_credit, nb_faillites, nb_retards) VALUES (?, ?, ?, ?)", clients)

# Ajouter des transactions pour chaque client
transactions = [(1, 100, '2023-10-15'), (1, 200, '2023-10-14'), (1, 150, '2023-10-10'),
                (2, 300, '2023-10-15'), (2, 250, '2023-10-12'),
                (3, 400, '2023-10-13'), (3, 450, '2023-10-11'),
                (4, 150, '2023-10-15'), (4, 200, '2023-10-14'), (4, 350, '2023-10-10'),
                (5, 250, '2023-10-15'),
                (5, 250, '2023-10-15'), (5, 250, '2023-10-14'), (5, 500, '2023-10-10')]

cur.executemany("INSERT INTO transactions (client_id, montant, date_payement) VALUES (?, ?, ?)", transactions)

conn.commit()

# Afficher tous les clients
cur.execute("SELECT * FROM clients")
print("Table Clients:")
print(cur.fetchall())

# Afficher toutes les transactions
cur.execute("SELECT * FROM transactions")
print("\nTable Transactions:")
print(cur.fetchall())

# Fermer la connexion à la base de données
conn.close()
