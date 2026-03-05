
from snowflake.snowpark import Session
import os
from dotenv import load_dotenv
import snowflake.snowpark.functions as f
from snowflake.core import Root,CreateMode

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



# tasks -automate data processing and business procedures through pipeline
# ways to run
# 1. scheduled times
# 2. triggered by events (such as when new data arrives in a stream)


# what can tasks do
# 1. run sql and stroed proc
# 2. for complex you can use task graphs.

# steps 
# 1. appropriate role
# 2. define the task (compute resource, schedule/trigger, fail condition, add session params)
# 3. resume task
# 4. monitor task costs 
# 5. refine the task 

# compute resource - 2ways
# 1. serverless tasks: snowflake handles auto
# 2. user managed vw

# target completion interval


# 1. serverless

from snowflake.core.task import Task , Cron
from datetime import timedelta

task1 = Task(
    name = "orders_serverless_task",
    definition= "insert into mydb.myschema.orders select * from mydb.myschema.orders",
    schedule = Cron("0 * * * *", "America/Los_Angeles"),
    # serverless_task_min_statement_size="SMALL",
    # serverless_task_max_statement_size="XXLARGE",
    # target_completion_interval = timedelta(minutes = 120),
    # user_task_timeout_ms = 6000 (10 mins),
    # suspend_task_after_num_failures = 3
    )

my_tasks = root.databases['mydb'].schemas['myschema'].tasks
my_tasks.create(
    task1,
    mode=CreateMode.or_replace
)
print('serverless task created')

# stream triggered task

stream_task1 = Task(
    name = "orders_stream_task",
    definition= """
    insert into mydb.myschema.orders
    select * from mydb.myschmea.orders_stream
    where metedata$action = 'insert'
    and system$stream_has_data('mydb.myschema.orders_stream') """,
    target_completion_interval= timedelta(minutes=10),
    schedule= timedelta(minutes=10),
        

)

my_tasks.create(
    stream_task1,
    mode=CreateMode.or_replace
)

print('serverless stream task created')


# dag 
# Task(
#     name,
#     definition=,
#     target_completion_interval=,
#     predecessors= ['parent_task']
# )

my_tasks['orders_serverless_task'].resume()
my_tasks['orders_stream_task'].resume()

# .execute() manual run
# .delete() 
my_tasks['orders_serverless_task'].suspend()
my_tasks['orders_stream_task'].suspend()