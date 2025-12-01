import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
import model


def drop_and_create_tables():
    username = os.environ.get('DB_USERNAME', 'root')
    password = os.environ.get('DB_PASSWORD', '')
    database = os.environ.get('DB_DATABASE', 'bookstore')
    port = os.environ.get('DB_PORT', '3306')
    server = os.environ.get('DB_SERVER', 'localhost')

    # Correct MySQL connection string
    engine = create_engine(
        f'mysql+pymysql://{username}:{password}@{server}:{port}/{database}',
        echo_pool=os.environ.get('SQL_ECHO_POOL', "").lower() == 'true',
        pool_pre_ping=os.environ.get('SQL_POOL_PRE_PING', "").lower() == 'true',
        max_overflow=int(os.environ.get('SQL_MAX_OVERFLOW', 5)),
        pool_size=int(os.environ.get('SQL_POOL_SIZE', 5)),
        pool_recycle=int(os.environ.get('SQL_POOL_RECYCLE', -1)),
    )

    session: Session = sessionmaker(bind=engine, autoflush=False)()

    try:
        # Disable foreign key checks
        session.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
        session.commit()

        # Drop and create tables
        model.Base.metadata.drop_all(engine)
        model.Base.metadata.create_all(engine)

        # Enable foreign key checks
        session.execute(text("SET FOREIGN_KEY_CHECKS=1;"))
        session.commit()
    finally:
        session.close()


if __name__ == '__main__':
    drop_and_create_tables()
    print('Database created')