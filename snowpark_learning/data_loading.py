
from snowflake.snowpark import Session
import os
from dotenv import load_dotenv
import snowflake.snowpark.functions as f
from snowflake.core import Root,CreateMode
from snowflake.core.task import Task, Cron
from datetime import timedelta

load_dotenv()


connection_params = {
    "account":   os.getenv('SNOWFLAKE_ACCOUNT'),
    "user":      os.getenv('SNOWFLAKE_USER'),
    "password":  os.getenv('SNOWFLAKE_PASSWORD'),
    "role":      os.getenv('SNOWFLAKE_ROLE'),
    "warehouse": os.getenv('SNOWFLAKE_WAREHOUSE'),
    "database":  os.getenv('SNOWFLAKE_DATABASE'),
    "schema":    os.getenv('SNOWFLAKE_SCHEMA'),
    "login_timeout": int(os.getenv('SNOWFLAKE_LOGIN_TIMEOUT', 30)),
    "network_timeout": int(os.getenv('SNOWFLAKE_NETWORK_TIMEOUT', 60)),
    "client_session_keep_alive": os.getenv('SNOWFLAKE_CLIENT_SESSION_KEEP_ALIVE', 'true').lower() == 'true',
    "query_tag": os.getenv('SNOWFLAKE_QUERY_TAG')
}

session = Session.builder.configs(connection_params).create()

root = Root(session)
schema = root.databases['mydb'].schemas['myschema']


