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


# 9. window functions

from snowflake.snowpark import Window
import snowflake.snowpark.functions as f


window_spec = Window.partition_by().order_by(f.col('age').desc())
df.show()
df.with_column('row_num',f.row_number().over(window_spec))\
    .with_column('rank',f.rank().over(window_spec))\
    .with_column('dense_rank',f.dense_rank().over(window_spec)).show()

df.with_column('running_age_sum',f.sum('age').over(window_spec))\
    .with_column('prev_age',f.lag('age',1).over(window_spec))\
    .with_column('next_age',f.lead('age',1).over(window_spec)).show()


# 10.vectorized udf

# normal age(0 to 1)
import pandas as pd
from snowflake.snowpark.functions import pandas_udf

@pandas_udf(return_type = t.FloatType(),input_types = [t.FloatType()])
def double_age(age:pd.Series) -> pd.Series:
    return age*2
df.with_column('double_Age',double_age(f.col('age'))).show()


# ex1. normalize age

@pandas_udf(return_type = t.FloatType(),input_types = [t.FloatType()])
def normalize(age:pd.Series) -> pd.Series:
    return (age - age.min() )/ (age.max()  - age.min())

# ex2. clean a string

@pandas_udf(return_type = t.StringType(),input_types = [t.StringType()])
def clean_String(s :pd.Series) ->pd.Series:
    return s.str.strip().str.title()

df.with_column('clean_name',clean_String(f.col('name'))).show()


# ex3. age category
@pandas_udf(return_type = t.StringType(),input_types = [t.FloatType()])
def age_category(age:pd.Series) -> pd.Series:
    bins = [0,35,55,100]
    labels = ['young','mid','old']
    return pd.cut(age,bins = bins ,labels=labels, right = False).astype(str)

df.with_column('category',age_category(f.col('age'))).show()

# 11.null




# 12. null and condition when when otherwise
df_case = df.with_column(
    'age_band',
    f.when(f.col('age').is_null(),f.lit('unknown'))
    .when(f.col('age') < 35,f.lit('kid'))
    .when((f.col('age') >= 35) & (f.col('age') < 55),f.lit('unc'))
    .otherwise(f.lit('zoom'))
)

df_case =df_case.with_column(
    'state_clean',
    f.when(f.col('state').is_null,f.lit('unkown'))
    .otherwise(f.trim(f.col('state')))
)
df_case.select("id", "age", "AGE_BAND").show()



customer_df = session.table('MYSCHEMA.CUSTOMER')

order_df = session.table('MYSCHEMA.orders')


orders_update_df = session.create_dataframe(
    [
        (102,2,210.50,'DELIVERED'),(105,5,460.63,'DELIVERED'),(106,1,80.01,'PLACED')
    ],
    schema=['ORDER_ID','CUSTOMER_ID','AMOUNT','STATUS']
)
orders_update_df