from backend.db import DB
from backend.setup.set_up_db import set_up_db

db = DB()
set_up_db(db)
print("Test database has been set up")
