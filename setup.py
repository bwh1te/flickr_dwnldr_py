# -*- coding: utf-8 -*-

import argparse
import textwrap

import psycopg2

from core.helpers import get_config


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

    config = get_config(args.config)

    with psycopg2.connect(**config.DB) as conn:
        with conn.cursor() as cur:
            table_exist = cur.execute(
                "SELECT to_regclass('{table}');".format(table=config.APP['IMAGES_TABLE'])
            )
            if not table_exist:
                print('Table {table} will be created...'.format(table=config.APP['IMAGES_TABLE']))
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
                '''.format(table=config.APP['IMAGES_TABLE']))
                print('Done!')
            else:
                print('Table {table} has already created!'.format(table=config.APP['IMAGES_TABLE']))
