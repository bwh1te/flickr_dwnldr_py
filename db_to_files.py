# -*- coding: utf-8 -*-

import argparse
import os
import sys

import psycopg2

from core.helpers import get_config


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Gets images from DB and store them to files')
    parser.add_argument('config', type=str, help="path to configuration file")
    parser.add_argument('destination', type=str, help="path where to store images")
    args = parser.parse_args()

    config = get_config(args.config)
    if not os.path.isdir(args.destination):
        print('Looks like {dest} is not a valid directory'.format(dest=args.destination))
        sys.exit(1)

    with psycopg2.connect(**config.DB) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, image_url, raw_data, file_hash FROM {table};".format(
                    table=config.APP['IMAGES_TABLE']
                )
            )
            for record in cur:
                id, image_url, raw_data, file_hash = record
                file_name = image_url.rpartition('/')[2]
                with open(os.path.join(args.destination, file_name), 'wb') as f:
                    print('Save {f} to {dest}'.format(f=file_name, dest=args.destination))
                    f.write(raw_data)
