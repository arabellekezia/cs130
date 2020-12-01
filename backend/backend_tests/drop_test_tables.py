from backend.db import DB
from backend.setup.set_up_db import drop_all_tables

db = DB()
drop_all_tables(db)
print("Removed all tables from test db")
