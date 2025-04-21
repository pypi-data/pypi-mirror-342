import click
import json
from click import echo
from typing import List
from ehentai.conf import *
from ehentai import __version__
from ehentai import Page,Gallery,get_search,get_popular
from ehentai.utils import save_Page,load_Page

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

def echo_gl_comment(comment):
    for nick,cs in comment:
                echo(f"{FONT_STYLE.bold.value}{FONT_COLOR.green.value}{nick}{RESET}")
                for c in cs:
                    echo(f"\t{c}")

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
@click.argument('search-content',default="")
@click.option('--cats','-c',default=255,type=int,help="Doujinshi,Manga...")
@click.option('--rating','-r',default=None,type=int,help="the minium rating")
@click.option('--show-expunged/--no-show-expunged','-sh/',default=False,help="show the removed galleries")
@click.option('--show-torrent/--no-show-torrent','-sto/',default=False,help="filter galleries have torrent")
def search(search_content,cats,rating,show_expunged,show_torrent):
    page=get_search(search_content,cats,rating,show_expunged,show_torrent)
    save_Page(page)
    print(page)

@cli.command(help="|show the fetched galleries")
@click.option("--detailed/--no-detailed", "-d/", default=False)
def list(detailed):
    page=load_Page()
    echo_gl_table(detailed,page.gl_table)

@cli.command(help="|show and operate the gallery")
@click.option('--id','-i',default=0,help="default:0,gallery's index in galleries' list")
@click.option('--download/--no-download','-d/',default=False,help="select this to download gallery")
@click.option('--rename',default=None,type=str,help="rename gallery when download")
@click.option('--path','-p',default=None,type=click.Path(),help="download path,default is current directory")
@click.option('--stream/--no-stream','-s/',default=True,type=bool,help="enable stream download")
@click.option('--comment/--no-comment', '-c/',default=False,help="echo the comment of gallery")
def view(id,download,rename,path,stream,comment):
    page=load_Page()
    gl=page.gl_table[id]
    echo(gl)
    if download:
        gl.download(name=rename,path=path,stream=stream)
    elif comment:
        comment=gl.comment()
        if comment:
            echo_gl_comment(comment)
        else:
            echo("no comments")
    
@cli.command(help="|fetch popular galleries")
def popular():
    page=get_popular()
    echo(f"Currently Popular Recent Galleries:{len(page.gl_table)}")
    save_Page(page)

# testing
# @cli.command()
# @click.option('--params','-p',default=None)
# def t(params):
#     echo(params if params else "DEFAULT")
#     pass