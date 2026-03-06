-- Databases

-- Tables

-- Dynamic tables

-- External tables

-- Externally managed and managed Apache Iceberg™ tables

-- Externally managed Delta Lake tables (with Delta Direct and catalog-linked databases)

-- Views

-- Regular views

-- Secure views

-- Secure materialized views

-- Semantic views

-- Cortex Search services

-- User-defined functions (UDFs) (secure and non-secure)

-- Models of type USER_MODEL, CORTEX_FINETUNED, or DOC_AI



-- you can share the above objects

-- cost = storage+compute 
-- when you share the customer doesnt share the cost. 

-- 2 ways to share
-- grant priviliges on object directly to a share
-- grant priviliges on objects to a share via role

create or replace share orders_direct_share;
grant usage on database mydb
to share orders_direct_share;

alter share orders_direct_share
add accounts = consumer_account_locator;



-- via role

create or replace share orders_role_share;

-- custom role for share

create or replace role orders_share_role;

grant usage on database mydb
to role orders_share_role;

grant role orders_share_role
to share orders_role_share;