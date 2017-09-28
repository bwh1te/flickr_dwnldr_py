# flickr_dwnldr_py
Script for downloading photos from Flickr by tag

## Installation
1. Prepare your PostgreSQL DB where we will store images. For example:
```
create database flickr;
create user flickr with password 'flickr';
grant all privileges on database flickr to flickr;
```
2. Get your own Flickr API key at https://www.flickr.com/services/apps/create/
3. Fill your config.ini with your settings (at least with DB credentials and Flick API key)
4. Install project requirements with running `pip install -r requirements.txt` It's desirable to use virtual environment.
5. Run `python setup.py` to create table for storing photos and additional information.

## Usage
For example: `python get_images.py Novosibirsk --config config.ini` 
More info: `python get_images.py --help`
