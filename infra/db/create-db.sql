CREATE ROLE flyway LOGIN PASSWORD 'flyway_pwd' SUPERUSER CREATEDB CREATEROLE REPLICATION;
CREATE ROLE example LOGIN PASSWORD 'example_pwd' CREATEDB CREATEROLE INHERIT;
CREATE ROLE example_ro LOGIN PASSWORD 'example_ro_pwd' CREATEDB CREATEROLE INHERIT;

CREATE DATABASE "example";