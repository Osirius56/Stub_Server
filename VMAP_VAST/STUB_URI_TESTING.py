import requests
from pprint import pprint

req_list = [
    "http://{host}:{port}/hhh0",
    "http://{host}:{port}/hhh25",
    "http://{host}:{port}/hhh50",
    "http://{host}:{port}/hhh75",
    "http://{host}:{port}/hhh100",
    "http://{host}:{port}/hhhsigh=sslpk9gubSo&label=admute&ad_mt=[AD_MT]",
    "http://{host}:{port}/hhhsigh=sslpk9gubSo&label=adunmute&ad_mt=[AD_MT]",
    "http://{host}:{port}/hhhsigh=sslpk9gubSo&label=adrewind&ad_mt=[AD_MT]",
    "http://{host}:{port}/hhhsigh=sslpk9gubSo&label=adpause&ad_mt=[AD_MT]",
    "http://{host}:{port}/hhhsigh=sslpk9gubSo&label=adresume&ad_mt=[AD_MT]",
    "http://{host}:{port}/hhhsigh=sslpk9gubSo&label=adfullscreen&ad_mt=[AD_MT]",
    "http://{host}:{port}/hhhsigh=sslpk9gubSo&label=vast_creativeview&ad_mt=[AD_MT]",
    "http://{host}:{port}/hhhsigh=sslpk9gubSo&label=vast_exit_fullscreen&ad_mt=[AD_MT]",
    "http://{host}:{port}/hhhsigh=sslpk9gubSo&label=acceptinvitation&ad_mt=[AD_MT]",
    "http://{host}:{port}/hhhsigh=sslpk9gubSo&label=adclose&ad_mt=[AD_MT]",
    "http://{host}:{port}/hhhsigh=sslpk9gubSo&label=videoskipped&ad_mt=[AD_MT]",
    "http://{host}:{port}/hhhsigh=sslpk9gubSo&label=video_skip_shown&ad_mt=[AD_MT]",
    "http://{host}:{port}/hhhsigh=sslpk9gubSo&label=video_engaged_view&ad_mt=[AD_MT]"
]

host = "197.30.30.181"
port = 81

results = [requests.get(uri.format(host=host,port=port)) for uri in req_list]

pprint(results)