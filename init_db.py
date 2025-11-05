from database import engine, Base
import models

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("criou")

if __name__ == "__main__":
    create_tables(models)