CREATE TABLE hospital_table (patient_id INTEGER,
                             patient_name VARCHAR, 
                             billing_address VARCHAR,
                             diagnosis VARCHAR, 
                             treatment VARCHAR,
                             cost NUMBER(10,2));


INSERT INTO hospital_table 
        (patient_ID, patient_name, billing_address, diagnosis, treatment, cost) 
    VALUES
        (1, 'Mark Knopfler', '1982 Telegraph Road', 'Industrial Disease', 
            'a week of peace and quiet', 2000.00),
        (2, 'Guido van Rossum', '37 Florida St.', 'python bite', 'anti-venom', 
            70000.00)
        ;

CREATE VIEW doctor_view AS
    SELECT patient_ID, patient_name, diagnosis, treatment FROM hospital_table;

CREATE VIEW accountant_view AS
    SELECT patient_ID, patient_name, billing_address, cost FROM hospital_table;


select distinct diagnosis from doctor_view;

-- non material - no cost, no store, slow
-- materialized - cost, store, fast


-- both can be defined as secure. - data privacy, data sharing 