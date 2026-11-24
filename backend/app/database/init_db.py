from app.helpers.db import Base, engine
import app.models

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully I guess")

if __name__=="__main__":
    init_db()
    