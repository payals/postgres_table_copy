CREATE TABLE IF NOT EXISTS test_copy (LIKE test);

ALTER TABLE test_copy ALTER COLUMN id TYPE bigint
ALTER TABLE test_copy ALTER COLUMN cost TYPE bigint

CREATE SEQUENCE test_copy_id_seq;
ALTER TABLE test_copy ALTER COLUMN id SET DEFAULT nextval('test_copy_id_seq');
ALTER SEQUENCE test_copy_id_seq OWNED BY test_copy.id;

ALTER TABLE test_copy ADD PRIMARY KEY (id);
CREATE OR REPLACE FUNCTION test()
  RETURNS trigger AS
$BODY$
BEGIN
        IF ( TG_OP = 'INSERT') THEN
                INSERT INTO test_copy VALUES((NEW).*);
                RETURN NEW;
        ELSIF ( TG_OP = 'UPDATE' ) THEN
                DELETE FROM test_copy WHERE id = NEW.id;
                INSERT INTO test_copy VALUES((NEW).*);
        ELSIF ( TG_OP = 'DELETE') THEN
                DELETE FROM test_copy WHERE id = OLD.id;
                RETURN OLD;
        END IF;          
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER test_trig BEFORE INSERT OR UPDATE OR DELETE ON test FOR EACH ROW EXECUTE PROCEDURE test();
CREATE TABLE IF NOT EXISTS test_copy (LIKE test);

ALTER TABLE test_copy ALTER COLUMN id TYPE bigint
ALTER TABLE test_copy ALTER COLUMN cost TYPE bigint

CREATE SEQUENCE test_copy_id_seq;
ALTER TABLE test_copy ALTER COLUMN id SET DEFAULT nextval('test_copy_id_seq');
ALTER SEQUENCE test_copy_id_seq OWNED BY test_copy.id;

ALTER TABLE test_copy ADD PRIMARY KEY (id);
('GRANT SELECT ON test TO rita;',)
('GRANT INSERT ON test TO tina;',)
('GRANT UPDATE ON test TO tina;',)
('CREATE UNIQUE INDEX CONCURRENTLY test_pkey ON public.test USING btree (id)',)
('CREATE UNIQUE INDEX CONCURRENTLY test_cost_idx ON public.test USING btree (cost)',)
CREATE TABLE IF NOT EXISTS test_copy (LIKE test);

ALTER TABLE test_copy ALTER COLUMN id TYPE bigint
ALTER TABLE test_copy ALTER COLUMN cost TYPE bigint

CREATE SEQUENCE test_copy_id_seq;
ALTER TABLE test_copy ALTER COLUMN id SET DEFAULT nextval('test_copy_id_seq');
ALTER SEQUENCE test_copy_id_seq OWNED BY test_copy.id;

ALTER TABLE test_copy ADD PRIMARY KEY (id);
