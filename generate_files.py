import os
from string import Template
import psycopg2
import argparse

parser = argparse.ArgumentParser()

args_general = parser.add_argument_group(title="General Options")
args_general.add_argument('-t', '--table_name', default='test', help='table to be copied. target table with have _copy as a suffix')
args_general.add_argument('-c', '--columns', default='id', help='list the columns to be converted to bigint eg. col1,col2,col3')
args_general.add_argument('-p', '--primary_key', default='id', help='primary key of the table for which a new sequence is created in the copy table')

args = parser.parse_args()

table_name = args.table_name
if not os.path.exists('generated/{}'.format(table_name)):
        os.makedirs('generated/{}'.format(table_name))
pk = args.primary_key
columns = args.columns
raw_convert = columns.split(',')
convert = []

for c in raw_convert:
    convert.append('ALTER TABLE {} ALTER COLUMN {} TYPE bigint'.format(table_name+"_copy", c))

def create_clone(table_name, pk, convert):
    template = open('templates/clone.sql')
    src = Template(template.read())

    d = {'source': table_name, 'target': table_name+"_copy", 'pk': pk, 'seq_name': table_name+"_copy"+"_id"+"_seq", 'convert': '\n'.join(convert)}

    result = src.substitute(d)
    f = open("generated/{0}/{0}_clone.sql".format(table_name), "a")
    f.write(result)
    f.close


def create_indexes(table_name):
    try:
        conn = psycopg2.connect("dbname=postgres")
    except psycopg2.Error as e:
        print("Failed to connect to the database: ", e.pgcode)

    template = open('templates/trigger.sql')
    src = Template(template.read())

    query = "select replace(indexdef,'INDEX', 'INDEX CONCURRENTLY') from pg_indexes where tablename = '{}'".format(table_name)
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    template = open('templates/indexes.sql')
    src = Template(template.read())

    d = {'indexes': '\n'.join(list(str(row) for row in rows))}
    result = src.substitute(d)
    f = open("generated/{0}/{0}_indexes.sql".format(table_name), "a")
    f.write(result)
    f.close


def create_trigger(table_name, pk):
    template = open('templates/trigger.sql')
    src = Template(template.read())

    d = {'source': table_name, 'target': table_name+"_copy", 'pk': pk, 'tname': table_name+"_trig", 'b': "$BODY$"}

    result = src.substitute(d)
    f = open("generated/{0}/{0}_trig.sql".format(table_name), "a")
    f.write(result)
    f.close


def grant_acl(table_name):

    try:
        conn = psycopg2.connect("dbname=postgres")
    except psycopg2.Error as e:
        print("Failed to connect to the database: ", e.pgcode)

    query = "select 'GRANT ' || privilege_type || ' ON ' || table_name || ' TO ' || grantee || ';' from information_schema.role_table_grants where table_name = '{}' and grantee <> grantor;".format(table_name, table_name)

    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    template = open('templates/acl.sql')
    src = Template(template.read())
 
    d = {'acl': '\n'.join(str(row) for row in rows)}
    result = src.substitute(d)
    f = open("generated/{0}/{0}_acl.sql".format(table_name), "a")
    f.write(result)
    f.close


def main():

    create_trigger(table_name, pk)
    create_clone(table_name, pk, convert)
    grant_acl(table_name)
    create_indexes(table_name)


if __name__ == "__main__":
    main()
