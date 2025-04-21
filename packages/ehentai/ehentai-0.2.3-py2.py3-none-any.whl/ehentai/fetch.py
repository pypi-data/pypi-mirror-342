from bs4 import BeautifulSoup
import os
from ehentai.conf import FONT_STYLE,CATS_BG_COLOR,RESET
from ehentai.connect import get_sp,next_view,get_response
import time
# book
class Gallery:
    name=""#名字
    cover=""#封面
    view_url=""#视图超链接
    cat=""#类别
    tags=[]#标签
    s_tags=[]#simply tags
    def __init__(self,name=None,cover=None,view_url=None,cat=None,tags=None,s_tags=None):
        self.name=name
        self.cover=cover
        self.view_url=view_url
        self.cat=cat
        self.tags=tags
        self.s_tags=s_tags
    
    def __str__(self):
        return f"Cat:{FONT_STYLE.bold.value}{CATS_BG_COLOR[self.cat]}{self.cat:^12}{RESET}\tURL:{FONT_STYLE.underline.value}{self.view_url}{RESET}\nName:\t{self.name}\nTags:\t{self.s_tags}\n{"_"*20}"
    def __repr__(self):
        return f"<{self.name}>"
    
    def download(self,name=None,path=None,img_suffix="webp",show=True,stream=True,chunk_size=8192):
        start_time=time.time()
        if show:
            print("fetching the URL...")
        path=path if path else "./"
            
        view=get_sp(self.view_url)
        # get the html of the image
        images=list(map(lambda x:x.get('href'),view.find('div',id="gdt").find_all('a')))
        while next_view(view):
            view=get_sp(next_view(view).get('href'))
            images.extend(list(map(lambda x:x.get('href'),view.find('div',id="gdt").find_all('a'))))
        
        # images num
        totals=len(images)
        if show:
            print(f"Totals:{totals}")

        fdir=os.path.join(path,name if name else self.name)
        os.makedirs(fdir) if not os.path.exists(fdir) else None

        for i,v in enumerate(images):

            if show:
                print(f"Downloading...{i+1}/{totals}")

            img_src=get_sp(v).find('img',id="img").get('src')
            img=get_response(img_src,stream=stream)
            with open(os.path.join(fdir,f"{i}.{img_suffix}"),"wb") as f:
                if stream:
                    for chunk in img.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            f.flush()
                else:
                    f.write(img.content)
            
        if show:
            print(f"Completed!! consum:{time.time()-start_time}")
    
    # @return:list(author,list[str])
    def comment(self):
        table=get_sp(self.view_url,encoding='utf-8').find_all('div',class_="c1")
        return list(map(lambda v:(v.find('div',class_="c3").find('a').string,v.find('div',class_="c6").strings),table))


class Page:
    def __str__(self):
        return f"{"-"*50}\nPage:{self.search_text}\n{"-"*50}"
    def __init__(self,sp=None,gl_table:list[Gallery]=[],rangebar=None,search_text=None):
        # prevurl,nexturl,maxdate,mindate,rangeurl,rangemin,rangemax,rangespan
        self.rangebar:dict[str:any]={"prevurl":"","nexturl":"","maxdate":"","mindate":"","rangeurl":"","rangemin":"","rangemax":"","rangespan":""}
        self.search_text="Not Found"
        self.gl_table: list[Gallery] = list(
            map(
                lambda v: Gallery(
                    name=v["name"],
                    cover=v["cover"],
                    view_url=v["view_url"],
                    cat=v["cat"],
                    tags=v["tags"],
                    s_tags=v["s_tags"],
                ),
                gl_table,
            )
        )
        if rangebar:
            self.rangebar=rangebar
        if search_text:
            self.search_text=search_text

        if sp:
            if sp.find('head'):
                self.set_rangebar(sp)
                self.set_search_text(sp)
                self.fetch_gl(sp)
            else:
                self.search_text=sp.get_text()

    def set_rangebar(self,sp: BeautifulSoup):
        rangebar_script=sp.find_all('script',type="text/javascript")
        if rangebar_script:
            rangebar_script=rangebar_script[-1].get_text().splitlines()[1:-1]
            for s in rangebar_script:
                self.rangebar[s[s.find(" ")+1:s.find("=")]]=s[s.find("=")+1:-1].strip("\"")
    def set_search_text(self,sp: BeautifulSoup):
        t=sp.find('div',class_="searchtext")
        if t:
            self.search_text=t.get_text()
        # print(search_text)
    def fetch_gl(self,sp: BeautifulSoup):
        table=sp.find('table',class_="itg gltc")
        if table:
            trs=list(filter(lambda x:x.find('td',class_="gl1c glcat"),table.find_all('tr')))
            for tr in trs:
                # ['gl1c glcat','gl2c','gl3c glname','gl4c glhide']
                td=tr.find_all('td')
                self.gl_table.append(Gallery(
                    name=td[2].find('div',class_="glink").get_text(),
                    cover=td[1].find('img').get('data-src'),
                    view_url=td[2].find('a').get('href'),
                    cat=td[0].find('div').get_text(),
                    tags=list(map(lambda x:x.get('title'),td[2].find_all('div',class_="gt"))),
                    s_tags=list(map(lambda x:x.get_text(),td[2].find_all('div',class_="gt"))),
                ))
