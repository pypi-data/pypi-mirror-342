import json
import os
from PIL import Image
import platform

# home path
HOME:str
match platform.system():
    case 'Windows':HOME=os.path.abspath(os.path.join(os.getenv('HOMEPATH'),".hentai"))
    case _:HOME=os.path.abspath(os.path.join(os.getenv('HOME'),".hentai"))

# json data
if not os.path.exists(HOME):
    os.makedirs(HOME)
def save_json(filename: str,data: object):
    with open(os.path.join(HOME,filename),"w") as f:
        f.write(json.dumps(data,default=lambda obj:obj.__dict__))
def load_json(filename: str,data_type):
    with open(os.path.join(HOME,filename),"r") as f:
        return data_type(**json.loads(f.read()))

# args:list[Image]
def merge_img():
    pass

# args:list[Image]
def img2pdf():
    pass
