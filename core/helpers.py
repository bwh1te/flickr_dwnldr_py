# -*- coding: utf-8 -*-

import configparser
import os
import sys

from collections import namedtuple


FlickrDwnldrConfig = namedtuple('FlickrDwnldrConfig', 'DB FLICKR APP')


def image_to_url(image: dict) -> str:
    """
    Convert dict with image info into image url
    :param image: dict with image info
    :return: url
    """
    return 'http://farm{farm}.static.flickr.com/{server}/{id}_{secret}.jpg'.format(**image)


def get_config(config_path):
    """
    :param config_path: path to configuration file
    :return: named tuple (DB, FLICKR, APP) with dicts with configuration params
    """
    config = configparser.ConfigParser()
    config.read(config_path)
    try:
        return FlickrDwnldrConfig(
            # config_tuple.DB, dict with DB credentials
            {
                'dbname': config['DB']['NAME'],
                'host': config['DB']['HOST'],
                'port': config['DB']['PORT'],
                'user': config['DB']['USER'],
                'password': config['DB']['PASSWORD'],
            },
            # config_tuple.FLICKR, dict with Flickr API key and secret
            {
                'KEY': os.getenv('FLICKR_KEY', config['FLICKR']['KEY']),
                'SECRET': os.getenv('FLICKR_SECRET', config['FLICKR']['SECRET'])
            },
            # config_tuple.APP, dict with application level settings
            {
                'MAX_IMAGE_COUNT': config['APP'].getint('MAX_IMAGE_COUNT'),
                'IMAGES_PER_PAGE': config['APP'].getint('IMAGES_PER_PAGE'),
                'IMAGES_TABLE': config['APP']['IMAGES_TABLE']
            }
        )
    except KeyError as e:
        print('Please check that {key} is specified in {filename}'.format(key=e.args[0],
                                                                          filename=config_path))
        sys.exit(1)
