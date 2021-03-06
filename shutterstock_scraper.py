import logging
import os
import re
from bs4 import BeautifulSoup
from common import get_resource, save_resource

def compose_page_url(search_string, page):
    url = "https://www.shutterstock.com/search?searchterm="
    url += search_string
    url += "&sort=popular"
    url += "&image_type=all"
    url += "&search_source=base_landing_page"
    url += "&language=en"
    url += "&page="+str(page)

    return url

def get_data_from_url(page_url_list):
    """
    For get a resource for each url

    Parameters
    ----------

    page_url_list: list of str
        list of url search

    Output
    ------

    resource_list: list of str
        list of str containing resource

    """
    total_page_url = len(page_url_list)
    page_data_list = []
    for idx, page_url in enumerate(page_url_list):

        logging.info('Downloading page %d/%d %s',
                     idx+1,
                     total_page_url,
                     page_url)
        try:
            data = get_resource(page_url,
                            unverified_ctx=True)
            page_data_list.append(data)

        except Exception as e:
            logging.warning(e)

    return page_data_list

def scrape_page(data):
    """
    Get uri of images returned by search page

    Parameters
    ----------

    data: str
        resource to be scraped

    Output
    ------

    list of uri of image

    """
    scraper = BeautifulSoup(data, "lxml")
    container_list = scraper.find_all("div", {"class":"z_e_b"})
    img_uris = []
    for container in container_list:
        imgs = container.find_all("img")
        for img in imgs:
            img_uris.append(img.get("src"))

    return img_uris

def scrape_pages(page_data_list):
    """
    Scrape pages

    Parameters
    ----------

    page_data_list: str
        list of resources to be scraped

    Output
    ------

    list of uri of image

    """
    total_page_data = len(page_data_list)
    img_url_list = []
    for idx, page_data in enumerate(page_data_list):

        logging.info('Parsing page %d/%d',
                     idx+1,
                     total_page_data)
        try:
            imgs = scrape_page(page_data)
            img_url_list.extend(imgs)

        except Exception as e:
            logging.warning(e)

    return img_url_list

def get_total_pages(data):
    """
    Get number of pages, given a page containing search results

    Parameters
    ----------

    data: str
        resource containing search results page

    Output
    ------
    pages : int
        total number of pages
    """
    scraper = BeautifulSoup(data, "lxml")
    end_string = scraper.find_all("div", {"class":"b_M_f"})[0].text
    pattern = re.compile(r'[a-zAZ]*\s(\d+)$')
    pages = int(pattern.findall(end_string)[0])

    return pages

def save_images(img_url_list, destination):
    """
    Save images in list

    Parameters
    ----------
    img_url_list: list of str
        list of url of images

    """
    total_images = len(img_url_list)
    for idx, img_src in enumerate(img_url_list):
        url = "https://image.shutterstock.com/"
        img_name = img_src.replace(url, '').replace('/', '_')
        img_dest = os.path.join(destination,
                                img_name)

        logging.info('Downloading item %d/%d %s',
                     idx+1,
                     total_images,
                     img_src)
        try:
            save_resource(img_src, img_dest, unverified_ctx=True)

        except Exception as e:
            logging.warning(e)

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

    """

    search_string = '+'.join(search_terms)

    # get first page to have bounds
    url = compose_page_url(search_string, 1)
    data = get_resource(url, unverified_ctx=True)
    pages_tot = get_total_pages(data)
    pages_max = min(pages, pages_tot)

    # compose url list
    page_url_list = []
    for page in range(1, pages_max+1):
        page_url_list.append(compose_page_url(search_string,
                                              page))

    # get data from url
    page_data_list = get_data_from_url(page_url_list)

    # get img list for url
    img_url_list = scrape_pages(page_data_list)

    # download img
    save_images(img_url_list, destination)
