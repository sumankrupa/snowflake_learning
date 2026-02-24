-- target table

drop table customer;
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

-- storage integratoin

create or replace storage integration s3_external_table
type = external_stage
storage_provider = 's3'
enabled = true
storage_aws_role_arn = 'arn:aws:iam::285666934895:role/snowpiperole'
storage_allowed_locations = ('s3://etl-suman-files/');

desc integration s3_external_table;

-- external stage 
create or replace stage s3_table_stage
url ='s3://etl-suman-files/external_table/'
storage_integration = s3_external_table
file_format = (format_name = csv_format);


-- external table 

create or replace external table ext_customer (
    id    int as (value:c1::int),
    name  varchar as (value:c2::varchar),
    age   int as (value:c3::int),
    state varchar as (value:c4::varchar)
)
location = @s3_table_stage
file_format = (format_name = csv_format)
auto_refresh = true;

select * from ext_customer;

insert into customer 
select id,name,age,state from ext_customer;

