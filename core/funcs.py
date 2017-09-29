# -*- coding: utf-8 -*-

import hashlib
from typing import Dict, List, Generator

import requests

from .constants import FLICKR_ENDPOINT


REQUEST_BASE_DATA = dict(
    format='json',
    nojsoncallback='1'
)


def get_places(api_key: str, query: str) -> List[Dict]:
    """
    Finds places by name using flickr.photos.search endpoint
    :param api_key: Flickr API key
    :param query: search query
    :return: list of dicts with places info
    """
    resp = requests.get(
        FLICKR_ENDPOINT,
        params=dict(
            api_key=api_key,
            method='flickr.places.find',
            query=query,
            **REQUEST_BASE_DATA
        )
    )
    try:
        resp_json = resp.json()
        return resp_json['places']['place']
    except KeyError:
        return list()


def get_photos(api_key: str, max_images: int, query_params: dict) -> Generator[Dict, None, None]:
    """
    Finds photos by params using flickr.photos.search endpoint
    :param api_key: Flickr API key
    :param max_images: Maximum images count to download
    :param query_params: dict of params compatible with flickr.photos.search endpoint
    :return: generator of dicts with photos info extended with files raw data
    """
    current_page, total_pages = 1, 1
    images_processed = 0

    while current_page <= total_pages and images_processed < max_images:
        resp = requests.get(
            FLICKR_ENDPOINT,
            params=dict(
                api_key=api_key,
                method='flickr.photos.search',
                extras='geo,url_l,place_id',
                page=current_page,
                **REQUEST_BASE_DATA,
                **query_params
            )
        )
        resp_json = resp.json()

        for photo in resp_json['photos']['photo']:
            try:
                photo_file = requests.get(photo['url_l'])
                yield dict(
                    **photo,
                    raw_data=photo_file.content,
                    file_hash=hashlib.md5(photo_file.content).hexdigest()
                )
                images_processed += 1
                if images_processed >= max_images:
                    break
            except KeyError:
                continue

        current_page += 1
        total_pages = int(resp_json['photos']['pages'])
