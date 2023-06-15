import socket
import uuid,random
import os,xmlschema,sys,re
import flask
from flask import Flask,Response,send_from_directory,request,render_template
import json
from copy import deepcopy
from messages import *

from flask.wrappers import Request
from blueprints.events import events

__version__ = "2.0.0"

app = Flask(__name__)
# app.register_blueprint(events)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



# PATHS
SCRIPT_PATH = os.path.dirname(__file__)
VAST_PATH = os.path.join(SCRIPT_PATH,"vast")
VMAP_PATH = os.path.join(SCRIPT_PATH,"vmap")
# SERVER INFOS
with open(os.path.join(SCRIPT_PATH, "html","stub_info.html")) as fp:
    SERVER_INFO = fp.read()
SERVER_INFO = SERVER_INFO.replace("__version__",__version__)
SERVER_INFO = SERVER_INFO.replace("__pyver__",sys.version)
SERVER_INFO = SERVER_INFO.replace("__flask_version__",flask.__version__)


# DEFAULT NETWORK
# import netifaces as ni
# ni.ifaddresses('eth0')
# ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
# print(ip)  # should print "192.168.100.37"
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    STUB_HOST = s.getsockname()[0]
    s.close()
except Exception as err:
    print(err)

# STUB_HOST = "127.0.0.1"
LISTEN_PORT = 80

# TEMPLATES
TEMPLATE_DIR = os.path.join(SCRIPT_PATH, "templates",)
T_VAST_POD_AD = "T_VAST_POD_INLINE_AD.xml"
T_VAST_STANDALONE_AD = "T_VAST_STANDALONE_INLINE_AD.xml"
T_VAST_HEADER = "T_VAST_HEADER.xml"
T_VAST_FOOTER = "T_VAST_FOOTER.xml"
T_VMAP_ADBREAK_ITEM = "T_VMAP_ADBREAK_ITEM.xml"
T_VMAP = "T_VMAP.xml"

VAST_GENERATED_FILE = "generated_vast.xml"
VMAP_GENERATED_FILE = "generated_vmap.xml"

RESPONSES = {} # Dictionary of custom responses (on the fly)
DEFAULT_HEADERS = {'Access-Control-Allow-Origin': '*','charset': 'utf-8'}

DEFAULT_ADBREAK_VMAP_DATA = {
    "breakType": "linear",
    "timeOffset": random.choice(["start","end","00:01:00.000"]), # MUST set with requests (start(preroll),end(postroll),"hh:mm:ss.fff"(midroll))
    "breakId":uuid.uuid4(),
    "id":uuid.uuid4(),
    "allowMultipleAds": "false",
    "followRedirects": "true",
    "templateType": "vast3",
    "AdTagURI": "http://{host}/vast/autogen",
}

DEFAULT_TEMPLATE_DATA= {
    "ad_type":"inline", # [inline | wrapper]
    # "ad_sequence": 1, # (int) optional, if set ad is in pod with order defined
    "template_ad_id": "ADHBBTV_%s",
    "ad_title":"CREATIVE",
    "ad_description":"AD_description",
    "impression": "https://event/securepubads.g.doubleclick.net/pcs/view?xai=AKAOjstQn8XKa16rjdCdgDAk3PwxHcgAMl31WVfbYxqsTcJs_WI_nWw4lBZaN6VYIXBzDFHcWXueRyjAYLc6uzgmytPvjwLvWg9EoynCf69hLYCOeap-etguLvI7xi99ND7qMIK-qg5EAxauFCbiaIHThcvfo6yG-PMVoWoy_8YzzPVZ3OqvuLN6dR0YXoU_FJoRASL04qkAXYNMX5fnFoZp6Tt2vpsL4nFM97k6YvFclxT7FnvRfUzr2lkBJGxtQUp04g&sai=AMfl-YSBdnB6aDbl5UOs4y6HvEvtLM2bq_mqNxvA3l-DBNBx&sig=Cg0ArKJSzDQ_JHr9NEsOEAE&adurl=",
    "error": 'http://{host}/event/hhhsigh=sslpk9gubSo&label=videoplayfailed[ERRORCODE]' ,
    "start": "http://{host}/event/hhh0" ,
    "firstQuartile": "http://{host}/event/hhh25" ,
    "midpoint": "http://{host}/event/hhh50" ,
    "thirdQuartile": "http://{host}/event/hhh75" ,
    "complete": "http://{host}/event/hhh100" ,
    "mute": "http://{host}/event/hhhsigh=sslpk9gubSo&label=admute&ad_mt=[AD_MT]" ,
    "unmute": "http://{host}/event/hhhsigh=sslpk9gubSo&label=adunmute&ad_mt=[AD_MT]" ,
    "rewind": "http://{host}/event/hhhsigh=sslpk9gubSo&label=adrewind&ad_mt=[AD_MT]" ,
    "pause": "http://{host}/event/hhhsigh=sslpk9gubSo&label=adpause&ad_mt=[AD_MT]" ,
    "resume": "http://{host}/event/hhhsigh=sslpk9gubSo&label=adresume&ad_mt=[AD_MT]" ,
    "fullscreen": "http://{host}/event/hhhsigh=sslpk9gubSo&label=adfullscreen&ad_mt=[AD_MT]" ,
    "creativeView": "http://{host}/event/hhhsigh=sslpk9gubSo&label=vast_creativeview&ad_mt=[AD_MT]" ,
    "exitFullscreen": "http://{host}/event/hhhsigh=sslpk9gubSo&label=vast_exit_fullscreen&ad_mt=[AD_MT]" ,
    "acceptInvitationLinear": "http://{host}/event/hhhsigh=sslpk9gubSo&label=acceptinvitation&ad_mt=[AD_MT]" ,
    "closeLinear": "http://{host}/event/hhhsigh=sslpk9gubSo&label=adclose&ad_mt=[AD_MT]" ,
    "skip": "http://{host}/event/hhhsigh=sslpk9gubSo&label=videoskipped&ad_mt=[AD_MT]" ,
    "video_skip_shown": "http://{host}/event/hhhsigh=sslpk9gubSo&label=video_skip_shown&ad_mt=[AD_MT]" ,
    "video_engaged_view": "http://{host}/event/hhhsigh=sslpk9gubSo&label=video_engaged_view&ad_mt=[AD_MT]" ,
    "ClickThrough": "http://{host}/event/pcs/click?xai=AKAOjsu-RcXCgn02yYoM8LFnnQSgUow1XTgUaUEzV22QVz5BKFbARMapKfkmghfF6zK3JpidpKgNUbtq7w-yygN6UvFLV3YhdsZAVSa_ZNWleqh-uR1hDXSefWqO_ohb0muCE8Of2dKmZG3sez9gQNM-nogjg-HYmelOGTVkCL3QQpT9yeVzgDAUrFXS15kUqk_r6-ZPHu1CWQ8oXJktxdY4YPXSJblydMf4tfMyeyE4l81_zb4YSHQrZR5biVW5Sg&sig=Cg0ArKJSzASr7QlljqBd&adurl=http://www.partner.co.il" 
}
