import sys
import os
import json
import click
import json
from click import echo
from typing import List
from ehentai.conf import *
from ehentai import __version__
from ehentai import Page,Gallery,get_search,get_popular

HOME=os.path.abspath(os.path.join(os.getenv('HOME'),".hentai"))

if not os.path.exists(HOME):
    os.makedirs(HOME)

def echo_gl_table(detail=False,gl_table: List[Gallery]=None):
    if gl_table:
        if detail:
            for i,gl in enumerate(gl_table):
                echo(f"{i:^3}{gl}")
        else:
            for i,gl in enumerate(gl_table):
                echo(f"{i:^3}{FONT_STYLE.bold.value}{CATS_BG_COLOR[gl.cat]}{gl.cat:^12}{RESET}{gl.name}")
    else:
        echo("Page's Gallery Table is None.")


def save_json(filename: str,data: object):
    with open(os.path.join(HOME,filename),"w") as f:
        f.write(json.dumps(data,default=lambda obj:obj.__dict__))
def load_json(filename: str,data_type):
    with open(os.path.join(HOME,filename),"r") as f:
        return data_type(**json.loads(f.read()))

page: Page


@click.group()
def cli():
    pass
@cli.command(help="|show the version")
def version():
    echo(f"""{FONT_COLOR.pink.value}
██╗  ██╗███████╗███╗   ██╗████████╗ █████╗ ██╗
██║  ██║██╔════╝████╗  ██║╚══██╔══╝██╔══██╗██║
███████║█████╗  ██╔██╗ ██║   ██║   ███████║██║
██╔══██║██╔══╝  ██║╚██╗██║   ██║   ██╔══██║██║
██║  ██║███████╗██║ ╚████║   ██║   ██║  ██║██║
╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚═╝
{RESET}""")
    echo(f"Version: {__version__.__version__}")
    
@cli.command(help="|search from e-hentai")
@click.option('--search-content','-s',default="",type=str,prompt=True,help="search content,tags")
@click.option('--cats','-c',default=255,type=int,help="Doujinshi,Manga...")
@click.option('--rating','-r',default=None,type=int,help="the minium rating")
@click.option('--show-expunged/--no-show-expunged','-sh/',default=False,help="show the removed galleries")
@click.option('--show-torrent/--no-show-torrent','-sto/',default=False,help="filter galleries have torrent")
@click.option('--use-direct/--no-direct','-u',default=False,help="enable this to connect directly")
def search(search_content,cats,rating,show_expunged,show_torrent,use_direct):
    page=get_search(search_content,cats,rating,show_expunged,show_torrent,direct=use_direct)
    save_json("page.json",page)
    print(page)

@cli.command(help="|show the fetched galleries")
@click.option("--detailed/--no-detailed", "-d/", default=False)
def list(detailed):
    page=load_json("page.json",Page)
    echo_gl_table(detailed,page.gl_table)

@cli.command(help="|show and operate the gallery")
@click.option('--id','-i',default=0,help="default:0,gallery's index in galleries' list")
@click.option('--download/--no-download','-d/',default=False,help="select this to download gallery")
@click.option('--rename',default=None,type=str,help="rename gallery when download")
@click.option('--path','-p',default=None,type=click.Path(),help="download path,default is current directory")
@click.option('--stream/--no-stream','-s/',default=True,type=bool,help="enable stream download")
@click.option('--comment/--no-comment', '-c/',default=False,help="echo the comment of gallery")
def view(id,download,rename,path,stream,comment):
    page=load_json("page.json",Page)
    gl=page.gl_table[id]
    echo(gl)
    if download:
        gl.download(name=rename,path=path,stream=stream)
    elif comment:
        comment=gl.comment()
        if comment:
            for nick,cs in comment:
                echo(f"{FONT_STYLE.bold.value}{FONT_COLOR.green.value}{nick}{RESET}")
                for c in cs:
                    echo(f"\t{c}")
        else:
            echo("no comments")
    
@cli.command(help="|fetch popular galleries")
@click.option('--use-direct/--no-direct','-u',default=False,help="enable this to connect directly")
def popular(use_direct):
    page=get_popular(direct=use_direct)
    echo(f"Currently Popular Recent Galleries:{len(page.gl_table)}")
    save_json("page.json",page)

# testing
# @cli.command()
# @click.option('--params','-p',default=None)
# def t(params):
#     echo(params if params else "DEFAULT")
#     pass