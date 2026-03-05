
from snowflake.snowpark import Session
import os
from dotenv import load_dotenv
import snowflake.snowpark.functions as f
from snowflake.core import Root

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

# create a stream on a source table
from snowflake.core.stream import  Stream, StreamSourceTable

from snowflake.core import CreateMode

stream_on_table = Stream(
    name = 'orders_stream',
    stream_source = StreamSourceTable(
        name = 'orders',
        append_only = True,
        show_initial_rows = False
    )
)
root.databases['mydb'].schemas['myschema'].streams.create(
    stream_on_table,
    mode=CreateMode.or_replace
    # mode=CreateMode.if_not_exists
    # mode=CreateMode.error_if_exists
)


# create a stream on a source view


from snowflake.core.stream import Stream, StreamSourceView,PointOfTimeOffset

from snowflake.core import CreateMode

stream_on_view = Stream(
    name = 'orders_view_stream',
    stream_source = StreamSourceView(
        name = 'orders_view',
        point_of_time= PointOfTimeOffset(reference = 'at',offset = '0'),
    ),
    comment = 'Stream on orders_view'
)


root.databases['mydb'].schemas['myschema'].streams.create(
    stream_on_view,
    mode = CreateMode.or_replace
)

# clone a stream
from snowflake.core.stream import Stream

if not root.databases['mydb'].schemas['myschema'].streams["my_stream"]:
  root.databases['mydb'].schemas['myschema'].streams.create("my_stream", clone_stream="orders_stream")


stream = root.databases['mydb'].schemas['myschema'].streams["my_stream"]
stream_details = stream.fetch()
print(stream_details.to_dict())

# list all streams

stream_list = root.databases['mydb'].schemas['myschema'].streams.iter()
for i in stream_list:
  print(i.name)

# dropping a stream 

stream = root.databases['mydb'].schemas['myschema'].streams["my_stream"]
stream.drop()

