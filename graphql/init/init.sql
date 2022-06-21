CREATE SCHEMA default_schema;

CREATE TABLE default_schema.author(
    id BIGSERIAL NOT NULL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL
);

ALTER TABLE default_schema.author ADD CONSTRAINT unique_credentials UNIQUE (username, email);

CREATE TABLE default_schema.post(
    id BIGSERIAL NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    created_at DATE DEFAULT CURRENT_DATE,
    author_id INTEGER NOT NULL REFERENCES default_schema.author(id)
);


