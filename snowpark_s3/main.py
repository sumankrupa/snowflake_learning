from snowflake.snowpark import Session
from snowflake.snowpark.types import StructType, StructField, IntegerType, StringType
from snowflake.snowpark.functions import col
from dotenv import load_dotenv
import os

load_dotenv()
connection_params = {
    "account"   : os.getenv('SNOWFLAKE_ACCOUNT'),
    "user"      : os.getenv('SNOWFLAKE_USER'),
    "password"  : os.getenv('SNOWFLAKE_PASSWORD'),          # or use key pair (see below)
    "role"      : os.getenv('SNOWFLAKE_ROLE'),
    "warehouse" : os.getenv('SNOWFLAKE_WAREHOUSE'),
    "database"  : os.getenv('SNOWFLAKE_DATABASE'),
    "schema"    : os.getenv('SNOWFLAKE_SCHEMA')
}

session = Session.builder.configs(connection_params).create()

# define schema
schema = StructType([
    StructField('id',IntegerType()),
    StructField('name',StringType()),
    StructField('age',IntegerType()),
    StructField('state',StringType())
])

# stage to df

df = (session.read.
      schema(schema).
      option('skip_header',1).
      option('field_delimiter',',').
      csv('@s3_snowpark_stage')
      
      )
    
df.show()
# write to table
df.write.mode('overwrite').save_as_table('customer')
session.table('customer').show()

session.close()