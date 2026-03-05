
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




warehouse_task = Task(
    name="orders_warehouse_task",
    definition="INSERT INTO mydb.myschema.orders_log VALUES (CURRENT_TIMESTAMP, 'warehouse task ran')",
    schedule=Cron("0 8 * * *", "America/Los_Angeles"),
    warehouse="compute_wh",
    suspend_task_after_num_failures=3,
    user_task_timeout_ms=600000,

    comment="Warehouse task — runs daily at 8AM using compute_wh",
)

schema.tasks.create(warehouse_task, mode=CreateMode.or_replace)
print("Warehouse task created: orders_warehouse_task")


# stream and task

from snowflake.core.stream import Stream,StreamSourceTable 

orders_stream  = Stream (
    name = 'orders_wh_stream',stream_source=StreamSourceTable(
        name = 'orders',
        append_only=True,
        show_initial_rows=False
    )
)
schema.streams.create(
    orders_stream,
    mode= CreateMode.or_replace
)


warehouse_task = Task(
    name='orders_wh_task',
    warehouse= 'compute_wh',
    definition="""
    insert into mydb.myschma.orders_processed
    select * from mydb.myschema.orders_wh_stream
    where metadata$action = 'insert'
    and system$stream_has_data('mydb.myschem.orders_wh_stream')


    """,
    suspend_task_after_num_failures=3,
    schedule= timedelta(minutes=5)
)
schema.tasks.create(
    warehouse_task,
    mode=CreateMode.or_replace
)

schema.tasks['orders_wh_task'].resume()

schema.tasks['orders_wh_task'].suspend()
schema.tasks['orders_wh_task'].delete()