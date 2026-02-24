USE ROLE accountadmin;
USE WAREHOUSE compute_wh;
USE DATABASE mydb;
USE SCHEMA myschema;


-- internal stages - user(auto),table(auto), named(user defined)

list @~;

create or replace stage my_internal_stage
    file_format = (format_name = csv_format)

    comment = 'internal stage for loading csv files';


show stages;

list @my_internal_stage;

-- upload file using python