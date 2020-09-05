This repository contains the utilities required for converting table data from int to bigint

SQL files are generated in `generated/<table_name>` sub-directories

### Arguments:

Run the script with `-h` or `--help` to see arguments and option details

### Batch run:

```
$ python3 batch.py
dbname=postgres user=postgres password='' host=localhost
Starting pp with 8 workers
Spawning 4 parallel jobs across 8 cores
splitting in chunks of 25000000 and commit batch size of 10000
calling function: backfill(0, 25000000, 10000, test_copy, test, id, 0.1)
calling function: backfill(25000001, 50000000, 10000, test_copy, test, id, 0.1)
calling function: backfill(50000001, 75000000, 10000, test_copy, test, id, 0.1)
calling function: backfill(75000001, 100000000, 10000, test_copy, test, id, 0.1)
Time elapsed:  306.8411967754364 s
Job execution statistics:
 job count | % of all jobs | job time sum | time per job | job server
         4 |        100.00 |     1223.5495 |   305.887373 | local
Time elapsed since server creation 306.2634189128876
0 active tasks, 8 cores
```

### SQL generation example:

Run the script with `--help` to see argument details. 

For example, `python3 generate_file.py --c id,cost` generates the following output:

```
(base) payalmac:postgres_table_copy payal$ python3 generate_files.py -t test -c id,cost -p id
(base) payalmac:postgres_table_copy payal$ ls -l generated/test/
total 32
-rw-r--r--  1 payal  staff   105 Sep  5 02:50 test_acl.sql
-rw-r--r--  1 payal  staff  1998 Sep  5 02:50 test_clone.sql
-rw-r--r--  1 payal  staff   166 Sep  5 02:50 test_indexes.sql
-rw-r--r--  1 payal  staff   626 Sep  5 02:50 test_trig.sql
(base) payalmac:postgres_table_copy payal$ cat generated/test/test_trig.sql
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
(base) payalmac:postgres_table_copy payal$ cat generated/test/test_clone.sql
CREATE TABLE IF NOT EXISTS test_copy (LIKE test);

ALTER TABLE test_copy ALTER COLUMN id TYPE bigint
ALTER TABLE test_copy ALTER COLUMN cost TYPE bigint

CREATE SEQUENCE test_copy_id_seq;
ALTER TABLE test_copy ALTER COLUMN id SET DEFAULT nextval('test_copy_id_seq');
ALTER SEQUENCE test_copy_id_seq OWNED BY test_copy.id;

ALTER TABLE test_copy ADD PRIMARY KEY (id);
```
