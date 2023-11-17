from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.orm import declarative_base,sessionmaker
from passlib.context import CryptContext

# Déclarer la classe de modèle (représente une table dans la base de données)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    username = Column(String(50))
    password = Column(String(50))
    email = Column(String(50))
    

if __name__ == '__main__':    
    # Créer un moteur SQLite en mémoire (remplacez 'sqlite:///:memory:' par votre propre URL de base de données)
    engine = create_engine('sqlite:///./DataBase/baseDonneeClients.db', echo=False)

    # Créer la table dans la base de données
    Base.metadata.create_all(engine)

    # Créenr ue session pour interagir avec la base de données
    Session = sessionmaker(bind=engine)
    session = Session() 

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    def get_password_hash(password):
        return pwd_context.hash(password)

    # Ajouter des utilisateurs à la base de données
    user1 = User(name='John Doe', username='DoeJ', password= get_password_hash('loikujytgrehujrjrsjd'), email='john.doe@example.com')
    user2 = User(name='Will Smith', username='SmithW', password= get_password_hash('poiuytreza'), email='will.smith@example.com')

    session.add_all([user1, user2])
    session.commit()

    # Interroger la base de données
    all_users = session.query(User).all()

    # Afficher les résultats
    for user in all_users:
        print(f"User ID: {user.id}, Name: {user.name}, Username: {user.username}, Email: {user.email}, password: {user.password}")

    # Fermer la session
    session.close() 