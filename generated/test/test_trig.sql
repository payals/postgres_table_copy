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
