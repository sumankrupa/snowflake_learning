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
field_delimiter = ','

-- storage integration

create or replace storage integration s3_integration
type = external_stage
storage_provider = s3
enabled = true
storage_aws_role_arn = 'arn:aws:iam::285666934895:role/snowpiperole'
storage_allowed_locations = ('s3://etl-suman-files/');

desc integration s3_integration;

-- external stage

create or replace stage s3_stage
url = 's3://etl-suman-files/event/'
storage_integration = s3_integration
file_format = csv_format;


-- snowpipe 
create or replace pipe s3_load_customer_pipe 
auto_ingest = true
as 
copy into customer from @s3_stage
file_format = (format_name = csv_format)
on_error = 'continue'
;



-- desc pipe 
desc pipe s3_load_customer_pipe;

-- load 

select * from customer;

