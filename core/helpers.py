# -*- coding: utf-8 -*-

FLICKR_ENDPOINT = 'https://api.flickr.com/services/rest/'


def image_to_url(image: dict) -> str:
    """
    Convert dict with image info into image url
    :param image: dict with image info
    :return: url
    """
    return 'http://farm{farm}.static.flickr.com/{server}/{id}_{secret}.jpg'.format(**image)
