#!/usr/local/bin/python3

import time, psycopg2
import argparse
import pp

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description='backfill table data in batches', epilog='''------
                                 USAGE:
                                 ------
                                    Use the listed options to provide connection details for the script. 
                                    Script will divide the table size and run jobs in parallel 
                                 ------''')

args_general = parser.add_argument_group(title="General options")
args_general.add_argument('-n', '--hostname', default="localhost", help='database endpoint')
args_general.add_argument('-u', '--user', default="postgres", help='user to log into the database with')
args_general.add_argument('-w', '--password', default="''", help='password for the user')
args_general.add_argument('-d', '--dbname', default="postgres", help='database name')
args_general.add_argument('-s', '--source_table', default="test", help='table to backfill data from')
args_general.add_argument('-t', '--target_table', default="test_copy", help='table to copy data to')
args_general.add_argument('-p', '--primary_key', default="id", help='primary key column of source table')
args_general.add_argument('-b', '--batch_size', default=10000, help='number of rows to copy per commit (higher the value, higher the time taken per commit due to concurrency)')
args_general.add_argument('-i', '--sleep_interval', default=0.1, help='sleep between each commit can allow other jobs to run which might be waiting. 1s is recommended')

args = parser.parse_args()

connstr = "dbname={} user={} password={} host={}".format(args.dbname, args.user, args.password, args.hostname)
target = args.target_table
src = args.source_table
pk = args.primary_key
batch_size = args.batch_size
interval = args.sleep_interval

def backfill(lower_id, higher_id, batch_size, target, src, pk, interval, connstr):
    conn = psycopg2.connect(connstr)
    cur = conn.cursor()
    i = lower_id
    j = i + batch_size
    while i <= higher_id:
        query = "INSERT INTO {} SELECT * FROM {} WHERE {} BETWEEN {} AND {} ON CONFLICT DO NOTHING".format(target, src, pk, i, j)
        cur.execute(query)
        conn.commit();
#        print (time.time(), ' - latest updated id:', i)
        i = i + batch_size + 1
        j = j + batch_size
        time.sleep(interval)

#    print('Done')


def main():
    start_time = time.time()

    # Connect to the database
    try:
        print(connstr)
        conn = psycopg2.connect(connstr)
    except psycopg2.Error as e:
        print("Unable to connect:" + str(e.pgerror))

    # Start pp server
    job_server = pp.Server()
    print( "Starting pp with", job_server.get_ncpus(), "workers")
    parallel_jobs = round(job_server.get_ncpus()/2)
    print("Spawning {} parallel jobs across {} cores".format(parallel_jobs, job_server.get_ncpus()))

    # Get min and max IDs of the source table
    query = "SELECT max({}), min({}) from {}".format(pk, pk, src)
    cur = conn.cursor()
    cur.execute(query)
    row = cur.fetchone()
    cur.close()
    max_id = row[0]
    min_id = row[1]

    # Prepare arguments for backfill function
    lower_id = min_id - 1                           # backfill function uses sql BETWEEN operator to insert in batches, and between excludes the lower and higher values
    chunk = round(max_id / parallel_jobs)           # total row by number of parallel jobs allowed split the table evently for each job
    higher_id = chunk
    print("splitting in chunks of {} and commit batch size of {}".format(chunk, batch_size))

    # Spawn parallel insert jobs divided into chunks, divided into batches
    jobs = []
    for i in range(parallel_jobs):
        print("calling function: backfill({}, {}, {}, {}, {}, {}, {})".format(lower_id, higher_id, batch_size, target, src, pk, interval))
        jobs.append(job_server.submit(backfill, (lower_id, higher_id, batch_size, target, src, pk, interval, connstr), (), ("psycopg2","time",)))
        lower_id = higher_id + 1
        higher_id = higher_id + chunk

    for job in jobs:
        result = job()
        if result:
            break

    print("Time elapsed: ", time.time() - start_time, "s")
    job_server.print_stats()

if __name__ == "__main__":
    main()
