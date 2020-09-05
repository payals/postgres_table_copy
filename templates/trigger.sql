CREATE OR REPLACE FUNCTION $source()
  RETURNS trigger AS
$b
BEGIN
        IF ( TG_OP = 'INSERT') THEN
                INSERT INTO $target VALUES((NEW).*);
                RETURN NEW;
        ELSIF ( TG_OP = 'UPDATE' ) THEN
                DELETE FROM $target WHERE $pk = NEW.$pk;
                INSERT INTO $target VALUES((NEW).*);
        ELSIF ( TG_OP = 'DELETE') THEN
                DELETE FROM $target WHERE $pk = OLD.$pk;
                RETURN OLD;
        END IF;          
END;
$b LANGUAGE plpgsql;

CREATE TRIGGER $tname BEFORE INSERT OR UPDATE OR DELETE ON $source FOR EACH ROW EXECUTE PROCEDURE $source();
