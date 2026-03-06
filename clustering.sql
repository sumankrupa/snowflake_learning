SELECT SYSTEM$CLUSTERING_INFORMATION('mydb.myschema.orders', '(order_date)');


-- clustering 
-- by default sf organizes the clusters.
-- it tell sf to physically reorganize the micro partitions so rows with 
-- same cluster key value are stored together

-- caches

-- 3 types
-- metadata cache 
-- result cache - data after the query
-- virtual warehouse cache - data in the vw that can be used for another query.


--  system schemas
-- information_schema - one db, object metadata
-- snowflake.accoutn_usage - entire account, 45min -3 hr, cost monitor,auditing

CREATE OR REPLACE TABLE mydb.myschema.orders (
    order_id     NUMBER,
    customer_id  NUMBER,
    order_amount NUMBER,
    status       VARCHAR,
    region       VARCHAR,
    order_date   DATE
);

INSERT INTO mydb.myschema.orders VALUES
    (1001, 501, 250,  'PLACED',    'NORTH', '2024-01-05'),
    (1002, 502, 1500, 'SHIPPED',   'SOUTH', '2024-01-12'),
    (1003, 503, 89,   'DELIVERED', 'EAST',  '2024-02-03'),
    (1004, 504, 3200, 'PLACED',    'WEST',  '2024-02-18'),
    (1005, 505, 450,  'CANCELLED', 'NORTH', '2024-03-07'),
    (1006, 506, 780,  'SHIPPED',   'SOUTH', '2024-03-22'),
    (1007, 507, 5000, 'DELIVERED', 'EAST',  '2024-04-10'),
    (1008, 508, 120,  'PLACED',    'WEST',  '2024-04-25'),
    (1009, 509, 960,  'SHIPPED',   'NORTH', '2024-05-14'),
    (1010, 510, 2200, 'DELIVERED', 'SOUTH', '2024-05-30');

ALTER TABLE mydb.myschema.orders
CLUSTER BY (order_date);



SELECT SYSTEM$CLUSTERING_INFORMATION('mydb.myschema.orders', '(order_date)');



-- Check clustering depth after enabling
SELECT SYSTEM$CLUSTERING_DEPTH('mydb.myschema.orders', '(order_date)');


-- Remove clustering (stops auto-maintenance, reduces costs if not needed)
ALTER TABLE mydb.myschema.orders DROP CLUSTERING KEY;

-- Multi-column clustering: cluster by date AND region together
-- Use this when you ALWAYS filter on both columns together
ALTER TABLE mydb.myschema.orders
    CLUSTER BY (order_date, region);


-- warehouse sizing


ALTER WAREHOUSE compute_wh SET WAREHOUSE_SIZE = 'LARGE';

ALTER WAREHOUSE compute_wh SET WAREHOUSE_SIZE = 'XSMALL';
ALTER WAREHOUSE compute_wh SET AUTO_SUSPEND = 60;

ALTER WAREHOUSE compute_wh SET AUTO_RESUME = TRUE;

select table_name,
row_count,
bytes / 1024 /1024 as size_mb,
created,
last_altered from mydb.information_schema.tables 
where table_schema = 'MYSCHEMA'
order by bytes DESC;



-- List all columns in a table with their data types
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM mydb.information_schema.columns
WHERE table_schema = 'MYSCHEMA'
  AND table_name   = 'ORDERS';


SELECT table_name as view_name, view_definition
FROM mydb.information_schema.views
WHERE table_schema = 'MYSCHEMA';

SELECT stage_name, stage_type, stage_url
FROM mydb.information_schema.stages
WHERE stage_schema = 'MYSCHEMA';



-- Check query history for the current session (last 7 days, real-time)
SELECT
    query_id,
    query_text,
    execution_status,
    total_elapsed_time / 1000   AS duration_seconds,
    bytes_scanned / 1024 / 1024 AS mb_scanned,
    start_time
FROM TABLE(mydb.information_schema.query_history())
ORDER BY start_time DESC
LIMIT 20;