-- clone objects using time travel - at before

-- timetravel takes time and also statement

create schema s2 clone myschema at(timestamp => '2026-03-04')

-- create schema s2 clone myschema before(statement => '')