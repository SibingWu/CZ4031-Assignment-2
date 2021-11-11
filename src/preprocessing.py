# The preprocessing.py file contains any code for reading inputs and
# any preprocessing necessary to make your algorithm work
import json

import psycopg2
import logging

from annotation import annotate


class Preprocessing:
    def __init__(self, host, port, dbname, user, password):
        # connect to postgres
        try:
            conn = "host='{}' port='{}' dbname='{}' user='{}' password='{}'".format(host, port, dbname, user, password)
            self.conn = psycopg2.connect(conn)
            self.cursor = self.conn.cursor()
            logging.info("connected to database!")
        except Exception as e:
            logging.error(e)

        self.query = ''
        self.query_plan = {}
        self.annotated_plan = ""

    def parse(self, query=''):
        # parse query using postgres inner function cursor.fetchall()
        self.query = query
        logging.info('Parsing query plan for query: {}'.format(self.query))

        # simplify execution as query plan
        self.cursor.execute("EXPLAIN (FORMAT JSON) {}".format(self.query))
        query_plan = self.cursor.fetchall()
        self.query_plan = query_plan[0][0][0]['Plan']

        return self.query_plan

    def annotate(self, query_plan={}):
        self.query_plan = query_plan

        logging.info('Annotating query plan for query plan: {}'.format(json.dumps(self.query_plan, indent=4)))
        self.annotated_plan = annotate(self.query_plan, start=True)

        logging.info(self.annotated_plan)

        return self.annotated_plan


if __name__ == '__main__':
    p = Preprocessing('localhost', '5432', 'postgres', 'postgres', '123456')
    parsed_plan = p.parse('''
    select *
    from customer
    limit 5;
    ''')
    print(parsed_plan)
    annotation = p.annotate(parsed_plan)
    print(annotation)
