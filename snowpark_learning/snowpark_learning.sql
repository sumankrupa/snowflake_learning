-- run in Snowflake first
create or replace table employees (
    id         int,
    name       varchar,
    salary     int,
    department varchar,
    age        int,
    state      varchar
);

insert into employees values
(1,  'Alice',   95000, 'Engineering', 30, 'TX'),
(2,  'Bob',     45000, 'Marketing',   25, 'CA'),
(3,  'Charlie', 72000, 'Engineering', 35, 'TX'),
(4,  'Diana',   88000, 'HR',          28, 'NY'),
(5,  'Eve',     61000, 'Marketing',   32, 'CA'),
(6,  'Frank',   null,  'Engineering', 40, 'TX'),
(7,  'Grace',   55000, 'HR',          27, null),
(8,  'Henry',   79000, 'Engineering', 33, 'NY'),
(9,  'Iris',    92000, 'Marketing',   29, 'CA'),
(10, 'Jack',    48000, null,          31, 'TX');


create or replace file format csv_format
    type            = 'csv'
    skip_header     = 1
    field_delimiter = ',';

create or replace storage integration s3_snowpark_integration
type                      = external_stage
storage_provider          = s3
enabled                   = true
storage_aws_role_arn      = 'arn:aws:iam::285666934895:role/snowpiperole'
storage_allowed_locations = ('s3://etl-suman-files/');

desc integration s3_snowpark_integration;

-- external stage

create or replace stage s3_snowpark_stage
url = 's3://etl-suman-files/snowpark_files/'
storage_integration = s3_snowpark_integration
file_format = (format_name= csv_format);


list @s3_snowpark_stage;


truncate table employees;

select * from employees;