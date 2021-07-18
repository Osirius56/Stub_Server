# import socket
# import uuid,random
# import os,xmlschema,sys,re
# import flask
# from flask import Flask,Response,send_from_directory,request,render_template
# import json
# from copy import deepcopy
# from messages import *

# from flask.wrappers import Request
# from blueprints.events import events
from methods import *
"""This stub server developed under Flask (Python) allows you to respond to the various events raised by the SmartLib.
It also offers the possibility of providing VAST / VMAP that can be published via API:
 - API '/vast/static/<id>': VAST / VMAP publication in XML format, specific and identified by an ID (can be added, modified, deleted and retrieved)
 - API '/vast/autogen': Automatic generation of a document from JSON data.
"""

# __version__ = "2.0.0"

# app = Flask(__name__)
# # app.register_blueprint(events)

# class bcolors:
#     HEADER = '\033[95m'
#     OKBLUE = '\033[94m'
#     OKCYAN = '\033[96m'
#     OKGREEN = '\033[92m'
#     WARNING = '\033[93m'
#     FAIL = '\033[91m'
#     ENDC = '\033[0m'
#     BOLD = '\033[1m'
#     UNDERLINE = '\033[4m'

# def _check_path(path):
#     if not os.path.isdir(path):
#         os.makedirs(path)
#         assert os.path.isdir(path),"%sCouldn't find or create %s %s" %(bcolors.FAIL,path,bcolors.ENDC)
#     return path

# # PATHS
# SCRIPT_PATH = os.path.dirname(__file__)
# VAST_PATH = os.path.join(SCRIPT_PATH,"vast")
# VMAP_PATH = os.path.join(SCRIPT_PATH,"vmap")
# # SERVER INFOS
# with open(os.path.join(SCRIPT_PATH, "html","stub_info.html")) as fp:
#     SERVER_INFO = fp.read()
# SERVER_INFO = SERVER_INFO.replace("__version__",__version__)
# SERVER_INFO = SERVER_INFO.replace("__pyver__",sys.version)
# SERVER_INFO = SERVER_INFO.replace("__flask_version__",flask.__version__)


# # DEFAULT NETWORK
# # import netifaces as ni
# # ni.ifaddresses('eth0')
# # ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
# # print(ip)  # should print "192.168.100.37"
# try:
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.connect(("8.8.8.8", 80))
#     STUB_HOST = s.getsockname()[0]
#     s.close()
# except Exception as err:
#     print(err)

# # STUB_HOST = "127.0.0.1"
# LISTEN_PORT = 81

# # TEMPLATES
# TEMPLATE_DIR = os.path.join(SCRIPT_PATH, "templates",)
# T_VAST_POD_AD = "T_VAST_POD_INLINE_AD.xml"
# T_VAST_STANDALONE_AD = "T_VAST_STANDALONE_INLINE_AD.xml"
# T_VAST_HEADER = "T_VAST_HEADER.xml"
# T_VAST_FOOTER = "T_VAST_FOOTER.xml"
# T_VMAP_ADBREAK_ITEM = "T_VMAP_ADBREAK_ITEM.xml"
# T_VMAP = "T_VMAP.xml"

# VAST_GENERATED_FILE = "generated_vast.xml"
# VMAP_GENERATED_FILE = "generated_vmap.xml"

# RESPONSES = {} # Dictionary of custom responses (on the fly)
# DEFAULT_HEADERS = {'Access-Control-Allow-Origin': '*','charset': 'utf-8'}

# DEFAULT_ADBREAK_VMAP_DATA = {
#     "breakType": "linear",
#     "timeOffset": random.choice(["start","end","00:01:00.000"]), # MUST set with requests (start(preroll),end(postroll),"hh:mm:ss.fff"(midroll))
#     "breakId":uuid.uuid4(),
#     "id":uuid.uuid4(),
#     "allowMultipleAds": "false",
#     "followRedirects": "true",
#     "templateType": "vast3",
#     "AdTagURI": "http://{host}/vast/autogen",
# }

# DEFAULT_TEMPLATE_DATA= {
#     "ad_type":"inline", # [inline | wrapper]
#     # "ad_sequence": 1, # (int) optional, if set ad is in pod with order defined
#     "template_ad_id": "ADHBBTV_%s",
#     "ad_title":"CREATIVE",
#     "ad_description":"AD_description",
#     "impression": "https://event/securepubads.g.doubleclick.net/pcs/view?xai=AKAOjstQn8XKa16rjdCdgDAk3PwxHcgAMl31WVfbYxqsTcJs_WI_nWw4lBZaN6VYIXBzDFHcWXueRyjAYLc6uzgmytPvjwLvWg9EoynCf69hLYCOeap-etguLvI7xi99ND7qMIK-qg5EAxauFCbiaIHThcvfo6yG-PMVoWoy_8YzzPVZ3OqvuLN6dR0YXoU_FJoRASL04qkAXYNMX5fnFoZp6Tt2vpsL4nFM97k6YvFclxT7FnvRfUzr2lkBJGxtQUp04g&sai=AMfl-YSBdnB6aDbl5UOs4y6HvEvtLM2bq_mqNxvA3l-DBNBx&sig=Cg0ArKJSzDQ_JHr9NEsOEAE&adurl=",
#     "error": 'http://{host}/event/hhhsigh=sslpk9gubSo&label=videoplayfailed[ERRORCODE]' ,
#     "start": "http://{host}/event/hhh0" ,
#     "firstQuartile": "http://{host}/event/hhh25" ,
#     "midpoint": "http://{host}/event/hhh50" ,
#     "thirdQuartile": "http://{host}/event/hhh75" ,
#     "complete": "http://{host}/event/hhh100" ,
#     "mute": "http://{host}/event/hhhsigh=sslpk9gubSo&label=admute&ad_mt=[AD_MT]" ,
#     "unmute": "http://{host}/event/hhhsigh=sslpk9gubSo&label=adunmute&ad_mt=[AD_MT]" ,
#     "rewind": "http://{host}/event/hhhsigh=sslpk9gubSo&label=adrewind&ad_mt=[AD_MT]" ,
#     "pause": "http://{host}/event/hhhsigh=sslpk9gubSo&label=adpause&ad_mt=[AD_MT]" ,
#     "resume": "http://{host}/event/hhhsigh=sslpk9gubSo&label=adresume&ad_mt=[AD_MT]" ,
#     "fullscreen": "http://{host}/event/hhhsigh=sslpk9gubSo&label=adfullscreen&ad_mt=[AD_MT]" ,
#     "creativeView": "http://{host}/event/hhhsigh=sslpk9gubSo&label=vast_creativeview&ad_mt=[AD_MT]" ,
#     "exitFullscreen": "http://{host}/event/hhhsigh=sslpk9gubSo&label=vast_exit_fullscreen&ad_mt=[AD_MT]" ,
#     "acceptInvitationLinear": "http://{host}/event/hhhsigh=sslpk9gubSo&label=acceptinvitation&ad_mt=[AD_MT]" ,
#     "closeLinear": "http://{host}/event/hhhsigh=sslpk9gubSo&label=adclose&ad_mt=[AD_MT]" ,
#     "skip": "http://{host}/event/hhhsigh=sslpk9gubSo&label=videoskipped&ad_mt=[AD_MT]" ,
#     "video_skip_shown": "http://{host}/event/hhhsigh=sslpk9gubSo&label=video_skip_shown&ad_mt=[AD_MT]" ,
#     "video_engaged_view": "http://{host}/event/hhhsigh=sslpk9gubSo&label=video_engaged_view&ad_mt=[AD_MT]" ,
#     "ClickThrough": "http://{host}/event/pcs/click?xai=AKAOjsu-RcXCgn02yYoM8LFnnQSgUow1XTgUaUEzV22QVz5BKFbARMapKfkmghfF6zK3JpidpKgNUbtq7w-yygN6UvFLV3YhdsZAVSa_ZNWleqh-uR1hDXSefWqO_ohb0muCE8Of2dKmZG3sez9gQNM-nogjg-HYmelOGTVkCL3QQpT9yeVzgDAUrFXS15kUqk_r6-ZPHu1CWQ8oXJktxdY4YPXSJblydMf4tfMyeyE4l81_zb4YSHQrZR5biVW5Sg&sig=Cg0ArKJSzASr7QlljqBd&adurl=http://www.partner.co.il" 
# }

# # METHODS
# def head_update(html):
#     return html.replace("__version__",__version__).replace("__pyver__",sys.version).replace("__flask_version__",flask.__version__)

# def get_validation_errors(xml, xsd_uri):
#     dir_path = os.path.dirname(os.path.realpath(__file__))

#     if os.path.isfile(xml):
#         with open(xml,'rb') as fp:
#             xml_string = fp.read().decode('utf-8')
#     elif isinstance(xml,bytes):
#         xml_string = xml.decode('utf_8')
#     elif isinstance(xml,str):
#         xml_string = xml
    
        
#     xsd_path = os.path.join(dir_path, xsd_uri)
#     schema = xmlschema.XMLSchema(xsd_path)
#     validation_error_iterator = schema.iter_errors(xml_string)
    
#     xml_schema_error = []
#     for idx, validation_error in enumerate(validation_error_iterator, start=1):
#         xml_schema_error.append(f'[{idx}] path: {validation_error.path} | reason: {validation_error.reason}')
    
#     return xml_schema_error

# def update_uri(data):
#     output = []
#     docs = []
#     output_matrix = []
#     rx_rules = re.compile(r"Rule\s*'(?P<uri>.*)'\s*\((?P<methods>.*)\)\s*->\s*(?P<name>.*)>")
#     mapping = rx_rules.findall(str(data))
#     # print(mapping)
#     # mapping = str(data).replace("<", "").replace(">", "").replace("Rule", "").replace("[", "").replace("]", "").replace("Map", " ").replace(")", "").replace("(", "")

#     # m = mapping.split(",\n")
#     # a = [re.split("(^,\s+|' | - )",z) for z in m]
#     for index,data_tuple in enumerate(mapping):
#         formated_data = []
#         for data in data_tuple:
#             data = data.replace("<","&lt;").replace(">","&gt;").replace("'","")
#             formated_data.append(data)
#             print("data : %s" % data)
#         output_matrix.append(formated_data)
#         print(output_matrix)
#         if formated_data[2] not in ("index","favicon"):
#             if not str(formated_data[2]).startswith("doc_") :
#                 output.append("<li><div>%s</div></li>" % " ".join(["<h4>"+formated_data[2]+"</h4>","<p class='methods'><code>"+formated_data[1]+"</code></p>","<p class='url'>"+formated_data[0]+"</p>"]))
#                 output.sort()
#             else:
#                 docs.append("<li><div>%s</div></li>" % " ".join(["<h4><a href="+formated_data[0]+">"+formated_data[2].replace("doc_",'')+"</a></h4>","<p class='url'>"+formated_data[0]+"</p>"]))
#     m = "\n".join(output)
#     doc = "\n".join(docs)

#     # m = ["<li>%s" % i for i in m]
#     # m = "</li>".join(m)
#     return SERVER_INFO.replace("__data__", "<ul>"+m.replace("'","")+"</ul>").replace("__doc__", "<ul>"+doc.replace("'","")+"</ul>")#, output_matrix

# def mediafile_cdata_write(cdata):
#     return "<![CDATA[%s]]>" % cdata

# def mediafile_write(paramDict):
#     print(paramDict)
#     cdata = paramDict.pop("cdata")
#     string = "<MediaFile "
#     for param,value in paramDict.items():
#         string = "%s %s=\"%s\"" % (string,param,value)
#     string = "%s> %s </MediaFile>" % (string,mediafile_cdata_write(cdata))
#     return string

# def vast_generate(request, output=os.path.join(_check_path(VAST_PATH), VAST_GENERATED_FILE)):
#     # add header and footer after treat all ads by for loop
#     with open(os.path.join(TEMPLATE_DIR, T_VAST_HEADER)) as fp:
#         header = fp.read()
#     with open(os.path.join(TEMPLATE_DIR, T_VAST_FOOTER)) as fp:
#         footer = fp.read()
#     if request.json != None:
#         if not isinstance(request.json,list):
#             data_list = [request.json]
#         else:
#             data_list = request.json
#     else:
#         data_list = [DEFAULT_TEMPLATE_DATA]

#     ad_list = [header, footer]

#     for ad in data_list:
#         assert ad["template_ad_id"]
#         assert ad["skipoffset"]
#         assert ad["duration"]

#         if "ad_sequence" in ad:
#             XML_TEMPLATE = T_VAST_POD_AD
#         else :
#             XML_TEMPLATE = T_VAST_STANDALONE_AD

#         # print(XML_TEMPLATE)
#         with open(os.path.join(TEMPLATE_DIR, XML_TEMPLATE)) as fp:
#             xml = fp.read()

#         data = deepcopy(DEFAULT_TEMPLATE_DATA)
#         data = dict([[key,value.format(host=request.host)] for key,value in data.items()])
#         # print("data:%s" % data)
#         ad["mediafile"] = mediafile_write(ad["mediafile"])
#         data.update(ad)
#         ad_list.insert(-1, xml.format(**data))
    
#     xml = "\n".join(ad_list)
    
#     with open(output, "w") as fp:
#         fp.writelines(ad_list)
    
#     return xml

# def vmap_generate(request, output=os.path.join(_check_path(VMAP_PATH), VMAP_GENERATED_FILE)):
#     # add header and footer after treat all ads by for loop
#     ad_break_list = []
    
#     with open(os.path.join(TEMPLATE_DIR, T_VMAP)) as fp:
#         body = fp.read()

#     with open(os.path.join(TEMPLATE_DIR, T_VMAP_ADBREAK_ITEM)) as fp:
#         content = fp.read()

#     if request.json != None:
#         if not isinstance(request.json,list):
#             data_list = [request.json]
#         else:
#             data_list = request.json
#     else:
#         data_list = [DEFAULT_ADBREAK_VMAP_DATA]
    
#     for adbreak in data_list:
#         data = deepcopy(DEFAULT_ADBREAK_VMAP_DATA)
#         data["timeOffset"] = random.choice(["start","end","00:01:00.000"])
#         data["breakId"] = uuid.uuid4()
#         data["id"] = uuid.uuid4()
#         data = dict([[key,value] for key,value in data.items()])
#         print(data)
#         print(adbreak)
#         data.update(adbreak)
#         print(data)
#         ad_break_list.append(content.format(**data))
    
#     xml = body.format(ad_breaks="\n".join(ad_break_list)).format(host=request.host)
#     with open(output, "w") as fp:
#         fp.write(xml)
    
#     return xml

# def check_vast(data,xsd_uri='schema/vast3_draft.xsd'):
#     try:
#         xml_error = get_validation_errors(data, xsd_uri)
#         print("xml_error %s "% xml_error)
#         if len(xml_error) > 0:
#             msg = deepcopy(MSG_400_BAD_REQUEST)
#             msg["error"] = "\n".join(xml_error)
#             return Response(json.dumps(msg) ,mimetype="application/json",headers=DEFAULT_HEADERS,status=500)
#         # else:
#         #     return Response(data, mimetype='text/xml',headers=DEFAULT_HEADERS)
#     except Exception as err:
#         msg = deepcopy(MSG_500_INTERNAL_ERROR)
#         msg['error'] = str(err)
#         return Response(json.dumps(msg) ,mimetype="application/json",headers=DEFAULT_HEADERS,status=500)

# def check_vmap(data, xsd_uri='schema/vmap_1.0.xsd'):
#     try:
#         xml_error = get_validation_errors(data, xsd_uri)
#         if len(xml_error) > 0:
#             msg = deepcopy(MSG_400_BAD_REQUEST)
#             msg["error"] = "\n".join(xml_error)
#             return Response(json.dumps(msg) ,mimetype="application/json",headers=DEFAULT_HEADERS,status=400)
#         # else:
#         #     return Response(data, mimetype='text/xml',headers=DEFAULT_HEADERS)
#     except Exception as err:
#         msg = deepcopy(MSG_500_INTERNAL_ERROR)
#         msg['error'] = str(err)
#         return Response(json.dumps(msg) ,mimetype="application/json",headers=DEFAULT_HEADERS,status=500)


# ROUTES
# -- INDEX
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    # return SERVER_INFO
    return update_uri(app.url_map)

# -- VMAP
@app.route("/vmap/")
def doc_vmap():
    return send_from_directory("./","html/vmap_info.html")

@app.route("/vmap/static/<id>",methods=["DELETE","POST","GET"])
def vmap_static(id):
    output = "%s.xml" % id
    msg = deepcopy(MSG_200_OK)
    print("req.data %s " % request.data)
    if request.method == "DELETE":
        if os.path.isfile(os.path.join(VMAP_PATH,output)):
            status = 200
            try:
                os.remove(os.path.join(VMAP_PATH,output))
                msg["message"] = "%s removed sucessfully" % id
            except Exception as error:
                msg["message"] = error
        else:
            msg["message"] = "Resource not found"
            status = 404
        return Response(json.dumps(msg),mimetype="application/json",headers=DEFAULT_HEADERS,status=status)

    if request.method == "POST":
        # response = check_vmap(request.data)
        # print("resp %s" % response)
        # if response != None:
        #     return response
        
        if os.path.isfile(os.path.join(VMAP_PATH,output)):
            msg = deepcopy(MSG_409_CONFLICT)
            return Response(json.dumps(msg),mimetype="application/json",headers=DEFAULT_HEADERS,status=409)
        else:
            # try:
            with open(os.path.join(_check_path(VMAP_PATH),output), "wb") as fp:
                fp.write(request.data)
            if os.path.isfile(os.path.join(VMAP_PATH,output)):
                msg = deepcopy(MSG_201_CREATED)
                return Response(json.dumps(msg),mimetype="application/json",headers=DEFAULT_HEADERS,status=201)
            else :
                msg = deepcopy(MSG_500_INTERNAL_ERROR)
                msg["error"] =  "File %s can't be created without server error."%id
                return Response(json.dumps(msg),mimetype="application/json",headers=DEFAULT_HEADERS,status=500)
            # except Exception as err:
                # return Response(json.dumps(MSG_404_NOT_FOUND) ,mimetype="application/json",headers=DEFAULT_HEADERS,status=500)

    if request.method == "PUT":
        pass
    if request.method == "GET":
        try:
            with open(os.path.join(VMAP_PATH,output)) as fp:
                VAST = fp.read()
            return Response(VAST, mimetype='text/xml',headers=DEFAULT_HEADERS,status=200)
        except Exception as error:
            msg = deepcopy(MSG_404_NOT_FOUND)
            msg["error"] = "VAST Not Found"
            return Response(json.dumps(msg) ,mimetype="application/json",headers=DEFAULT_HEADERS,status=404)

@app.route("/vmap/autogen",methods=["PUT","GET"])
def vmap_dynamic():
    if request.method == "PUT":
        # response = check_vmap(vmap_generate(request))
        response = Response(vmap_generate(request), mimetype='text/xml',headers=DEFAULT_HEADERS)
        # msg = MSG_200_OK
        # msg['message'] = vmap_generate(request)
        # response = Response(json.dumps(msg),mimetype="application/json",headers=DEFAULT_HEADERS,status=200)

    else:
        try:
            if request.args['type'] == "text":
                mimetype = 'text/plain'
            else :
                mimetype='text/xml'
        except Exception as err:
            mimetype = 'text/xml'

        with open(os.path.join(VMAP_PATH, VMAP_GENERATED_FILE)) as fp:
            VMAP = fp.read()
            response = Response(VMAP, mimetype=mimetype,headers=DEFAULT_HEADERS)
    return response

# -- VAST
@app.route("/vast/")
def doc_vast():
    return send_from_directory("./","html/vast_info.html")

@app.route('/vast/static/<id>',methods=["DELETE","PUT","GET"])
def vast_static(id):
    """ Args : no_check | activate VAST schema validation passthrough (no validation)
    """
    output = "%s.xml" % id
    msg = deepcopy(MSG_200_OK)
    print("req.data %s " % request.data)
    if request.method == "DELETE":
        if os.path.isfile(os.path.join(VAST_PATH,output)):
            status = 200
            try:
                os.remove(os.path.join(VAST_PATH,output))
                msg["message"] = "%s removed sucessfully" % id
            except Exception as error:
                msg["message"] = error
        else:
            msg["message"] = "Resource not found"
            status = 404
        return Response(json.dumps(msg),mimetype="application/json",headers=DEFAULT_HEADERS,status=status)

    if request.method == "PUT":
        try:
            request.args['no_check']
        except:
            print("no_check VAST data")
            response = check_vast(request.data)
            print("resp %s" % response)
            if response != None:
                return response
        
        if os.path.isfile(os.path.join(VAST_PATH,output)):
            msg = deepcopy(MSG_409_CONFLICT)
            return Response(json.dumps(msg),mimetype="application/json",headers=DEFAULT_HEADERS,status=409)
        else:
            # try:
            with open(os.path.join(_check_path(VAST_PATH),output), "wb") as fp:
                fp.write(request.data)
            if os.path.isfile(os.path.join(VAST_PATH,output)):
                msg = deepcopy(MSG_201_CREATED)
                return Response(json.dumps(msg),mimetype="application/json",headers=DEFAULT_HEADERS,status=201)
            else :
                msg = deepcopy(MSG_500_INTERNAL_ERROR)
                msg["error"] =  "File %s can't be created without server error."%id
                return Response(json.dumps(msg),mimetype="application/json",headers=DEFAULT_HEADERS,status=500)
            # except Exception as err:
                # return Response(json.dumps(MSG_404_NOT_FOUND) ,mimetype="application/json",headers=DEFAULT_HEADERS,status=500)

    if request.method == "GET":
        try:
            with open(os.path.join(VAST_PATH,output)) as fp:
                VAST = fp.read()
            return Response(VAST, mimetype='text/xml',headers=DEFAULT_HEADERS,status=200)
        except Exception as error:
            msg = deepcopy(MSG_404_NOT_FOUND)
            msg["error"] = "VAST Not Found"
            return Response(json.dumps(msg) ,mimetype="application/json",headers=DEFAULT_HEADERS,status=404)

@app.route('/vast/autogen',methods=["PUT","GET"])
def vast_dynamic():
    if request.method == "PUT":
        try:
            vast = vast_generate(request)
            response = check_vast(vast)
            if response != None:
                return response
        except Exception as err:
            msg = deepcopy(MSG_500_INTERNAL_ERROR)
            msg['error'] = str(err)
            response = Response(json.dumps(msg) ,mimetype="application/json",headers=DEFAULT_HEADERS,status=500)
        
    with open(os.path.join(VAST_PATH, VAST_GENERATED_FILE)) as fp:
        VAST = fp.read()
        try:
            if request.args['type'] == "text":
                mimetype = 'text/plain'
            else :
                mimetype='text/xml'
        except Exception as err:
            mimetype = 'text/xml'
    return Response(VAST, mimetype=mimetype,headers=DEFAULT_HEADERS)

@app.route('/event/<event_uri>',methods=["GET"])
def custom_event(event_uri):
    if request.args.get("code") == None:
        status_code = 200
    else :
        status_code = request.args.get("code")
    
    if request.args.get("msg") == None:
        msg = "%s 200 OK" % event_uri
    else :
        msg = request.args.get("msg")

    return Response(msg,status=status_code,headers=DEFAULT_HEADERS)

@app.route('/custom/',methods=["GET"])
def doc_custom():
    with open(os.path.join(SCRIPT_PATH, "html/custom_urls_info.html")) as fp:
        CUSTOM_URL_INFO = fp.read()
    example="""{
                "status_code": 200,
                "message" : "You Win",
                "headers":{
                    "content-type": "text",
                    "my-custom-header": "test01"
                }
            }"""
    return Response(head_update(CUSTOM_URL_INFO).format(host=STUB_HOST,port=LISTEN_PORT,example=example),status=200,headers=DEFAULT_HEADERS)

@app.route('/custom/<custom_uri>',methods=["GET","PUT","DELETE"])
def custom(custom_uri):
    if request.method == "DELETE":
        try:
            RESPONSES.pop(custom_uri)
        except Exception as err:
            print(err)
        return Response("%s correctly deleted" % custom_uri)

    if request.method == "PUT":
        headers = DEFAULT_HEADERS
        if "headers" in str(request.json.keys()).lower():
            headers.update(request.json["headers"])
        RESPONSES[custom_uri] = Response(request.json["message"],status=request.json["status_code"],headers=headers)
        return Response("%s set" % custom_uri,status=200,headers=DEFAULT_HEADERS)
    else :
        try:
            return RESPONSES[custom_uri]
        except:
            return Response("%s not found" % custom_uri,status=404)


if __name__ == "__main__":
    """Main script to run STUB with static confguration of ads in vast. Should include an api to change vast ads data (in version 2.0.0)
    """
    import argparse
    import json
    from collections import namedtuple
 

    parser = argparse.ArgumentParser(prog=os.path.basename(__file__))
    parser.add_argument("-f","--json-file",help="Stub default data to describe static ads to include in vast",default="data/mp4_pod_3ads.json")
    parser.add_argument("-H","--host",help="Define host (IP or DNS) for Stub server",required=False,type=str,default=STUB_HOST)
    parser.add_argument("-p","--port",help="Define port of stub (default = 80)",required=False,type=int,default=LISTEN_PORT)

    args = parser.parse_args()
    
    with open(args.json_file) as fp:
        vast_data = {"json": json.load(fp),"host":"%s:%s" % (args.host,args.port)}
    
    data = namedtuple('Struct', vast_data.keys())(*vast_data.values())
    vast_generate(data)
    app.run(host=str(args.host),port=args.port)


