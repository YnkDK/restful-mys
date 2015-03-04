-- Database: restful

DROP DATABASE IF EXISTS restful;

CREATE DATABASE restful
WITH ENCODING = 'UTF8'
TABLESPACE = pg_default
LC_COLLATE = 'en_US.UTF-8'
LC_CTYPE = 'en_US.UTF-8'
CONNECTION LIMIT = -1;

COMMENT ON DATABASE restful
IS 'Toy database for the restful-mys application';


-- Sequence: auth_id_seq

DROP TABLE IF EXISTS auth;
DROP SEQUENCE IF EXISTS auth_id_seq;

CREATE SEQUENCE auth_id_seq
INCREMENT 1
MINVALUE 1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- Table: auth


CREATE TABLE auth
(
  id         BIGINT         NOT NULL DEFAULT nextval('auth_id_seq' :: REGCLASS), -- User ID
  login      CHARACTER(128) NOT NULL, -- Hexadecimal digest of login
  password   CHARACTER(60)  NOT NULL, -- The encrypted password, e.g. $2a$07$p7dX8FhxTNirJVXa9zMjHe4GXAQRNpTwIcK2Gfsi1L85BePO1DUii
  auto_token BOOLEAN        NOT NULL DEFAULT TRUE, -- True if a new token should be generated on each request, False otherwise
  CONSTRAINT login_id_key PRIMARY KEY (id),
  CONSTRAINT login_unique UNIQUE (login)
)
WITH (
OIDS =FALSE
);
COMMENT ON TABLE auth
IS 'Data for authentication';
COMMENT ON COLUMN auth.id IS 'User ID';
COMMENT ON COLUMN auth.login IS 'Hexadecimal digest of login';
COMMENT ON COLUMN auth.password IS 'The encrypted password, e.g. $2a$07$p7dX8FhxTNirJVXa9zMjHe4GXAQRNpTwIcK2Gfsi1L85BePO1DUii';


-- Index: login_hash

DROP INDEX IF EXISTS login_hash;

CREATE INDEX login_hash
ON auth
USING HASH
(login COLLATE pg_catalog."default");
COMMENT ON INDEX login_hash
IS 'Faster access for equal look-up, i.e. login = XXX';

-- Insert the user 'mys' with password 'mypassword'
INSERT INTO auth (login, password)
VALUES (
  'e89856aef4a258d48b780925ada4173bd6bebd6ce467058a7a9ba96c2d0ff1cdd51221c2cd18b94d7aea8fafb799eacd6beb0acaf84f99d83ead309ecd17a903',
  '$2a$07$sU0YdNJCEWGEMtVd4ho.3.KUyBMP7pfo6/AgKdTUG6ofPLdSlkTo2'
);