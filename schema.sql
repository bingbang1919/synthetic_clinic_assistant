PRAGMA foreign_keys = ON;
CREATE TABLE patient (
 patient_id INTEGER PRIMARY KEY,
 first_name TEXT NOT NULL,
 last_name TEXT NOT NULL,
 date_of_birth TEXT NOT NULL
);
CREATE TABLE provider (
 provider_id INTEGER PRIMARY KEY,
 provider_name TEXT NOT NULL,
 specialty TEXT NOT NULL
);
CREATE TABLE visit (
 visit_id INTEGER PRIMARY KEY,
 patient_id INTEGER NOT NULL REFERENCES patient(patient_id),
 provider_id INTEGER NOT NULL REFERENCES provider(provider_id),
 visit_date TEXT NOT NULL,
 visit_type TEXT NOT NULL CHECK(visit_type IN ('Routine','Follow-up','Urgent'))
);
CREATE TABLE condition (
 condition_id INTEGER PRIMARY KEY,
 condition_name TEXT NOT NULL UNIQUE
);
CREATE TABLE patient_condition (
 patient_id INTEGER NOT NULL REFERENCES patient(patient_id),
 condition_id INTEGER NOT NULL REFERENCES condition(condition_id),
 diagnosis_date TEXT NOT NULL,
 PRIMARY KEY(patient_id, condition_id)
);
CREATE TABLE medication (
 medication_id INTEGER PRIMARY KEY,
 medication_name TEXT NOT NULL UNIQUE
);
CREATE TABLE prescription (
 prescription_id INTEGER PRIMARY KEY,
 patient_id INTEGER NOT NULL REFERENCES patient(patient_id),
 medication_id INTEGER NOT NULL REFERENCES medication(medication_id),
 provider_id INTEGER NOT NULL REFERENCES provider(provider_id),
 start_date TEXT NOT NULL,
 end_date TEXT,
 dose TEXT NOT NULL,
 CHECK(end_date IS NULL OR end_date >= start_date)
);
CREATE INDEX ix_visit_patient_date ON visit(patient_id, visit_date);
CREATE INDEX ix_condition_condition ON patient_condition(condition_id);
CREATE INDEX ix_prescription_patient ON prescription(patient_id);
