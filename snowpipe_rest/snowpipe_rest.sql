
-- create table 

create or replace table customer(
    id    int,
    name  varchar,
    age   int,
    state varchar
);

-- create file format 

create or replace file format csv_format
    type            = 'csv'
    skip_header     = 1
    field_delimiter = ',';

create or replace storage integration s3_rest_integration
type                      = external_stage
storage_provider          = s3
enabled                   = true
storage_aws_role_arn      = 'arn:aws:iam::285666934895:role/snowpiperole'
storage_allowed_locations = ('s3://etl-suman-files/');

desc integration s3_rest_integration;

-- external stage

create or replace stage s3_rest_stage
url = 's3://etl-suman-files/rest/'
storage_integration= s3_rest_integration
file_format = (format_name = csv_format);

-- pipe auto ingest false

truncate table customer;

-- manual call
create or replace pipe s3_rest_customer_pipe 
auto_ingest = false
as 
copy into customer from @s3_rest_stage
file_format = (format_name = csv_format);

desc pipe s3_rest_customer_pipe;

select * from customer;

alter user sumankrupa963
set rsa_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArICo2A5uRO21BBKe+Nr3
m+/YlD1yDW+Oyp0mwZrr8dJUgw1U57pmbND+r76olrnltutwHBw//nraBPlYbFgO
M1Zl0Pbpm586YbUUAswxb/OpKo763AorzEkuleF9ImsdzowJXx/Ansa1ON9wZCP/
cGTaUGE/Nl2J01kdWejRLKnhartRLD90ww8Mob7wzS2jkZ/05wuaAr8cng9nJV3J
lctNZeIkmiUkGvszyqbTjQ5RQUWb2kRnfCy7XI+szEpWcLfw5aaEEKKslgnaLPny
RngrRxcW+hXbGbZIw2DZgEXiZuw6fnruOVpFK7p0m2p0R2Xq+UDfO4FGnXKoJdYl
5QIDAQAB';