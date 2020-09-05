CREATE TABLE IF NOT EXISTS $table_name_copy (LIKE $table_name);
ALTER TABLE $table_name_copy ALTER COLUMN item_extra_id TYPE bigint;
ALTER TABLE $table_name_copy ALTER COLUMN item_extra_option_id TYPE bigint;
ALTER TABLE $table_name_copy ALTER COLUMN id TYPE bigint;
CREATE SEQUENCE $table_name_copy_id_seq;
ALTER TABLE $table_name_copy ALTER COLUMN id SET DEFAULT nextval('$table_name_copy_id_seq');
ALTER SEQUENCE $table_name_copy_id_seq OWNED BY $table_name_copy.id;
ALTER TABLE $table_name_copy ADD PRIMARY KEY (id);
