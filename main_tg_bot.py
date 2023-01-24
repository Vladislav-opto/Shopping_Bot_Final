from database.db import Base, engine
from webapp.webapp import create_app
from tg_bot.shopping_bot import tg_main


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    tg_main()   
