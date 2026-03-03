
from snowflake.snowpark import Session
import os
from dotenv import load_dotenv
import snowflake.snowpark.functions as f

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

customer_df = session.table('MYSCHEMA.CUSTOMER')

order_df = session.table('MYSCHEMA.orders')


orders_update_df = session.create_dataframe(
    [
        (102,2,210.50,'DELIVERED'),
        (105,5,460.63,'DELIVERED'),
        (106,1,80.01,'PLACED')
    ],
    schema=['ORDER_ID','CUSTOMER_ID','AMOUNT','STATUS']
)


order_df.merge(
    source = orders_update_df,
    join_expr=(order_df['order_id'] == orders_update_df['order_id']),
    clauses=[
        f.when_matched().update({
            'CUSTOMER_ID': orders_update_df['CUSTOMER_ID'],
            'AMOUNT': orders_update_df['amount'],
            'status': orders_update_df['status']
        }),
        f.when_not_matched().insert({
            'order_id':orders_update_df['order_id'],
            'CUSTOMER_ID': orders_update_df['CUSTOMER_ID'],
            'AMOUNT': orders_update_df['amount'],
            'status': orders_update_df['status']
        }),
    ]
)

session.table('myschema.orders').show()


