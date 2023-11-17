import sys 
sys.path.append('../')
from utils import *


if __name__ == '__main__':
    # Créer la table dans la base de données
    engine = create_engine('sqlite:///baseDonneeClients.db', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)

    def get_password_hash(password):
        return pwd_context.hash(password)

    # Ajouter des utilisateurs à la base de données
    user1 = User(name='John Doe', username='DoeJ', password= get_password_hash('loikujytgrehujrjrsjd'), email='john.doe@example.com')
    stat1 = StatistiquesClient(id_Client= 1, total_credit=1000, nb_faillites=10, nb_retards= 10)
    u1_transac1 = Transactions(id_Client=1, montant=100, date_payement='2023-10-15')
    u1_transac2 = Transactions(id_Client=1, montant=200, date_payement='2023-10-14')
    u1_transac3 = Transactions(id_Client=1, montant=150, date_payement='2023-10-10')

    user2 = User(name='Will Smith', username='SmithW', password= get_password_hash('poiuytreza'), email='will.smith@example.com')
    stat2 = StatistiquesClient(id_Client= 2, total_credit=3, nb_faillites=0, nb_retards= 2)
    u2_transac1 = Transactions(id_Client=2, montant=300, date_payement='2023-10-15')
    u2_transac2 = Transactions(id_Client=2, montant=250, date_payement='2023-10-12')

    user3 = User(name='Jean Dupont', username='DupontJ', password= get_password_hash('azertyuiop'), email='jean.dupont@example.com')
    stat3 = StatistiquesClient(id_Client= 3, total_credit=5, nb_faillites=3, nb_retards= 7)
    u3_transac1 = Transactions(id_Client=3, montant=400, date_payement='2023-10-13')
    u3_transac2 = Transactions(id_Client=3, montant=450, date_payement='2023-10-11')
    
    session.add_all([user1, user2,user3, stat1, stat2, stat3, u1_transac1, u1_transac2, u1_transac3, u2_transac1, u2_transac2, u3_transac1, u3_transac2])
    session.commit()

    # Interroger la base de données
    all_users = session.query(User).all()
    all_stats = session.query(StatistiquesClient).all()
    all_transac = session.query(Transactions).all()

    # Afficher les résultats
    for user in all_users:
        print(f"User ID: {user.id}, Name: {user.name}, Username: {user.username}, Email: {user.email}, password: {user.password}")
    
    # Afficher les résultats
    for stat in all_stats:
        print(f"IdClient: {stat.id_Client}, total_credit: {stat.total_credit}, nb_faillites: {stat.nb_faillites}, nb_retards: {stat.nb_retards}")

    # Afficher les résultats
    for stat in all_transac:
        print(f"IdClient: {stat.id_Client}, montant: {stat.montant}, date_payement: {stat.date_payement}")


    # Fermer la session
    session.close() 