# -*- coding: utf-8 -*-

import argparse
import configparser
import sys

import psycopg2
from psycopg2.extensions import AsIs


from core import funcs

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Gets images from Flickr and store them to DB')
    parser.add_argument('geotag', type=str, help="location name")
    parser.add_argument("--config", help="path to configuration file")
    parser.add_argument("--place", action='store_true',
                        help="find through place name instead of image tag")
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
        FLICKR_KEY = config['FLICKR']['KEY']
        MAX_IMAGE_COUNT = config['APP'].getint('MAX_IMAGE_COUNT')
        IMAGES_PER_PAGE = config['APP'].getint('IMAGES_PER_PAGE')
        TABLE_NAME = config['APP']['IMAGES_TABLE']
    except KeyError as e:
        print('Please check that {key} is specified in {filename}'.format(key=e.args[0],
                                                                          filename=args.config))
        sys.exit(1)

    image_query_params = dict(
        per_page=IMAGES_PER_PAGE,
        privacy_filter=1,
        sort='relevance'
        # geo_context='2',  # strange but doesn't work
    )

    if args.place:
        places = funcs.get_places(FLICKR_KEY, args.geotag)
        image_query_params.update({'place_id': places[0]['place_id']})
    else:
        image_query_params.update({'tags': args.geotag})

    with psycopg2.connect(**DB_CONNECTION_PARAMS) as conn:
        print('Connected!')

        with conn.cursor() as cur:
            print('Got cursor!')
            images = funcs.get_photos(
                FLICKR_KEY,
                MAX_IMAGE_COUNT,
                image_query_params
            )
            for image in images:
                if image['latitude'] == 0 or image['longitude'] == 0:
                    continue
                print('Downloading {}'.format(image['url_l']))
                cur.execute("""\
                    INSERT INTO %(table)s (image_url, raw_data, lat, long, file_hash)
                    VALUES (%(url)s, %(raw_data)s, %(lat)s, %(long)s, %(hash)s)""",
                    {
                        'table': AsIs(TABLE_NAME),
                        'url': image['url_l'],
                        'raw_data': psycopg2.Binary(image['raw_data']),
                        'lat': image['latitude'],
                        'long': image['longitude'],
                        'hash': image['file_hash']
                    }
                )
