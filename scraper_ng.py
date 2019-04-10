#!/usr/bin/env python
import argparse
import logging
import os

from shutterstock_scraper import imagescrape
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Shutterstock Scraper')

    parser.add_argument('--destination', '-d',
                        type=str, default='./data',
                        help='destination folder')

    parser.add_argument('--pages', '-p',
                        type=int, default=1,
                        help='number of pages')

    parser.add_argument('search_terms', nargs='+',
                        type=str,
                        help='search terms')

    args = vars(parser.parse_args())

    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)

    if not os.path.exists(args['destination']):
        os.makedirs(args['destination'])

    imagescrape(**args)
