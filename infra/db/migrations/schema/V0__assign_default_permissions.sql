CREATE SCHEMA example;

ALTER ROLE example WITH NOCREATEDB NOCREATEROLE NOINHERIT;

GRANT USAGE ON SCHEMA example TO example;

ALTER DEFAULT PRIVILEGES IN SCHEMA example GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO example;