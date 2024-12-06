CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE example.records
(
	"id"                        UUID NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    "message"                   VARCHAR(1024) NOT NULL DEFAULT ''
);
