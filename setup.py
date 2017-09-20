# -*- coding: utf-8 -*-

import argparse
import configparser
import sys
import textwrap

import psycopg2


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            Setup DB tables for get_images.py script
            ========================================
            Make sure that: 
                1. The DB credentials in your config file is right
                2. The DB is created
                3. The user has permissions to create tables''')
    )
    parser.add_argument('config', type=str, help="path to configuration file")
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config)

    try:
        DB_CONNECTION_PARAMS = {
            'dbname': config['DB']['NAME'],
            'host': config['DB']['HOST'],
            'port': config['DB']['PORT'],
            'user': config['DB']['USER'],
            'password': config['DB']['PASSWORD'],
        }
        TABLE_NAME = config['APP']['IMAGES_TABLE']
    except KeyError as e:
        print('Please check that {key} is specified in {filename}'.format(key=e.args[0],
                                                                          filename=args.config))
        sys.exit(1)

    with psycopg2.connect(**DB_CONNECTION_PARAMS) as conn:
        with conn.cursor() as cur:
            table_exist = cur.execute(
                "SELECT to_regclass('{table}');".format(table=TABLE_NAME)
            )
            if not table_exist:
                print('Table {table} will be created...'.format(table=TABLE_NAME))
                cur.execute('''\
                  CREATE TABLE {table} (
                    id serial PRIMARY KEY,
                    image_url VARCHAR(100),
                    raw_data BYTEA,
                    lat FLOAT,
                    long FLOAT,
                    file_hash VARCHAR(32),
                    timestamp TIMESTAMP default CURRENT_TIMESTAMP
                  );
                '''.format(table=TABLE_NAME))
                print('Done!')
            else:
                print('Table {table} has already created!'.format(table=TABLE_NAME))
