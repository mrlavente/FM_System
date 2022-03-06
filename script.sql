create table data
(
    report_id        INTEGER not null
        primary key,
    species_name     VARCHAR(100),
    date_report      VARCHAR(100),
    location         VARCHAR(100),
    site             VARCHAR(100),
    no_observation   INTEGER,
    mode_observation VARCHAR(100),
    threats          VARCHAR(100),
    remarks          VARCHAR(1000),
    name_observers   VARCHAR(500),
    coordinates_lat  FLOAT,
    coordinates_lng  FLOAT
);

create table population
(
    population_id INTEGER not null
        primary key,
    park_name     VARCHAR(100),
    pop_name      VARCHAR(100),
    pop_date      VARCHAR(100),
    population_no INTEGER,
    park_add      VARCHAR(100)
);


