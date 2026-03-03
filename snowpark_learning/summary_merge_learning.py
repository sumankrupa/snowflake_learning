
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


# build and merge a summary table

session.sql("""
            create table if not exists myschema.customer_sales_summary(
            CUSTOMER_ID INT,
            TOTAL_ORDERS INT,
            TOTAL_AMOUNT FLOAT,
            LAST_UPDATED TIMESTAMP_NTZ
            )
            
            """).collect()

customer_sales_df = (
    order_df.group_by('customer_id')
    .agg(
        f.count('*').alias('TOTAL_ORDERS'),
        f.sum('amount').alias('TOTAL_AMOUNT'),
        f.current_timestamp().alias('LAST_UPDATED')
    )
)


customer_sales_df.show()

# merge the customer_sales_df to the target 


customer_sales_summary_df = session.table('myschema.customer_sales_summary')

customer_sales_summary_df.merge(
    source = customer_sales_df,
    join_expr=(customer_sales_summary_df['CUSTOMER_ID'] == customer_sales_df['CUSTOMER_ID']),
    clauses=[
        f.when_matched().update({
            'TOTAL_ORDERS':customer_sales_df['TOTAL_ORDERS'],
            'TOTAL_AMOUNT': customer_sales_df['TOTAL_AMOUNT'],
            'LAST_UPDATED':customer_sales_df['LAST_UPDATED']
        }),
        f.when_not_matched().insert({
            'CUSTOMER_ID':customer_sales_df['CUSTOMER_ID'],
            'TOTAL_ORDERS':customer_sales_df['TOTAL_ORDERS'],
            'TOTAL_AMOUNT': customer_sales_df['TOTAL_AMOUNT'],
            'LAST_UPDATED':customer_sales_df['LAST_UPDATED']
        })
    ]
)

session.table('myschema.customer_sales_summary').show()