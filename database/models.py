from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    password = Column(String(128))
    email = Column(String(30))
    is_manager = Column(Boolean, default=False)
    accesses = relationship("Access", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name})>"

    def create_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

class Access(Base):
    __tablename__ = 'accesses'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    tab_name = Column(String(30))
    user = relationship("User", back_populates="accesses")

DATABASE_PATH = 'database/db/app.sqlite'
engine = create_engine(f'sqlite:///{DATABASE_PATH}')
Base.metadata.create_all(bind=engine)
