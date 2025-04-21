from ehentai.fetch import Gallery,Page
from ehentai.connect import URL_E, get_sp, keyword

def get_Page(url: str=URL_E,params=None,encoding: str=None,direct: bool=False)->Page:
    """
    Args:
        url (str, optional): ehentai has the galleries. Defaults to URL_E.
        params (fetch.keyword, optional): use this to search. Defaults to None.
        encoding (str, optional): 'utf-8'..,use this when encoding is wrong. Defaults to None.
        direct  (bool,optional): enable this to connect directly
    Returns:
        Page:
            attr:gl_table,rangebar,search_text
    """
    return Page(get_sp(url,params,encoding,direct))

def get_search(search_content,cats_code=None,rating=None,expunged=None,torrent=None,cats_list=None,**args)->Page:
    return get_Page(
        url=URL_E,
        params=keyword(
            f_search=search_content,
            f_cats=cats_code,
            f_srdd=rating,
            f_sh=expunged,
            f_sto=torrent,
            cats_list=cats_list
        ),
        **args
    )

def get_popular(**args):
    return get_Page(url="https://e-hentai.org/popular",**args)