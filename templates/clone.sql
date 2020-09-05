CREATE TABLE IF NOT EXISTS $target (LIKE $source);

$convert

CREATE SEQUENCE $seq_name;
ALTER TABLE $target ALTER COLUMN $pk SET DEFAULT nextval('$seq_name');
ALTER SEQUENCE $seq_name OWNED BY $target.$pk;

ALTER TABLE $target ADD PRIMARY KEY ($pk);
