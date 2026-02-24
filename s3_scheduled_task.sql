-- target table

create or replace table customer(
    id    int,
    name  varchar,
    age   int,
    state varchar
);

-- file format 
create or replace file format csv_format
type = 'csv'
skip_header = 1
field_delimiter = ',';

-- storage integration 

create or replace storage integration s3_task_integration
type = external_stage
storage_provider = 's3'
enabled = true
storage_aws_role_arn = 'arn:aws:iam::285666934895:role/snowpiperole'
storage_allowed_locations = ('s3://etl-suman-files/');

desc integration s3_task_integration;

-- external stage 
create or replace stage s3_task_stage
url = 's3://etl-suman-files/task/'
storage_integration = s3_task_integration
file_format = (format_name = csv_format);
-- task

create or replace task s3_customer_task 
warehouse = 'compute_wh'
schedule = '1 minute'
as 
copy into customer from @s3_task_stage
file_format = (format_name = csv_format);



select * from customer;
-- resume task 
alter task s3_customer_task resume;

show tasks;

alter task s3_customer_task suspend;

