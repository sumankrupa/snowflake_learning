from snowflake.connector import connector

conn = connector(
    user='YOUR_USER',
    password='YOUR_PASSWORD',
    account='YOUR_ACCOUNT',
    warehouse='COMPUTE_WH',
    database='YOUR_DB',
    schema='PUBLIC'
)

cur = conn.cursor()
cur.execute('select current_version()')
print(cur.fetchall())

cur.close()
conn.close()
