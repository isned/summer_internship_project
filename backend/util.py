
from sqlalchemy.orm import sessionmaker, scoped_session 
from sqlalchemy import create_engine

def get_session(connection_string):
    engine = create_engine(connection_string)
    session_maker = sessionmaker(engine)
    Data = scoped_session(session_maker)
    return Data