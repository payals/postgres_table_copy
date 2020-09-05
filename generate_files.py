from string import Template
import psycopg2
#import argparse


def create_clone(table_name, pk, convert):
    template = open('templates/clone.sql')
    src = Template(template.read())

    d = {'source': table_name, 'target': table_name+"_copy", 'pk': pk, 'seq_name': table_name+"_copy"+"_id"+"_seq", 'convert': '\n'.join(convert)}

    result = src.substitute(d)
    print(result)

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
    print(result)



def create_trigger(table_name, pk):
    template = open('templates/trigger.sql')
    src = Template(template.read())

    d = {'source': table_name, 'target': table_name+"_copy", 'pk': pk, 'tname': table_name+"_trig", 'b': "$BODY$"}

    result = src.substitute(d)
    print(result)


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
    print(result)


def main():

    table_name = "test"
    pk = "id"
    convert = ['col1', 'col2', 'col3']
    create_trigger(table_name, pk)
    create_clone(table_name, pk, convert)
    grant_acl(table_name)
    create_indexes(table_name)


if __name__ == "__main__":
    main()
