from bs4 import BeautifulSoup
import time
from ehentai.conf import CATS
from curl_cffi import requests

DOMAIN_E="e-hentai.org"
URL_E="https://e-hentai.org"

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Referer":"http://www.google.com",
    "Accept":"image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
}

hosts=["104.20.19.168", "172.67.2.238", "104.20.18.168"]

def get_response(url: str,direct: bool=False,hosts=hosts,headers=headers,params=None,**args)->requests.Response:
    
    if not direct:
        for ip in hosts:
            if url.find(DOMAIN_E)!=-1:
                domain=url.split('/')[2]
                headers['Host']=domain
                url=f"{url[:url.find(domain)]}{ip}{url[url.find(domain)+len(domain):]}"
            try:
                response = requests.get(
                    url,
                    params=params,
                    impersonate="chrome",
                    headers=headers,
                    verify=False,
                    **args,
                )

                if response.ok:
                    return response
            except requests.exceptions.ConnectionError as e:
                time.sleep(1)
                print("fetch again..")
            except requests.exceptions.ReadTimeout as e:
                time.sleep(1)
                print("fetch again..")
            except Exception as e:
                time.sleep(1)
                print("fetch again..")

    return requests.get(url,params=params,headers=headers,impersonate="chrome",timeout=27.03,**args)

def keyword(
    f_search: str = None,
    f_cats: int = None,
    advsearch: bool = None,
    f_sh: bool = None,
    f_sto: bool = None,
    f_spf: int = None,
    f_spt: int = None,
    f_srdd: int = None,
    f_sfl: bool = None,
    f_sfu: bool = None,
    f_sft: bool = None,
    cats_list=None
):
    kw={}
    # search_kw
    kw["f_search"]=f_search
    # category
    if f_cats or cats_list:kw["f_cats"]=get_f_cats(f_cats,cats_list),
    # advanced search
    # show advanced options
    if advsearch or f_sh or f_sto or f_spf or f_spt or f_srdd or f_sfl or f_sfu or f_sft:kw["advsearch"]=1
    # show expunged galleries
    if f_sh:kw["f_sh"]="on"
    # require Gallery torrent
    if f_sto:kw["f_sto"]="on"
    # between {f_spf} and {f_spt} Pages
    if f_spf:kw["f_spf"]=f_spf,
    if f_spt:kw["f_spt"]=f_spt,
    # minimum_rating
    if f_srdd:kw["f_srdd"]=f_srdd,
    # disable filter language
    if f_sfl:kw["f_sfl"]="on"
    # disable filter uploader
    if f_sfu:kw["f_sfu"]="on"
    # disable filter tags
    if f_sft:kw["f_sft"]="on"
    
    return kw


def next_view(sp: BeautifulSoup):
    return sp.find('table',class_="ptt").find_all('td')[-1].find('a')

# url:target_URL
# parms:search_keyword
def get_sp(url: str,params=None,encoding=None,direct=False)->BeautifulSoup:
    # set encoding
    response=get_response(url,direct,params=params)

    if encoding:
        response.encoding=encoding

    # response info
    # print(response.encoding)
    # print(response.url)
    
    return BeautifulSoup(response.text,"lxml")


# switch categories: doujinshi...
def get_f_cats(cat_code=None,cats: list=None):
    cat_code=cat_code if cat_code else 0b0011111111
    res=0b1111111111
    if cats:
        for v in list(i.value for i in cats):
            res&=v
        return res
    
    for v in list(i.value for i in CATS):
        if cat_code&1:res&=v
        cat_code>>=1
    return res
