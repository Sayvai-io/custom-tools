from engine import pool
from sqlalchemy import text

# Create a cursor
cursor = pool.connect()

# column = cursor.execute(text("""CREATE TABLE patient_info (id SERIAL PRIMARY KEY, name VARCHAR(255), phone_number VARCHAR(255), start_time VARCHAR(255), end_time VARCHAR(255), event_id VARCHAR(255), appointment_date date);"""))
# print(column.fetchall())
column = cursor.execute(text("""SELECT * from patient_info;"""))
print(column.fetchall())
# cursor.commit()
