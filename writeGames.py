import pymysql
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, ForeignKey,Column,String,INTEGER
import psycopg2 as pg

base = declarative_base()

class Game(base):
    __tablename__ = "games"
    
    SEASON_ID = Column("season_id",INTEGER)
    TEAM_ID = Column("team_id",INTEGER)
    TEAM_ABBREVIATION = Column("team_abbreviation",String(6))
    TEAM_NAME = Column("team_name",String(30))
    GAME_ID = Column("game_id",INTEGER,primary_key = True)
    GAME_DATE = Column("game_date",String(15))
    MATCHUP = Column("matchup",String(25))
    WL = Column("wl",String(1))
    
    def __init__(self,season_id,team_id,team_abbreviation,team_name,game_id,game_date,matchup,wl):
        self.SEASON_ID = season_id
        self.TEAM_ID = team_id
        self.TEAM_ABBREVIATION = team_abbreviation
        self.TEAM_NAME = team_name
        self.GAME_ID = game_id
        self.GAME_DATE = game_date
        self.MATCHUP = matchup
        self.WL = wl
        
def get_connection(user,password,host,port,database):
    return create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        )
    )
    
def write_to_db(df,user,password,host,port,database):
    engine = get_connection(user, password, host, port, database)
    Base.metadata.create_all(bind = engine)
    Session = sessionmaker(bind = engine)
    
    session = Session()
    for indx,row in df.iterrows():
        session.add(Game(*row.tolist()))
    
    session.commit()