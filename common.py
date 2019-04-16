import ssl
from six.moves.urllib.request import urlopen, urlretrieve

def get_resource(url, unverified_ctx=False):
    """
    Get resource from url

    Parameters
    ----------

    url: str
        resource url

    unverified_ctx: bool
        if True, do not use ssl verification


    Output
    ------
    res: str
        UTF-8 encoded string containing the resource
    """

    if unverified_ctx:
        ssl._create_default_https_context = ssl._create_unverified_context

    return urlopen(url).read().decode('utf-8')

def save_resource(url, dest, unverified_ctx=False):
    """
    Save resource from url

    Parameters
    ----------

    url: str
        resource url

    dest: str
        destination resource

    unverified_ctx: bool
        if True, do not use ssl verification

    """
    if unverified_ctx:
        ssl._create_default_https_context = ssl._create_unverified_context
    urlretrieve(url, dest)
