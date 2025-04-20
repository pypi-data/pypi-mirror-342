from enum import Enum,unique
from ehentai.__version__ import __version__
@unique
class CATS(Enum):
    Doujinshi=1021
    Manga=1019
    Artist_CG=1015
    Game_CG=1007
    Western=511
    Non_H=767
    Image_Set=991
    Cosplay=959
    Asian_Porn=895
    Misc=1022

CATS_BG_COLOR={
    "Doujinshi":"\x1b[48;5;9m",
    "Manga":"\x1b[48;5;214m",
    "Artist CG":"\x1b[48;5;184m",
    "Game CG":"\x1b[48;5;28m",
    "Western":"\x1b[48;5;112m",
    "Non-H":"\x1b[48;5;44m",
    "Image Set":"\x1b[48;5;26m",
    "Cosplay":"\x1b[48;5;128m",
    "Asian Porn":"\x1b[48;5;212m",
    "Misc":"\x1b[48;5;250m",
}
@unique
class FONT_STYLE(Enum):
    reset="\x1b[0m"
    bold="\x1b[1m"
    faint="\x1b[2m"
    italic="\x1b[3m"
    underline="\x1b[4m"
    blink="\x1b[5m"
    reverse="\x1b[7m"
    hidden="\x1b[8m"
    strikethrough="\x1b[9m"

class FONT_COLOR(Enum):
    red="\x1b[38;5;160m"
    brown="\x1b[38;5;130m"
    orange="\x1b[38;5;208m"
    yellow="\x1b[38;5;226m"
    green="\x1b[38;5;112m"
    blue1="\x1b[38;5;45m"
    blue2="\x1b[38;5;21m"
    purple="\x1b[38;5;134m"
    pink="\x1b[38;5;199m"
    
RESET="\x1b[0m"