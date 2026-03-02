import os
from dotenv import load_dotenv
from snowflake.snowpark import Session, Row
import snowflake.snowpark.functions as f
import snowflake.snowpark.types as t

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
print(session.sql("SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE()").collect())

# 3. DataFrames
df = session.table('MYSCHEMA.CUSTOMER')
df1 = session.sql('SELECT * FROM MYSCHEMA.EVENT')

# 4. Transformations
df.select('id', 'name', 'age', 'state').show()
df.filter(f.col('age') > 20).show()
df.with_column('Price', f.lit(20)).show()
df.group_by('age').agg(f.avg("age").alias("AVG_AGE")).show()
df.sort(f.col('age').desc()).show()

# Join
dummy_df = session.create_dataframe([
    Row(id=1, CATEGORY="Young"),
    Row(id=2, CATEGORY="Mid"),
    Row(id=3, CATEGORY="Senior"),
    Row(id=4, CATEGORY="Elder"),
    Row(id=5, CATEGORY="Retired")
])

merged_df = df.join(dummy_df, df['id'] == dummy_df['id'])
merged_df.show()

# 5. Actions
df.show()                                               # print results
rows = df.collect()                                     # returns list of Row objects
print(rows)
count = df.count()                                      # returns row count
print(count)
pandas_df = df.to_pandas()                              # convert to pandas (needs pandas installed)
print(pandas_df)

# 6. Writing Data
# df.write.mode('overwrite').save_as_table('MYSCHEMA.MYTABLE')
# df.write.mode('append').save_as_table('MYSCHEMA.MYTABLE')

# # 7. UDF — fix indentation
from snowflake.snowpark.functions import udf

@udf(return_type=t.FloatType(), input_types=[t.FloatType(), t.FloatType()])
def calculate_margin(cost, price):
    return (price - cost) / price * 100

# Use the UDF
df.with_column('Price', f.lit(20))\
    .with_column('Margin', calculate_margin(f.col('age'), f.lit(100))) \
  .show()


# 8. stored procedures


def my_first_sproc(session: Session) -> str:
    df = session.table('myschema.customer')
    count = df.count()
    return str(count)

# Register the function
session.sproc.register(
    func=my_first_sproc,
    name='my_first_sproc',
    replace=True,
    is_permanent=False,             
    packages=['snowflake-snowpark-python'] 
)

result = session.call('my_first_sproc')
print(f'Result: {result}')