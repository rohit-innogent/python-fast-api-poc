from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

URL_DATABASE = 'mysql+pymysql://root:root@localhost:3306/fast_api'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
