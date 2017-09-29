# -*- coding: utf-8 -*-

import argparse

import psycopg2
from psycopg2.extensions import AsIs

from core import funcs
from core.helpers import get_config


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Gets images from Flickr and store them to DB')
    parser.add_argument('geotag', type=str, help="location name")
    parser.add_argument("--config", help="path to configuration file")
    parser.add_argument("--place", action='store_true',
                        help="find through place name instead of image tag")
    args = parser.parse_args()

    config = get_config(args.config)

    image_query_params = dict(
        per_page=config.APP['IMAGES_PER_PAGE'],
        privacy_filter=1,
        sort='relevance'
        # geo_context='2',  # strange but doesn't work
    )

    if args.place:
        places = funcs.get_places(config.FLICKR['KEY'], args.geotag)
        image_query_params.update({'place_id': places[0]['place_id']})
    else:
        image_query_params.update({'tags': args.geotag})

    with psycopg2.connect(**config.DB) as conn:
        with conn.cursor() as cur:
            images = funcs.get_photos(
                config.FLICKR['KEY'],
                config.APP['MAX_IMAGE_COUNT'],
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
                        'table': AsIs(config.APP['IMAGES_TABLE']),
                        'url': image['url_l'],
                        'raw_data': psycopg2.Binary(image['raw_data']),
                        'lat': image['latitude'],
                        'long': image['longitude'],
                        'hash': image['file_hash']
                    }
                )
