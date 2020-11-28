from backend.db import DB

db = DB()
db.insert_data("drop table Goals;")
db.insert_data("drop table Fitness;")
db.insert_data("drop table Diet;")
db.insert_data("drop table Sleep;")
db.insert_data("drop table Users;")
