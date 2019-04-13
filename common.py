import ssl
from six.moves.urllib.request import urlopen, urlretrieve

def get_page(url, unverified_ctx=False):
    if unverified_ctx:
        ssl._create_default_https_context = ssl._create_unverified_context

    return urlopen(url).read().decode('utf-8')

def save_img(img_src, img_dest, unverified_ctx=False):
    if unverified_ctx:
        ssl._create_default_https_context = ssl._create_unverified_context
    urlretrieve(img_src, img_dest)
