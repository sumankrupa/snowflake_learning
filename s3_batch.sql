-- target table 

create or replace table customer(
    id int,
    name varchar,
    age int,
    state varchar
);

-- file format

create or replace file format csv_format
type = 'csv'
skip_header = 1
field_delimiter = ',';

-- storage integration

create or replace storage integration s3_batch_integration
type = external_stage
storage_provider = s3 
enabled = true 
storage_aws_role_arn = 'arn:aws:iam::285666934895:role/snowpiperole'
storage_allowed_locations = ('s3://etl-suman-files/');

desc integration s3_batch_integration;
-- external stage
create or replace stage s3_batch_stage
url = 's3://etl-suman-files/batch/'
storage_integration = s3_batch_integration
file_format = csv_format;
-- batch load 



copy into customer from @s3_batch_stage
file_format = (format_name = csv_format);

