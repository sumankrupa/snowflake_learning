from snowflake.ingest import SimpleIngestManager
from snowflake.ingest import StagedFile
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import os


with open('rsa_key.pem', 'r') as f:
   
        private_key_pem = f.read()
       
ACCOUNT       = 'GLMIMDW-OT80024'      
USER          = 'SUMANKRUPA963'
PIPE_NAME     = 'MYDB.MYSCHEMA.S3_REST_CUSTOMER_PIPE'


files = [
    StagedFile('customer.csv', None),
]

ingest_manager = SimpleIngestManager(
    account = ACCOUNT,
    host = f'{ACCOUNT}.snowflakecomputing.com',
    user = USER,
    pipe = PIPE_NAME,
    private_key = private_key_pem
)

response = ingest_manager.ingest_files(files)
print(f'response: {response}')