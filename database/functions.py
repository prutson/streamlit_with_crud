from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.models import User, Access, engine

def create_entity(engine, entity_type, **kwargs):
    with Session(bind=engine) as session:
        if entity_type == 'user':
            # Verifica se o email já está em uso
            existing_user = session.query(User).filter(User.email == kwargs['email']).first()
            if existing_user:
                raise ValueError("Email já está em uso.")
            
            # Criando e configurando um novo usuário
            user = User(name=kwargs['name'], email=kwargs['email'])
            user.create_password(kwargs['password'])
            session.add(user)
        
        elif entity_type == 'access':
            if 'user_id' not in kwargs:
                raise ValueError("user_id é necessário para criar um acesso.")

            # Verifica se o user_id corresponde a um usuário existente
            user = session.query(User).filter(User.id == kwargs['user_id']).first()
            if not user:
                raise ValueError(f"Não existe usuário com o ID {kwargs['user_id']}.")

            # Criando e configurando um novo acesso
            access = Access(user_id=kwargs['user_id'], tab_name=kwargs['tab_name'])
            session.add(access)
        
        else:
            raise ValueError("Tipo de entidade desconhecido ou parâmetros insuficientes fornecidos.")

        # Commit das alterações no banco de dados
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise ValueError("Erro de integridade ao tentar inserir no banco de dados.")


# # Exemplo de uso para criar um usuário
# try:
#     create_entity(engine, 'user', name='joao', email='joao@joao.com', password='minhasenha')
# except ValueError as e:
#     print(f"Erro ao criar usuário: {str(e)}")

# # Exemplo de uso para criar um acesso
# create_entity(engine, 'access', user_id=1, tab_name='Dashboard')


def delete_entity(engine, entity_type, entity_id):
    with Session(bind=engine) as session:
        if entity_type == 'user':
            # Localizando o usuário pelo ID
            user = session.query(User).filter(User.id == entity_id).first()
            if user:
                session.delete(user)
            else:
                raise ValueError("Usuário não encontrado.")
        elif entity_type == 'access':
            # Localizando o acesso pelo ID
            access = session.query(Access).filter(Access.id == entity_id).first()
            if access:
                session.delete(access)
            else:
                raise ValueError("Acesso não encontrado.")
        else:
            raise ValueError("Tipo de entidade desconhecido.")

        # Confirmando a remoção no banco de dados
        session.commit()

# # Exemplo de uso para deletar um usuário
# try:
#     delete_entity(engine, 'user', 1)  # Supondo que 1 seja o ID do usuário
# except ValueError as e:
#     print(e)

# # Exemplo de uso para deletar um acesso
# try:
#     delete_entity(engine, 'access', 1)  # Supondo que 2 seja o ID do acesso
# except ValueError as e:
#     print(e)


def read(engine, entity_type, filter_column, filter_value):
    with Session(bind=engine) as session:
        entity = None
        if entity_type == 'user':
            entity = session.query(User).filter(getattr(User, filter_column) == filter_value).first()
        elif entity_type == 'access':
            entity = session.query(Access).filter(getattr(Access, filter_column) == filter_value).first()
        else:
            raise ValueError("Tipo de entidade desconhecido.")

        if entity:
            return {column.name: getattr(entity, column.name) for column in entity.__table__.columns}
        else:
            return "Nenhum registro encontrado."

# # Exemplo de uso para ler um usuário por email
# user_details = read(engine, 'user', 'email', 'joao@joao.com')
# print(user_details)

# # Exemplo de uso para ler um acesso por user_id
# access_details = read(engine, 'access', 'user_id', 1)
# print(access_details)


def read_all(engine, entity_type):
    with Session(bind=engine) as session:
        if entity_type == 'user':
            results = session.query(User).all()
        elif entity_type == 'access':
            results = session.query(Access).all()
        else:
            raise ValueError("Tipo de entidade desconhecido.")
        
        # Retornando uma lista de dicionários
        return [{column.name: getattr(result, column.name) for column in result.__table__.columns} for result in results]


