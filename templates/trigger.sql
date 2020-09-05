CREATE OR REPLACE FUNCTION $table_name()
  RETURNS trigger AS
<BODY>
BEGIN
        IF ( TG_OP = 'INSERT') THEN
                INSERT INTO $table_name VALUES((NEW).*);
                RETURN NEW;
        ELSIF ( TG_OP = 'DELETE') THEN
                DELETE FROM $table_name WHERE $pk = OLD.$pk;
                RETURN OLD;
        END IF;          
END;
<BODY> LANGUAGE plpgsql;

CREATE TRIGGER $table_name BEFORE DELETE ON $table_name FOR EACH ROW EXECUTE PROCEDURE $table_name();

$convert
