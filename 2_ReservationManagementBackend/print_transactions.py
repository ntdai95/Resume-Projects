from main import Settings
import sqlite3

# queries DB and prints transaction table (with header)
# and not at all dependent program 

db_name = Settings().database

conn = sqlite3.connect(db_name)
cursor = conn.cursor()

sql = "SELECT * FROM transactions"

with conn:
    result = cursor.execute(sql).fetchall()

width_list = [10, 10, 50, 30, 10, 10, 30]
for row in result:
    print("\nTRANS_ID".ljust(width_list[0]), "CUSTOM_ID".ljust(width_list[1]), "RESERV_ID".ljust(width_list[2]),
          "TRANS_TYPE".ljust(width_list[3]), "COST".ljust(width_list[4]), "DOWNPAY".ljust(width_list[5]),
          "TRANS_DATE".ljust(width_list[6]))
    print("="*150)

    for i, elem in enumerate(row):
        if i != len(row)-1:
            print(str(elem).ljust(width_list[i]), end=" ")
        else:
            print(str(elem).ljust(width_list[i]))

