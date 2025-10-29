# import os
# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import Session, sessionmaker
# import model
#
# def drop_and_create_tables():
#     """
#     Drop and create all tables in the database.
#     """
#     username = os.environ.get('DB_USERNAME') or 'root'
#     password = os.environ.get('DB_PASSWORD') or ''
#     database = os.environ.get('DB_DATABASE') or 'desenvolvimento'
#     port = os.environ.get('DB_PORT') or '3306'
#     server = os.environ.get('DB_SERVER') or 'localhost'
#     engine = create_engine(
#         f'mysql+pymysql://{username}:{password}@{server}:{port}/{database}',
#         echo_pool=os.environ.get('SQL_ECHO_POOL', "").lower() == 'true' or False,
#         pool_pre_ping=os.environ.get('SQL_POOL_PRE_PING', "").lower() == 'true' or False,
#         max_overflow=int(os.environ.get('SQL_MAX_OVERFLOW', 5)),
#         pool_size=int(os.environ.get('SQL_POOL_SIZE', 5)),
#         pool_recycle=int(os.environ.get('SQL_POOL_RECYCLE')
#
#     session: Session = sessionmaker(bind=engine, autoflush=False)()
#     # disable foreign key checks
#     session.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
#     session.commit()
#     model.Base.metadata.drop_all(engine)
#     model.Base.metadata.create_all(engine)
#     # enable foreign key checks
#     session.execute(text("SET FOREIGN_KEY_CHECKS=1;"))
#     session.commit()
#
#
#     if __name__ == '__main__':
#         drop_and_create_tables()
#     print('Database created')
