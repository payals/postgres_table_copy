from string import Template

def create_trigger():
    template = open('templates/trigger.sql')
    src = Template(template.read())

    table_name = "test"
    pk = "id"
    convert = ['first', 'second', 'third']
     
    d={'table_name':table_name, 'pk':pk, 'convert':'\n'.join(convert)}

    result = src.substitute(d)
    print(result)

def main():
    create_trigger()

if __name__ == "__main__":
    main()
