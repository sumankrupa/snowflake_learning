USE ROLE accountadmin;
USE WAREHOUSE compute_wh;
USE DATABASE mydb;
USE SCHEMA myschema;

create or replace file format csv_format
    type = 'csv'
    field_delimiter = ','
    record_delimiter = '\n'
    skip_header = 1
    null_if = ('null','Null','')
    empty_field_as_null = true 
    compression = none;



create or replace file format json_format
    type = 'json'
    strip_outer_array = true
    ignore_utf8_errors = true
    compression = none;


create or replace file format parquet_format
    type = 'parquet'
    
    compression = snappy;





CREATE OR REPLACE FILE FORMAT avro_format
    TYPE = 'AVRO'
    COMPRESSION = NONE;


CREATE OR REPLACE FILE FORMAT orc_format
    TYPE = 'ORC';


CREATE OR REPLACE FILE FORMAT xml_format
    TYPE = 'XML'
    COMPRESSION = NONE;

-- verify
SHOW FILE FORMATS IN SCHEMA mydb.myschema;


DESCRIBE FILE FORMAT csv_format;