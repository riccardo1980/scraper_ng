import logging
import os
from bs4 import BeautifulSoup
from common import get_page, save_img

def compose_page_url(search_string, page):
    url = "https://www.shutterstock.com/search?searchterm="
    url += search_string
    url += "&sort=popular"
    url += "&image_type=all"
    url += "&search_source=base_landing_page"
    url += "&language=en"
    url += "&page="+str(page)
    return url

def scrape_page(data):
    scraper = BeautifulSoup(data, "lxml")
    container_list = scraper.find_all("div", {"class":"z_c_b"})
    img_uris = []
    for container in container_list:
        imgs = container.find_all("img")
        for img in imgs:
            img_uris.append(img.get("src"))

    return img_uris

def imagescrape(search_terms, destination, pages):
    """
    Shutterstock image scrape

    Parameters
    ---------

    search_terms: list of str
        list of terms to search.

    destination: str
        destination folder.

    pages: int
        number of pages to scrape
    -

    """

    search_string = '+'.join(search_terms)
    try:
        for page in range(1, pages+1):

            logging.info('Getting page %d', page)
            url = compose_page_url(search_string, page)
            data = get_page(url, unverified_ctx=True)

            logging.info('Parsing page %d', page)
            img_uris = scrape_page(data)

            for img_src in img_uris:
                img_name = os.path.basename(img_src)
                img_dest = os.path.join(destination, img_name)

                logging.info('Downloading %s', img_src)
                try:
                    save_img(img_src, img_dest, unverified_ctx=True)

                except Exception as e:
                    logging.warning(e)

    except Exception as e:
        logging.warning(e)
