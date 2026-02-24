use role accountadmin;
use warehouse compute_wh;

create role if not exists data_engineer_role;

create user if not exists  dev_user
    password = 'TempPass@123'
    default_role = data_engineer_role
    default_warehouse = compute_wh
    default_namespace = mydb.myschema
    must_change_password = true;

-- grant role to the user
grant role data_engineer_role to user dev_user;

-- grant priviliges to role
grant usage on warehouse compute_wh to role data_engineer_role;
grant usage on database mydb to role data_engineer_role;

grant usage on schema mydb.myschema to role data_engineer_role;

grant select on all tables in schema mydb.myschema to role data_engineer_role;

-- verify
show users;
show roles;
show grants to role data_engineer_role;
show grants to user dev_user;

