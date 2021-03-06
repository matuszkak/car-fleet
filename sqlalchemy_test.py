from sqlalchemy import create_engine, Column, Integer, String

from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///testdb.sqlite')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# DB szerkezetének leírása / táblák


class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  name = Column(String(80), nullable=False)
  age = Column(Integer)

  def __init__(self, name):
    self.name = name

  def save_to_db(self):
    try:
      session.add(self)
      session.commit()
    except Exception as e:
      print(f'hiba történt az adatbázisba való mentéskor: {e}')
    finally:
      session.close()

# nincs szükség a példányra

  @classmethod
  def find_by_id(cls, id: int):
    query = session.query(cls)
    return query.filter_by(id=id).first()


# létrehozza a DB-t és benne a táblákat amiket definiáltunk
Base.metadata.create_all(engine)
# new_user = User("John")
# new_user.save_to_db()

# new_user = User("Peter")
# new_user.age = 28
# new_user.save_to_db()

user = User.find_by_id(5)
print(user.name)