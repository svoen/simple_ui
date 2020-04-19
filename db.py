#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
from psycopg2.extensions import AsIs
import datetime

connection = psycopg2.connect(user='',
                              password='',
                              host='0.0.0.0',
                              port='',
                              database='')#??

cursor = connection.cursor()




def execute(command):
    try:
        if type(command) == str:
            cursor.execute(command)
            result = cursor.fetchall()
            return result
        elif type(command) == tuple:
            cursor.execute(command[0], command[1])
            connection.commit()
    except Exception as e:
        print(e)


def insert(table, dict):

    columns = dict.keys()
    values = [dict[column] for column in columns]
    print(columns)
    print(values)
    insert_statement = """insert into {} (%s) values %s""".format(table)

    cursor.mogrify(insert_statement, (AsIs(','.join(columns)), tuple(values)))
    connection.commit()

