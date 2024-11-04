DROP SCHEMA IF EXISTS sch_alumni CASCADE;
CREATE SCHEMA sch_alumni;
SET SEARCH_PATH TO sch_alumni;

DROP TABLE IF EXISTS tbl_alumni;
DROP TABLE IF EXISTS tbl_experience;
DROP TABLE IF EXISTS tbl_education;

CREATE TABLE tbl_alumni (
    fld_alm_id_pk VARCHAR(255) PRIMARY KEY,
    fld_alm_full_name VARCHAR(50) NOT NULL,
    fld_alm_title VARCHAR(255),
    fld_alm_city VARCHAR(100),
    fld_alm_state VARCHAR(100),
    fld_alm_country VARCHAR(100),
    CONSTRAINT full_name_length CHECK (LENGTH(fld_alm_full_name) <= 50)
);

CREATE TABLE tbl_experience (
    fld_exp_id_pk SERIAL PRIMARY KEY,
    fld_exp_id_fk VARCHAR(255),
    fld_exp_company VARCHAR(50),
    fld_exp_title VARCHAR(255),
    fld_exp_location VARCHAR(200),
    fld_exp_starts_at DATE,
    fld_exp_ends_at DATE,
    fld_exp_description TEXT,
    CONSTRAINT fk_experience_alumni FOREIGN KEY (fld_exp_id_fk) REFERENCES tbl_alumni(fld_alm_id_pk)
);

CREATE TABLE tbl_education (
    fld_edu_id_pk SERIAL PRIMARY KEY,
    fld_edu_id_fk VARCHAR(255),
    fld_edu_full_name VARCHAR(50),
    fld_edu_school VARCHAR(255),
    fld_edu_degree_name VARCHAR(200),
    fld_edu_field_of_study VARCHAR(200),
    fld_edu_starts_at DATE,
    fld_edu_ends_at DATE,
    fld_edu_description TEXT,
    CONSTRAINT fk_education_alumni FOREIGN KEY (fld_edu_id_fk) REFERENCES tbl_alumni(fld_alm_id_pk)
);
