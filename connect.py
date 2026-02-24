import snowflake.connector
from dotenv import load_dotenv
import os

load_dotenv()

conn = snowflake.connector.connect(
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    user=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASSWORD'),
    role=os.getenv('SNOWFLAKE_ROLE'),
    warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
    database=os.getenv('SNOWFLAKE_DATABASE'),
    schema=os.getenv('SNOWFLAKE_SCHEMA'),
    login_timeout=int(os.getenv('SNOWFLAKE_LOGIN_TIMEOUT', 30)),
    network_timeout=int(os.getenv('SNOWFLAKE_NETWORK_TIMEOUT', 60)),
    client_session_keep_alive=os.getenv('SNOWFLAKE_CLIENT_SESSION_KEEP_ALIVE', 'true').lower() == 'true',
    query_tag=os.getenv('SNOWFLAKE_QUERY_TAG')
)

cur = conn.cursor()
try:

    cur.execute('select * from myschema.source_table1')
    row = cur.fetchone()
    print(row)
finally:
    cur.close()
conn.close()
