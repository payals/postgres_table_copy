from string import Template
import psycopg2
#import argparse


def create_clone(table_name, pk, convert):
    template = open('templates/clone.sql')
    src = Template(template.read())

    d = {'source': table_name, 'target': table_name+"_copy", 'pk': pk, 'seq_name': table_name+"_copy"+"_id"+"_seq", 'convert': '\n'.join(convert)}

    result = src.substitute(d)
    print(result)


def create_trigger(table_name, pk):
    template = open('templates/trigger.sql')
    src = Template(template.read())

    d = {'source': table_name, 'target': table_name+"_copy", 'pk': pk, 'tname': table_name+"_trig", 'b': "$BODY$"}

    result = src.substitute(d)
    print(result)


def main():

    try:
        conn = psycopg2.connect("dbname=postgres")
    except psycopg2.Error as e:
        print("Failed to connect to the database: ", e.pgcode)

    table_name = "test"
    pk = "id"
    convert = ['first', 'second', 'third']
    create_trigger(table_name, pk)
    create_clone(table_name, pk, convert)


if __name__ == "__main__":
    main()
