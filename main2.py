from database.db import Base, engine
from webapp.webapp import create_app
from tg_bot.shopping_bot import tg_main


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    #app = create_app()
    #app.run(host="127.0.0.1", port=5000, debug=True)
    tg_main()   
