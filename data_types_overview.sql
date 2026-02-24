USE ROLE accountadmin;
USE WAREHOUSE compute_wh;
USE DATABASE mydb;
USE SCHEMA myschema;


create or replace table data_type_demo(
    id int,
    age smallint,
    salary decimal(10,2),
    rating float,

    first_name varchar,
    last_name string,
    bio text,

    is_active boolean,

    birth_date date,
    created_at timestamp_ntz,
    updated_at timestamp_ltz,

    -- semi structured
    metadata variant,
    tags array,
    address object,

    profile_pic binary
    
    
    
    );
INSERT INTO data_type_demo 
    select 
    1, 28, 95000.50, 4.8,
    'Suman', 'Krupa', 'Data Engineer Intern',
    TRUE,
    '1996-05-15', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(),
    PARSE_JSON('{"team": "data", "level": "junior"}'),
    ARRAY_CONSTRUCT('snowflake', 'python', 'sql'),
    OBJECT_CONSTRUCT('city', 'Dallas', 'state', 'TX'),
    NULL ;